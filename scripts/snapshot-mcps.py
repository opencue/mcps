#!/usr/bin/env python3
from __future__ import annotations

import json
import re
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # back-port for 3.8–3.10
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIGS = ROOT / "configs"
DOCS = ROOT / "docs"

SOURCES = [
    ("codex", Path.home() / ".codex" / "config.toml", "mcp_servers"),
    ("claude", Path.home() / ".claude" / "settings.json", "mcpServers"),
    ("claude_runtime", Path.home() / ".claude.json", "mcpServers"),
    ("vscode", Path.home() / ".config" / "Code" / "User" / "mcp.json", "servers"),
]

CLAUDE_RUNTIME_PROJECTS_PATH = Path.home() / ".claude.json"
CLAUDE_SETTINGS_PATH = Path.home() / ".claude" / "settings.json"
PLUGINS_CACHE = Path.home() / ".claude" / "plugins" / "cache"
PLUGINS_DIR = ROOT / "plugins"

SECRET_KEY_RE = re.compile(r"(secret|token|password|passwd|api[_-]?key|access[_-]?key|private[_-]?key|client[_-]?secret|consumer[_-]?secret|authorization|bearer)", re.I)
SECRET_VALUE_RE = re.compile(r"^(sk-|pk_|ghp_|github_pat_|xox[baprs]-|ck_|cs_|eyJ|AKIA|ASIA)")
URL_SECRET_RE = re.compile(r"([?&](?:key|token|secret|password|consumer_key|consumer_secret)=)[^&\s]+", re.I)


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".toml":
        return tomllib.loads(text)
    return json.loads(text)


def redact_string(value: str) -> str:
    value = URL_SECRET_RE.sub(r"\1<redacted>", value)
    if SECRET_VALUE_RE.search(value):
        return "<redacted>"
    return display_path(value)


def display_path(value: Path | str) -> str:
    text = str(value)
    home = str(Path.home())
    if text == home:
        return "~"
    if text.startswith(home + "/"):
        return "~/" + text[len(home) + 1 :]
    return text


def sanitize(value: Any, key: str = "") -> Any:
    if SECRET_KEY_RE.search(key):
        if isinstance(value, dict):
            return {k: "<redacted>" for k in value.keys()}
        if isinstance(value, list):
            return ["<redacted>" for _ in value]
        return "<redacted>"

    if key == "env" and isinstance(value, dict):
        return {k: "<redacted>" for k in sorted(value.keys())}

    if isinstance(value, dict):
        return {k: sanitize(v, k) for k, v in sorted(value.items())}
    if isinstance(value, list):
        return [sanitize(v, key) for v in value]
    if isinstance(value, str):
        if key == "args" and SECRET_KEY_RE.search(value):
            return "<redacted secret-loading argument>"
        return redact_string(value)
    return value


def server_summary(name: str, cfg: dict[str, Any]) -> dict[str, Any]:
    command = cfg.get("command") or cfg.get("type") or cfg.get("url") or ""
    args = cfg.get("args") if isinstance(cfg.get("args"), list) else []
    env = cfg.get("env") if isinstance(cfg.get("env"), dict) else {}
    return {
        "name": name,
        "command_or_type": sanitize(command),
        "arg_count": len(args),
        "env_keys": sorted(env.keys()),
    }


def main() -> None:
    CONFIGS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    inventory: list[tuple[str, Path, str, list[dict[str, Any]]]] = []

    for source, path, key in SOURCES:
        data = load_config(path)
        servers = data.get(key, {}) if isinstance(data, dict) else {}
        if not isinstance(servers, dict):
            servers = {}

        sanitized = {
            "source": source,
            "source_path": display_path(path),
            "server_key": key,
            "servers": sanitize(servers),
        }
        (CONFIGS / f"{source}.sanitized.json").write_text(
            json.dumps(sanitized, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        summaries = [server_summary(name, cfg if isinstance(cfg, dict) else {}) for name, cfg in sorted(servers.items())]
        inventory.append((source, path, key, summaries))

    project_inventory: list[tuple[str, list[dict[str, Any]]]] = []
    runtime_data = load_config(CLAUDE_RUNTIME_PROJECTS_PATH)
    projects = runtime_data.get("projects", {}) if isinstance(runtime_data, dict) else {}
    if isinstance(projects, dict):
        per_project_sanitized: dict[str, Any] = {}
        for project_path, project_cfg in sorted(projects.items()):
            if not isinstance(project_cfg, dict):
                continue
            servers = project_cfg.get("mcpServers", {})
            if not isinstance(servers, dict) or not servers:
                continue
            display = display_path(project_path)
            per_project_sanitized[display] = sanitize(servers)
            project_inventory.append((display, [server_summary(n, c if isinstance(c, dict) else {}) for n, c in sorted(servers.items())]))
        if per_project_sanitized:
            (CONFIGS / "claude_runtime.projects.sanitized.json").write_text(
                json.dumps({
                    "source": "claude_runtime_projects",
                    "source_path": display_path(CLAUDE_RUNTIME_PROJECTS_PATH),
                    "server_key": "projects[*].mcpServers",
                    "projects": per_project_sanitized,
                }, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

    lines = ["# MCP Inventory", "", "Generated by `scripts/snapshot-mcps.py`.", ""]
    for source, path, key, summaries in inventory:
        lines.extend([f"## {source}", "", f"Source: `{display_path(path)}`", f"Server key: `{key}`", ""])
        if not summaries:
            lines.extend(["No MCP servers found.", ""])
            continue
        lines.append("| Server | Command/type | Args | Env keys |")
        lines.append("| --- | --- | ---: | --- |")
        for item in summaries:
            env_keys = ", ".join(f"`{k}`" for k in item["env_keys"]) or "-"
            lines.append(f"| `{item['name']}` | `{item['command_or_type']}` | {item['arg_count']} | {env_keys} |")
        lines.append("")

    if project_inventory:
        lines.extend(["## claude_runtime per-project", "", f"Source: `{display_path(CLAUDE_RUNTIME_PROJECTS_PATH)}` (`projects[*].mcpServers`)", ""])
        for project_display, summaries in project_inventory:
            lines.extend([f"### `{project_display}`", "", "| Server | Command/type | Args | Env keys |", "| --- | --- | ---: | --- |"])
            for item in summaries:
                env_keys = ", ".join(f"`{k}`" for k in item["env_keys"]) or "-"
                lines.append(f"| `{item['name']}` | `{item['command_or_type']}` | {item['arg_count']} | {env_keys} |")
            lines.append("")

    plugin_inventory = snapshot_plugins()
    if plugin_inventory:
        marketplaces, plugins_data = plugin_inventory
        PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
        (PLUGINS_DIR / "plugins.sanitized.json").write_text(
            json.dumps({
                "source": "claude_plugins",
                "source_paths": [
                    display_path(CLAUDE_SETTINGS_PATH) + "#enabledPlugins",
                    display_path(CLAUDE_SETTINGS_PATH) + "#extraKnownMarketplaces",
                    display_path(PLUGINS_CACHE) + "/<marketplace>/<plugin>/<version>/",
                ],
                "marketplaces": marketplaces,
                "plugins": plugins_data,
            }, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        lines.extend(["## plugins", "", f"Sources: `{display_path(CLAUDE_SETTINGS_PATH)}` (enabled set + marketplaces) + `{display_path(PLUGINS_CACHE)}` (latest cached version's manifest)", "",
                     "| Plugin | Marketplace | Version | Enabled | MCP servers |",
                     "| --- | --- | --- | :---: | --- |"])
        for plugin_id, info in sorted(plugins_data.items()):
            servers = info.get("mcpServers") or {}
            server_str = ", ".join(f"`{s}`" for s in sorted(servers.keys())) or "-"
            enabled_mark = "✓" if info.get("enabled") else "·"
            lines.append(f"| `{info['name']}` | `{info['marketplace']}` | `{info.get('version', '?')}` | {enabled_mark} | {server_str} |")
        lines.append("")

    (DOCS / "inventory.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote configs and docs/inventory.md")


def snapshot_plugins() -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Snapshot enabled plugins + their declared MCP servers from cached manifests.

    Returns (marketplaces, plugins) where plugins is keyed by `<plugin>@<marketplace>`.
    Reads the LATEST cached version of each plugin so updates flow through naturally.
    """
    if not CLAUDE_SETTINGS_PATH.exists():
        return None
    settings = load_config(CLAUDE_SETTINGS_PATH)
    if not isinstance(settings, dict):
        return None

    enabled = settings.get("enabledPlugins") or {}
    marketplaces_raw = settings.get("extraKnownMarketplaces") or {}
    marketplaces = sanitize(marketplaces_raw) if isinstance(marketplaces_raw, dict) else {}

    plugins: dict[str, Any] = {}
    if isinstance(enabled, dict):
        for plugin_id, is_enabled in sorted(enabled.items()):
            if "@" in plugin_id:
                plugin_name, marketplace = plugin_id.rsplit("@", 1)
            else:
                plugin_name, marketplace = plugin_id, "builtin"
            entry: dict[str, Any] = {
                "name": plugin_name,
                "marketplace": marketplace,
                "enabled": bool(is_enabled),
            }
            version_dir, manifest_servers = _read_plugin_manifest(marketplace, plugin_name)
            if version_dir is not None:
                entry["version"] = version_dir
            if manifest_servers is not None:
                entry["mcpServers"] = sanitize(manifest_servers)
            plugins[plugin_id] = entry

    return marketplaces, plugins


def _read_plugin_manifest(marketplace: str, plugin: str) -> tuple[str | None, dict[str, Any] | None]:
    plugin_root = PLUGINS_CACHE / marketplace / plugin
    if not plugin_root.is_dir():
        return None, None
    version_dirs = sorted(
        (p for p in plugin_root.iterdir() if p.is_dir()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not version_dirs:
        return None, None
    latest = version_dirs[0]
    version = latest.name

    mcp_inline = latest / ".mcp.json"
    if mcp_inline.exists():
        data = load_config(mcp_inline)
        servers = data.get("mcpServers") if isinstance(data, dict) else None
        return version, servers if isinstance(servers, dict) else {}

    plugin_manifest = latest / ".claude-plugin" / "plugin.json"
    if plugin_manifest.exists():
        data = load_config(plugin_manifest)
        if isinstance(data, dict):
            ref = data.get("mcpServers")
            if isinstance(ref, str):
                ref_path = (latest / ref).resolve()
                if ref_path.exists():
                    inline = load_config(ref_path)
                    servers = inline.get("mcpServers") if isinstance(inline, dict) else None
                    return version, servers if isinstance(servers, dict) else {}
            elif isinstance(ref, dict):
                return version, ref
        return version, {}

    return version, None


if __name__ == "__main__":
    main()
