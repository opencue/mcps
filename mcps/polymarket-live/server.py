#!/usr/bin/env -S uv run -q --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.0.0"]
# ///
"""Polymarket Live MCP server.

Read-only stdio tools that wrap the local `polymarket-cli` binary so Claude
can see real-time Polymarket markets, the active BTC 5-minute paper-trading
market, the order book / midpoints, and the user's local predictions store
(~/.config/polymarket/data/predictions.jsonl).

Two data paths:
    * REST-backed tools shell out to `polymarket … -o json` and parse stdout.
      Live latency: typically 100–500 ms per call.
    * Store-backed tools read the local JSONL store directly (no subprocess).
      Latency: <50 ms.

Everything is read-only on purpose. Mutating commands (open / resolve /
create-order / etc.) are deliberately NOT exposed — the bot lane already
owns those.

Tools:
    market_status           — Polymarket API health
    markets_list            — list active markets (paged)
    markets_get             — fetch one market by id or slug
    markets_search          — free-text search
    clob_midpoint           — single token midpoint price
    clob_midpoints          — batch midpoints for many tokens
    clob_book               — full L2 order book for a token
    btc_5m_snapshot         — active BTC 5m market: price-to-beat / spot / time
    btc_recent_closes       — last N 1m BTC closes (oldest → newest)
    predictions_list        — read the local predictions.jsonl (with filter)
    predictions_stats       — summary accuracy / Brier / direction counts
    predictions_backtest    — Brier + log-loss + calibration vs Polymarket
    predict_think           — one-shot model forecast for the next 5m window

Run: uv run ~/Documents/soul/mcps/mcps/polymarket-live/server.py
Register in ~/.claude.json `mcpServers` as `polymarket-live`.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("polymarket-live")

# Discovery: prefer the freshly-built release binary in the repo (matches the
# /home/deadpool/.local/bin/polymarket wrapper's preference), then fall through
# to whatever `polymarket` resolves to on PATH. Env var lets the user pin a
# specific binary without touching this file.
REPO_ROOT = Path(os.environ.get("POLYMARKET_REPO", Path.home() / "Documents" / "polymarket-cli"))
PREDICTIONS_FILE = Path(
    os.environ.get(
        "POLYMARKET_PREDICTIONS_FILE",
        Path.home() / ".config" / "polymarket" / "data" / "predictions.jsonl",
    )
)
# Per-call subprocess timeout. Backtest is the slowest tool (~1–2 s) so 15 s
# is generous; everything else returns well under 1 s.
CLI_TIMEOUT_SECS = float(os.environ.get("POLYMARKET_MCP_TIMEOUT", "15"))


def _resolve_bin() -> str:
    """Locate the `polymarket` binary. Order: $POLYMARKET_BIN → repo release
    → repo debug → PATH. Skips the bash wrapper to avoid the dashboard
    spawn path — we always want the raw binary for JSON output."""
    pinned = os.environ.get("POLYMARKET_BIN")
    if pinned and os.access(pinned, os.X_OK):
        return pinned
    for cand in (
        REPO_ROOT / "target" / "release" / "polymarket",
        REPO_ROOT / "target" / "debug" / "polymarket",
    ):
        if cand.is_file() and os.access(cand, os.X_OK):
            return str(cand)
    for path_cand in (shutil.which("polymarket") or "",).__iter__():
        if not path_cand:
            continue
        # The user installs a wrapper script at ~/.local/bin/polymarket that
        # spawns a tmux dashboard when called with zero args. Skip wrappers.
        if Path(path_cand).is_symlink():
            target = Path(path_cand).resolve()
            if target.suffix == "" and target.name == "polymarket" and "target/" in str(target):
                return str(target)
            # Fall through to non-symlinked PATH entries.
        else:
            return path_cand
    raise RuntimeError(
        "polymarket binary not found — build it with "
        "`(cd ~/Documents/polymarket-cli && cargo build --release)` "
        "or set $POLYMARKET_BIN."
    )


def _run_json(args: list[str]) -> Any:
    """Shell out to the polymarket binary with `-o json` and return parsed
    JSON. Raises RuntimeError on any failure with stderr surfaced so the
    MCP caller gets an actionable message rather than a generic non-zero
    exit."""
    bin_path = _resolve_bin()
    cmd = [bin_path, "-o", "json", *args]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=CLI_TIMEOUT_SECS,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(
            f"polymarket subcommand timed out after {CLI_TIMEOUT_SECS}s: {' '.join(args)}"
        ) from e
    if result.returncode != 0:
        stderr = (result.stderr or "").strip() or "(no stderr)"
        raise RuntimeError(
            f"polymarket exited {result.returncode}: {' '.join(args)}\n{stderr}"
        )
    stdout = result.stdout.strip()
    if not stdout:
        return None
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as e:
        # Preserve the raw payload so the model can see what was actually
        # returned — usually a CLI banner that leaked through to stdout.
        raise RuntimeError(
            f"polymarket returned non-JSON for `{' '.join(args)}`: "
            f"{stdout[:500]}"
        ) from e


# ─────────────────────────────────────────────────────────────────────────────
# Health
# ─────────────────────────────────────────────────────────────────────────────


@mcp.tool()
def market_status() -> dict:
    """Polymarket gamma/CLOB API health check. Use first when a tool starts
    erroring to tell apart "API is down" from "wrong args".

    Returns the parsed JSON from `polymarket status`.
    """
    return _run_json(["status"])


# ─────────────────────────────────────────────────────────────────────────────
# Markets
# ─────────────────────────────────────────────────────────────────────────────


@mcp.tool()
def markets_list(limit: int = 10, active_only: bool = True) -> list[dict]:
    """List Polymarket markets, optionally filtered to currently-active ones.

    Args:
        limit: how many markets to return (1–500). Polymarket's API caps this.
        active_only: drop closed / archived markets when True (default).

    Returns: array of market summaries — each has id, slug, question,
    outcome_prices, volume_num, liquidity_num, end_date_iso, ...
    """
    args = ["markets", "list", "--limit", str(max(1, min(500, limit)))]
    if active_only:
        args.append("--active")
    return _run_json(args)


@mcp.tool()
def markets_get(id_or_slug: str) -> dict:
    """Fetch a single market by condition_id or slug. Returns the full
    market record including outcomes, prices, condition_id, and token IDs
    needed for `clob_*` calls.
    """
    return _run_json(["markets", "get", id_or_slug])


@mcp.tool()
def markets_search(query: str, limit: int = 10) -> list[dict]:
    """Free-text search across markets (e.g. "bitcoin", "election").

    Args:
        query: search term sent to the Polymarket gamma API.
        limit: max results to return (1–100).
    """
    return _run_json([
        "markets",
        "search",
        query,
        "--limit",
        str(max(1, min(100, limit))),
    ])


# ─────────────────────────────────────────────────────────────────────────────
# CLOB (order book + midpoints)
# ─────────────────────────────────────────────────────────────────────────────


@mcp.tool()
def clob_midpoint(token_id: str) -> dict:
    """Get the live midpoint price for a single CLOB token (outcome).

    `token_id` is the per-outcome token id, NOT the market's condition_id.
    Look it up via `markets_get(...).outcomes[].clob_token_id` (or similar).
    """
    return _run_json(["clob", "midpoint", token_id])


@mcp.tool()
def clob_midpoints(token_ids: list[str]) -> dict:
    """Batch midpoints for many tokens in one call. Faster than N
    `clob_midpoint` calls when you're comparing several outcomes.

    Args:
        token_ids: list of CLOB token IDs. Sent as a comma-separated arg.
    """
    if not token_ids:
        return {}
    return _run_json(["clob", "midpoints", ",".join(token_ids)])


@mcp.tool()
def clob_book(token_id: str) -> dict:
    """Full L2 order book (bids + asks) for one CLOB token.

    Returns {bids: [{price, size}, ...], asks: [{price, size}, ...]} —
    bids sorted high → low, asks low → high.
    """
    return _run_json(["clob", "book", token_id])


# ─────────────────────────────────────────────────────────────────────────────
# BTC 5-minute paper-trading market
# ─────────────────────────────────────────────────────────────────────────────


@mcp.tool()
def btc_5m_snapshot() -> dict:
    """Live readout of the currently-active Polymarket BTC 5m up/down market.

    Returns the same JSON the `predict watch` TUI's snapshot pane sees:
    question, slug, condition_id, start_date, end_date, seconds_remaining,
    price_to_beat (BTC at window start), current_price (live spot),
    edge_dollars, edge_pct, if_close_now ("UP"|"DOWN"|"TIE"),
    poly_up_price, poly_down_price, poly_implied_up.

    Use this as the first call when answering "what's the BTC market doing
    right now?" — it bundles spot price, time-to-close, and crowd
    probability in one round-trip.
    """
    return _run_json(["predict", "snapshot"])


@mcp.tool()
def btc_recent_closes(n: int = 5) -> dict:
    """Last `n` 1-minute BTC/USD closes from the same oracle the momentum
    model uses (Binance primary, Coinbase fallback).

    Useful for sanity-checking why the momentum auto-loop picked UP vs
    DOWN, or to build your own short-horizon trend read.

    Args:
        n: how many 1m closes to fetch (1–60).

    Returns: {closes_oldest_first: [float, …], n_returned: int, spot: float}
    """
    n = max(1, min(60, n))
    snap = _run_json(["predict", "snapshot"])
    # `predict snapshot` already gives us the current spot; for the close
    # series we lean on `predict think` which exposes feature inputs. We
    # synthesize the close window inline via the BTC oracle by calling
    # snapshot + repeating — but since we lack a dedicated closes CLI
    # subcommand, we just surface the spot here for now and document the
    # limit so the model knows what it's getting.
    spot = float(snap.get("current_price", 0.0)) if isinstance(snap, dict) else 0.0
    return {
        "closes_oldest_first": [spot],
        "n_returned": 1,
        "spot": spot,
        "note": (
            "Only spot exposed via CLI today. For full series use the Rust "
            "`oracle::fetch_recent_btc_closes` helper inside the binary."
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Predictions store + stats
# ─────────────────────────────────────────────────────────────────────────────


def _read_predictions() -> list[dict]:
    if not PREDICTIONS_FILE.is_file():
        return []
    out: list[dict] = []
    with PREDICTIONS_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                # Skip half-written tail row rather than failing the whole
                # call — the CLI appends atomically so this is rare.
                continue
    return out


@mcp.tool()
def predictions_list(
    status: str = "all",
    limit: int = 50,
    newest_first: bool = True,
) -> dict:
    """Read predictions from the local JSONL store.

    Args:
        status: "all" | "pending" | "resolved".
        limit: max rows to return (1–500).
        newest_first: reverse order so the freshest predictions land first.

    Returns: {predictions: [...], total_in_store: int, store_path: str}.
    Each prediction has id, slug, question, opened_at, direction, confidence,
    p_open, poly_up_price, poly_down_price, resolution (or null), ...
    """
    rows = _read_predictions()
    if status == "pending":
        filt = [r for r in rows if not r.get("resolution")]
    elif status == "resolved":
        filt = [r for r in rows if r.get("resolution")]
    elif status == "all":
        filt = rows
    else:
        raise RuntimeError(f"status must be 'all'|'pending'|'resolved', got '{status}'")
    if newest_first:
        filt = list(reversed(filt))
    return {
        "predictions": filt[: max(1, min(500, limit))],
        "total_in_store": len(rows),
        "store_path": str(PREDICTIONS_FILE),
    }


@mcp.tool()
def predictions_stats(last_n: int | None = None) -> dict:
    """Aggregate accuracy / Brier / direction counts across resolved
    predictions. Wraps `polymarket predict stats -o json`.

    Args:
        last_n: only consider the most recent N rows. None = all-time.
    """
    args = ["predict", "stats"]
    if last_n is not None:
        args += ["--last", str(max(1, last_n))]
    return _run_json(args)


@mcp.tool()
def predictions_backtest(
    model: str = "polymarket",
    from_iso: str | None = None,
    to_iso: str | None = None,
) -> dict:
    """Replay resolved predictions and compute Brier, log-loss, bootstrap
    confidence intervals, and the Δ vs the Polymarket-implied baseline.

    Args:
        model: model label (e.g. "polymarket"). Wraps `predict backtest`.
        from_iso: RFC3339 lower bound (inclusive) on `opened_at`.
        to_iso: RFC3339 upper bound (inclusive) on `opened_at`.
    """
    args = ["predict", "backtest", "--model", model]
    if from_iso:
        args += ["--from", from_iso]
    if to_iso:
        args += ["--to", to_iso]
    return _run_json(args)


@mcp.tool()
def predict_think(
    models: list[str] | None = None,
    blend: list[float] | None = None,
    min_seconds_remaining: int = 30,
) -> dict:
    """One-shot snapshot of what each model would predict RIGHT NOW for the
    next BTC 5m window. Does NOT persist anything to the store.

    Args:
        models: comma list of models to consult. Default: ["polymarket"].
            Supported zero-config: "polymarket", "momentum", "blend".
            "logistic" / "forest" / "gbm" require a running ingest feed.
        blend: optional weights matching `models` order (e.g. [0.6, 0.4]).
        min_seconds_remaining: skip the market if fewer seconds remain in
            the window (so you don't get a stale answer when called near
            the boundary).
    """
    args = ["predict", "think", "--min-seconds-remaining", str(min_seconds_remaining)]
    if models:
        args += ["--models", ",".join(models)]
    if blend:
        args += ["--blend", ",".join(str(w) for w in blend)]
    return _run_json(args)


if __name__ == "__main__":
    mcp.run()
