#!/usr/bin/env -S uv run -q --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.0.0"]
# ///
"""Soul Skills MCP server.

Exposes 7 stdio MCP tools for managing skills + MCP catalog entries under
~/Documents/soul/. Lets Claude (Code or Desktop) introspect the soul taxonomy
and create new entries programmatically without going through a markdown
skill loop.

Tools:
    soul_categories         — list known skill categories
    soul_skill_list         — list skills (optionally filtered by category)
    soul_skill_get          — fetch one skill's frontmatter + body
    soul_skill_create       — write a new SKILL.md under <category>/<name>/
    soul_mcp_list           — list MCP catalog entries
    soul_mcp_create         — write a new MCP catalog README.md
    soul_lint               — run the SKILL.md linter and return findings

Run: uv run ~/Documents/soul/mcps/mcps/soul-skills/server.py
Register in ~/.claude.json mcpServers as `soul-skills`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Allow importing lint.py from same dir
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lint import lint_all, parse_frontmatter  # type: ignore

from mcp.server.fastmcp import FastMCP

SOUL = Path.home() / "Documents" / "soul"
SKILLS_ROOT = SOUL / "skills" / "skills"
MCPS_ROOT = SOUL / "mcps" / "mcps"

KEBAB_RE = re.compile(r"^[a-z][a-z0-9-]*[a-z0-9]$|^[a-z]$")

mcp = FastMCP("soul-skills")


def _categories() -> list[str]:
    if not SKILLS_ROOT.is_dir():
        return []
    return sorted(
        p.name for p in SKILLS_ROOT.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )


@mcp.tool()
def soul_categories() -> list[str]:
    """Return the list of skill categories under soul/skills/skills/.

    Stable taxonomy (don't add ad-hoc categories — ask the user first).
    """
    return _categories()


@mcp.tool()
def soul_skill_list(category: str | None = None) -> list[dict]:
    """List skills under soul/skills/skills/. Filter by category if provided.

    Returns: [{ name, category, path, description (≤200 chars) }]
    """
    out: list[dict] = []
    if not SKILLS_ROOT.is_dir():
        return out
    cat_dirs = (
        [SKILLS_ROOT / category] if category
        else [p for p in SKILLS_ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")]
    )
    for cat_dir in cat_dirs:
        if not cat_dir.is_dir():
            continue
        for skill_dir in cat_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            fm = parse_frontmatter(skill_md.read_text(errors="replace"))
            out.append({
                "name": skill_dir.name,
                "category": cat_dir.name,
                "path": str(skill_md),
                "description": (fm.get("description", "") or "")[:200],
            })
    return sorted(out, key=lambda x: (x["category"], x["name"]))


@mcp.tool()
def soul_skill_get(name: str) -> dict:
    """Fetch one skill's full frontmatter + body. Searches all categories."""
    if not SKILLS_ROOT.is_dir():
        return {"error": "soul/skills/skills/ not found"}
    for cat_dir in SKILLS_ROOT.iterdir():
        if not cat_dir.is_dir():
            continue
        skill_md = cat_dir / name / "SKILL.md"
        if skill_md.exists():
            text = skill_md.read_text(errors="replace")
            fm = parse_frontmatter(text)
            body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL).strip()
            return {
                "name": name,
                "category": cat_dir.name,
                "path": str(skill_md),
                "frontmatter": fm,
                "body": body,
            }
    return {"error": f"skill '{name}' not found in any category"}


@mcp.tool()
def soul_skill_create(
    name: str,
    category: str,
    description: str,
    body: str,
) -> dict:
    """Create a new skill at soul/skills/skills/<category>/<name>/SKILL.md.

    Args:
        name: kebab-case (a-z0-9-), ≤30 chars. Must equal the directory name.
        category: must be one of soul_categories(). New categories are
                  refused — call soul_categories() first to see options.
        description: skill listing match string. Should start with
                     "Use when user says ..." and include 3+ quoted trigger
                     phrases. 80–400 chars recommended.
        body: markdown body without frontmatter delimiters. Should have at
              least one H2-level heading (## ...).

    Returns: { ok, path, name, category, warnings, next } on success;
             { error } on collision or validation failure.
    """
    if not KEBAB_RE.match(name):
        return {"error": f"name must be kebab-case (a-z, 0-9, -); got '{name}'"}
    if len(name) > 30:
        return {"error": f"name too long ({len(name)} > 30 chars)"}

    cats = _categories()
    if category not in cats:
        return {
            "error": f"unknown category '{category}'",
            "existing_categories": cats,
            "hint": "Pick from existing — don't invent new categories without asking the user.",
        }

    skill_dir = SKILLS_ROOT / category / name
    skill_md = skill_dir / "SKILL.md"

    if skill_md.exists():
        return {"error": f"skill already exists at {skill_md}"}

    # Cross-category collision check
    for other_cat in SKILLS_ROOT.iterdir():
        if not other_cat.is_dir() or other_cat.name == category:
            continue
        if (other_cat / name / "SKILL.md").exists():
            return {
                "error": f"skill name '{name}' already exists in category '{other_cat.name}'",
                "hint": "Skill names are unique across the whole tree. Pick a different name or update the existing one.",
            }

    warnings: list[str] = []
    desc = description.strip()
    if len(desc) < 80:
        warnings.append(f"description very short ({len(desc)} chars; recommend 80+)")
    if len(desc) > 400:
        warnings.append(f"description over 400 chars ({len(desc)}); harness will truncate")
    if "Use when" not in desc and "TRIGGER when" not in desc and "Triggers on" not in desc:
        warnings.append("description has no 'Use when' / 'TRIGGER when' opener — matching may degrade")
    quoted = re.findall(r'"[^"]+"|\'[^\']+\'', desc)
    if len(quoted) < 2:
        warnings.append(f"only {len(quoted)} quoted trigger phrases; recommend 3+")

    skill_dir.mkdir(parents=True, exist_ok=True)
    fm_block = f"---\nname: {name}\ndescription: >-\n  {desc}\n---\n\n"
    skill_md.write_text(fm_block + body.rstrip() + "\n")

    return {
        "ok": True,
        "path": str(skill_md),
        "name": name,
        "category": category,
        "warnings": warnings,
        "next": "Skill is auto-symlinked into ~/.claude/skills and ~/.codex/skills by sync-all.sh (≤15 min via systemd timer, or end of next Claude Code turn). To force immediate install: ~/Documents/soul/skills/scripts/install-local.sh",
    }


@mcp.tool()
def soul_mcp_list() -> list[dict]:
    """List MCP catalog entries under soul/mcps/mcps/.

    Returns: [{ name, path, has_readme, has_skills_md }]
    """
    out: list[dict] = []
    if not MCPS_ROOT.is_dir():
        return out
    for mcp_dir in MCPS_ROOT.iterdir():
        if not mcp_dir.is_dir() or mcp_dir.name.startswith("."):
            continue
        readme = mcp_dir / "README.md"
        out.append({
            "name": mcp_dir.name,
            "path": str(readme if readme.exists() else mcp_dir),
            "has_readme": readme.exists(),
            "has_skills_md": (mcp_dir / "skills.md").exists(),
        })
    return sorted(out, key=lambda x: x["name"])


@mcp.tool()
def soul_mcp_create(
    name: str,
    source_url: str,
    install_command: str,
    command: str,
    args: list[str] | None = None,
    server_type: str = "stdio",
    env_vars: list[str] | None = None,
    related_skills: list[str] | None = None,
    health_check: str = "",
) -> dict:
    """Create a new MCP catalog entry at soul/mcps/mcps/<name>/README.md.

    Args:
        name: kebab-case identifier matching the eventual mcpServers key.
        source_url: GitHub/npm/upstream URL. Use "(local)" if no remote.
        install_command: one-liner shell command users would run to install.
        command: the binary or runtime invoked (e.g. "node", "bash", "npx").
        args: argv list. Empty list/None for none.
        server_type: "stdio" | "http" | "sse" | "skill-only". Default stdio.
        env_vars: required env var names. Names only, no values.
        related_skills: skill names that pair with this MCP.
        health_check: one-liner that verifies the binary is installed.
    """
    if not KEBAB_RE.match(name):
        return {"error": f"name must be kebab-case; got '{name}'"}

    args = args or []
    env_vars = env_vars or []
    related_skills = related_skills or []

    mcp_dir = MCPS_ROOT / name
    readme = mcp_dir / "README.md"
    if readme.exists():
        return {"error": f"MCP catalog entry already exists at {readme}"}

    args_block = "\n".join(f"  - {a}" for a in args) if args else "  (none)"
    env_block = "\n".join(env_vars) if env_vars else "(none)"
    skills_block = "\n".join(related_skills) if related_skills else "(none)"
    health = health_check or f"command -v {command}"

    content = (
        f"# {name} MCP\n\n"
        f"Source URL: {source_url}\n\n"
        f"Install command:\n\n"
        f"```sh\n{install_command}\n```\n\n"
        f"Expected command/type:\n\n"
        f"```text\ncommand: {command}\nargs:\n{args_block}\ntype: {server_type}\n```\n\n"
        f"Required env vars:\n\n"
        f"```text\n{env_block}\n```\n\n"
        f"Related skills:\n\n"
        f"```text\n{skills_block}\n```\n\n"
        f"Quick health check:\n\n"
        f"```sh\n{health}\n```\n"
    )

    mcp_dir.mkdir(parents=True, exist_ok=True)
    readme.write_text(content)

    return {
        "ok": True,
        "path": str(readme),
        "name": name,
        "next": "Catalog entry written. Register the actual server in ~/.claude.json (e.g. `claude mcp add ...`) — sync-claude-desktop-mcps.sh propagates to Claude Desktop on the next sync.",
    }


@mcp.tool()
def soul_lint() -> dict:
    """Run the soul SKILL.md linter across the whole tree.

    Reports frontmatter errors, description quality warnings, and cross-
    category name collisions. Returns: { checked, error_count,
    warning_count, errors: [...], warnings: [...] }
    """
    return lint_all()


if __name__ == "__main__":
    mcp.run()
