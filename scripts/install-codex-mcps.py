#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "codex.mcp.toml"
START = "# >>> soul-mcps managed block >>>"
END = "# <<< soul-mcps managed block <<<"


def replace_block(existing: str, block: str) -> str:
    managed = f"{START}\n{block.rstrip()}\n{END}\n"
    if START in existing and END in existing:
        before = existing.split(START, 1)[0].rstrip()
        after = existing.split(END, 1)[1].lstrip()
        return "\n\n".join(part for part in [before, managed.rstrip(), after.rstrip()] if part) + "\n"
    return existing.rstrip() + "\n\n" + managed if existing.strip() else managed


def main() -> None:
    parser = argparse.ArgumentParser(description="Install placeholder MCP blocks into Codex config.toml.")
    parser.add_argument("--target", default=str(Path.home() / ".codex" / "config.toml"))
    parser.add_argument("--dry-run", action="store_true", help="Print the rendered config instead of writing.")
    args = parser.parse_args()

    target = Path(args.target).expanduser()
    template = TEMPLATE.read_text(encoding="utf-8")
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    rendered = replace_block(existing, template)

    if args.dry_run:
        print(rendered, end="")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.with_suffix(target.suffix + ".backup").write_text(existing, encoding="utf-8")
    target.write_text(rendered, encoding="utf-8")
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
