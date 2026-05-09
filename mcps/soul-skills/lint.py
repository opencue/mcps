#!/usr/bin/env -S uv run -q --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Soul Skills linter.

Walks ~/Documents/soul/skills/skills/<category>/<name>/SKILL.md and reports:
  ERROR — frontmatter missing/malformed, name<>dir mismatch, cross-category collision
  WARN  — description too short/long, missing "Use when user says" opener,
          fewer than 3 quoted trigger phrases, body has no markdown heading,
          dir without SKILL.md

Imported by server.py (the soul_lint MCP tool) and run standalone for the
soul-lint shell wrapper. Stdlib only — no third-party deps.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SOUL = Path.home() / "Documents" / "soul"
SKILLS_ROOT = SOUL / "skills" / "skills"


def parse_frontmatter(text: str) -> dict[str, str]:
    """Minimal YAML frontmatter parser.

    Handles only the shapes soul SKILL.md files actually use:
      name: value
      description: >-
        multi-line value
        more lines
    """
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    out: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []
    multiline = False

    def flush() -> None:
        nonlocal current_key, current_lines, multiline
        if current_key is None:
            return
        if multiline:
            out[current_key] = " ".join(s.strip() for s in current_lines if s.strip())
        elif current_lines:
            out[current_key] = current_lines[0]
        else:
            out[current_key] = ""
        current_key = None
        current_lines = []
        multiline = False

    for raw in m.group(1).splitlines():
        if not raw.strip():
            continue
        # top-level key starts at column 0
        key_match = re.match(r"^([a-z_][a-z0-9_-]*?):\s*(.*)$", raw)
        if key_match and not raw.startswith((" ", "\t")):
            flush()
            current_key = key_match.group(1)
            value = key_match.group(2).strip()
            if value in (">-", ">", "|", "|-"):
                multiline = True
            else:
                current_lines = [value]
        elif current_key:
            current_lines.append(raw)
    flush()
    return out


def lint_all() -> dict:
    """Walk soul/skills and return findings as structured JSON."""
    issues: list[dict] = []
    name_to_paths: dict[str, list[Path]] = {}
    checked = 0

    if not SKILLS_ROOT.is_dir():
        return {"checked": 0, "error_count": 0, "warning_count": 0, "errors": [], "warnings": []}

    for cat_dir in sorted(SKILLS_ROOT.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            skill_md = skill_dir / "SKILL.md"
            rel = f"{cat_dir.name}/{skill_dir.name}"
            if not skill_md.exists():
                issues.append({"level": "warn", "path": rel, "issue": "directory has no SKILL.md"})
                continue
            checked += 1
            text = skill_md.read_text(errors="replace")
            fm = parse_frontmatter(text)

            if "name" not in fm:
                issues.append({"level": "error", "path": rel, "issue": "missing `name` in frontmatter"})
            elif fm["name"] != skill_dir.name:
                issues.append({
                    "level": "error", "path": rel,
                    "issue": f"frontmatter name '{fm['name']}' != dir name '{skill_dir.name}'",
                })

            desc = fm.get("description", "").strip()
            if not desc:
                issues.append({"level": "error", "path": rel, "issue": "missing `description` in frontmatter"})
            else:
                if len(desc) < 80:
                    issues.append({"level": "warn", "path": rel, "issue": f"description very short ({len(desc)} chars; recommend 80+)"})
                if len(desc) > 400:
                    issues.append({"level": "warn", "path": rel, "issue": f"description over 400 chars ({len(desc)}); harness will truncate"})
                if "Use when" not in desc and "TRIGGER when" not in desc and "Triggers on" not in desc:
                    issues.append({"level": "warn", "path": rel, "issue": "description has no 'Use when' / 'TRIGGER when' opener — matching may degrade"})
                quoted = re.findall(r'"[^"]+"|\'[^\']+\'', desc)
                if len(quoted) < 2:
                    issues.append({"level": "warn", "path": rel, "issue": f"only {len(quoted)} quoted trigger phrases; recommend 3+"})

            # Body has at least one heading
            body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)
            if not re.search(r"(?m)^#\s", body):
                issues.append({"level": "warn", "path": rel, "issue": "body has no markdown heading"})

            # Track for cross-category dup check
            name_to_paths.setdefault(skill_dir.name, []).append(skill_md)

    for skill_name, paths in name_to_paths.items():
        if len(paths) > 1:
            issues.append({
                "level": "error",
                "path": skill_name,
                "issue": f"duplicate name across {len(paths)} categories: {[str(p.parent.parent.name) for p in paths]}",
            })

    errors = [i for i in issues if i["level"] == "error"]
    warnings = [i for i in issues if i["level"] == "warn"]
    return {
        "checked": checked,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


if __name__ == "__main__":
    result = lint_all()
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    sys.exit(1 if result["error_count"] > 0 else 0)
