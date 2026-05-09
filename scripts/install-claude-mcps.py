#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "claude.mcp.json"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Install placeholder MCP blocks into Claude settings.json.")
    parser.add_argument("--target", default=str(Path.home() / ".claude" / "settings.json"))
    parser.add_argument("--dry-run", action="store_true", help="Print the rendered settings instead of writing.")
    args = parser.parse_args()

    target = Path(args.target).expanduser()
    existing = load_json(target)
    template = load_json(TEMPLATE)

    existing_servers = existing.get("mcpServers", {})
    template_servers = template.get("mcpServers", {})
    if not isinstance(existing_servers, dict):
        existing_servers = {}
    if not isinstance(template_servers, dict):
        raise SystemExit("template missing mcpServers object")

    existing["mcpServers"] = {**existing_servers, **template_servers}
    rendered = json.dumps(existing, indent=2, sort_keys=True) + "\n"

    if args.dry_run:
        print(rendered, end="")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.with_suffix(target.suffix + ".backup").write_text(
            json.dumps(load_json(target), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    target.write_text(rendered, encoding="utf-8")
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
