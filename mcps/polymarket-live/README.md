# polymarket-live MCP

Source URL: (local — `soul/mcps/mcps/polymarket-live/server.py`)

Install command:

```sh
# uv handles deps via PEP 723 inline metadata in server.py — no install step needed
test -f ~/Documents/soul/mcps/mcps/polymarket-live/server.py
# also requires the polymarket-cli binary on disk:
test -x ~/Documents/polymarket-cli/target/release/polymarket
```

Expected command/type:

```text
command: ~/.local/bin/uv
args:
  - run
  - --quiet
  - --script
  - /home/deadpool/Documents/soul/mcps/mcps/polymarket-live/server.py
type: stdio
```

Required env vars:

```text
POLYMARKET_BIN              (optional) absolute path to a specific polymarket binary
POLYMARKET_REPO             (optional) repo root, default ~/Documents/polymarket-cli
POLYMARKET_PREDICTIONS_FILE (optional) JSONL store path, default ~/.config/polymarket/data/predictions.jsonl
POLYMARKET_MCP_TIMEOUT      (optional) per-call subprocess timeout in seconds, default 15
```

Related skills:

```text
polymarket-research
polymarket-predictions-audit
```

Quick health check:

```sh
timeout 5 ~/.local/bin/uv run --quiet --with "mcp>=1.0.0" \
  python3 -c "
import sys; sys.path.insert(0, '/home/deadpool/Documents/soul/mcps/mcps/polymarket-live')
from server import _resolve_bin
print('bin:', _resolve_bin())
"
```

## Tools exposed

| Tool | Purpose |
|---|---|
| `market_status` | Polymarket API health |
| `markets_list(limit, active_only)` | List active markets |
| `markets_get(id_or_slug)` | One market with outcomes + token IDs |
| `markets_search(query, limit)` | Free-text search |
| `clob_midpoint(token_id)` | Live midpoint price for one outcome |
| `clob_midpoints(token_ids)` | Batch midpoints |
| `clob_book(token_id)` | Full L2 order book |
| `btc_5m_snapshot()` | Active BTC 5m market: spot, price-to-beat, time-left, P(up) |
| `btc_recent_closes(n)` | Last N 1-min BTC closes (best-effort) |
| `predictions_list(status, limit, newest_first)` | Read local predictions.jsonl |
| `predictions_stats(last_n)` | Accuracy / Brier summary |
| `predictions_backtest(model, from_iso, to_iso)` | Brier + log-loss + calibration |
| `predict_think(models, blend, min_seconds_remaining)` | One-shot model forecast |

## What it is for

Lets Claude (Code or Desktop) see the same data the `predict watch` TUI
shows — without having to run any subprocess by hand, and without the
local-store-read / REST-call boilerplate. Typical asks:

- "What's the BTC 5m market doing right now?" → `btc_5m_snapshot()`
- "Why is the auto-loop picking UP?" → `predict_think(models=["momentum","polymarket","blend"])`
- "Show my recent prediction accuracy" → `predictions_stats()` then `predictions_list(status="resolved", limit=20)`
- "Look up the X election market book" → `markets_search("election")` → `markets_get(slug)` → `clob_book(token_id)`

## What it is NOT for

Everything in `polymarket-live` is read-only. Mutating actions — opening
a paper prediction, resolving, posting CLOB orders, the live `bot` lane —
are intentionally NOT wrapped. Run those by hand with the CLI:

```sh
polymarket predict open --model momentum
polymarket predict resolve
polymarket bot run …
```

Reason: keep the MCP boundary safe to call without a private key, and avoid
ambiguous "did Claude just place a real order?" failure modes.
