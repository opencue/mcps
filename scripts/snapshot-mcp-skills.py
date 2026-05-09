#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = ROOT.parent / "skills" / "skills"
RULES_PATH = ROOT / "configs" / "mcp-skill-rules.json"
CONFIGS_DIR = ROOT / "configs"
MCPS_DIR = ROOT / "mcps"
DOCS_DIR = ROOT / "docs"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def mcp_page_path(mcp_name: str) -> Path:
    if mcp_name.startswith("omx_"):
        return Path("mcps") / "omx" / slugify(mcp_name.removeprefix("omx_")) / "skills.md"
    return Path("mcps") / slugify(mcp_name) / "skills.md"


def display_path(value: Path | str) -> str:
    text = str(value)
    home = str(Path.home())
    if text == home:
        return "~"
    if text.startswith(home + "/"):
        return "~/" + text[len(home) + 1 :]
    return text


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def parse_skill(skill_dir: Path) -> dict[str, str]:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    description = ""
    name = skill_dir.name

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            lines = parts[1].splitlines()
            for index, line in enumerate(lines):
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip('"')
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip('"')
                    if description in {"|", ">-", ">"}:
                        block: list[str] = []
                        for follow in lines[index + 1 :]:
                            if follow and not follow.startswith((" ", "\t")):
                                break
                            stripped = follow.strip()
                            if stripped:
                                block.append(stripped)
                        description = " ".join(block)

    return {
        "name": name or skill_dir.name,
        "slug": skill_dir.name,
        "category": skill_dir.parent.name,
        "description": description,
        "path": str(skill_dir),
        "search_text": f"{skill_dir.name}\n{description}".lower(),
    }


def load_skills(skills_root: Path) -> dict[str, dict[str, str]]:
    skills: dict[str, dict[str, str]] = {}
    if not skills_root.exists():
        return skills
    for skill_md in sorted(skills_root.rglob("SKILL.md")):
        skill = parse_skill(skill_md.parent)
        existing = skills.get(skill["slug"])
        if existing is None or len(Path(skill["path"]).parts) < len(Path(existing["path"]).parts):
            skills[skill["slug"]] = skill
    return skills


def load_mcp_names() -> list[str]:
    names: set[str] = set()
    for path in sorted(CONFIGS_DIR.glob("*.sanitized.json")):
        data = load_json(path)
        servers = data.get("servers", {})
        if isinstance(servers, dict):
            names.update(servers.keys())
    return sorted(names, key=str.lower)


def match_skills(mcp_name: str, skills: dict[str, dict[str, str]], rules: dict[str, Any]) -> list[dict[str, str]]:
    rule = rules.get(mcp_name, {})
    include_skills = set(rule.get("include_skills", []))
    include_prefixes = tuple(rule.get("include_skill_prefixes", []))
    include_categories = set(rule.get("include_skill_categories", []))
    keywords = [str(k).lower() for k in rule.get("keywords", [])]
    keyword_match = bool(rule.get("keyword_match", False))

    matches: dict[str, str] = {}
    for slug, skill in skills.items():
        reason = ""
        if slug in include_skills:
            reason = "explicit"
        elif include_prefixes and slug.startswith(include_prefixes):
            reason = "prefix"
        elif skill["category"] in include_categories:
            reason = "category"
        elif keyword_match and any(keyword and keyword in skill["search_text"] for keyword in keywords):
            reason = "keyword"

        if reason:
            matches[slug] = reason

    return [
        {
            "slug": slug,
            "name": skills[slug]["name"],
            "category": skills[slug]["category"],
            "description": skills[slug]["description"],
            "reason": matches[slug],
        }
        for slug in sorted(matches)
    ]


def write_mcp_skill_page(mcp_name: str, matches: list[dict[str, str]], rule: dict[str, Any]) -> None:
    page_path = ROOT / mcp_page_path(mcp_name)
    page_path.parent.mkdir(parents=True, exist_ok=True)
    source_url = str(rule.get("source_url", "")).strip()
    homepage = str(rule.get("homepage", "")).strip()
    package = str(rule.get("package", "")).strip()
    install = str(rule.get("install", "")).strip()
    health_command = str(rule.get("health_command", "")).strip()
    expected_type = str(rule.get("expected_type", "")).strip()
    owners = rule.get("owners", [])
    agent_surfaces = rule.get("agent_surfaces", [])
    lines = [
        f"# {mcp_name} skills",
        "",
        "Related skills from the `recodeee/skills` registry.",
        "",
    ]
    if source_url:
        lines.extend([f"MCP source: [{source_url}]({source_url})", ""])
    if homepage:
        lines.extend([f"Homepage: [{homepage}]({homepage})", ""])
    if package:
        lines.extend([f"Package: `{package}`", ""])
    if install:
        lines.extend([f"Install: `{install}`", ""])
    if expected_type:
        lines.extend([f"Expected type: `{expected_type}`", ""])
    if health_command:
        lines.extend([f"Health command: `{health_command}`", ""])
    if owners:
        lines.extend(["Owners: " + ", ".join(f"`{owner}`" for owner in owners), ""])
    if agent_surfaces:
        lines.extend(["Agent surfaces: " + ", ".join(f"`{surface}`" for surface in agent_surfaces), ""])

    if not matches:
        lines.extend([
            "No related skills are mapped yet.",
            "",
            "Add rules in `configs/mcp-skill-rules.json`.",
            "",
        ])
    else:
        lines.append("| Skill | Category | Reason | Description |")
        lines.append("| --- | --- | --- | --- |")
        for item in matches:
            desc = item["description"].replace("|", "\\|")
            lines.append(f"| `{item['slug']}` | `{item['category']}` | {item['reason']} | {desc} |")
        lines.append("")

    page_path.write_text("\n".join(lines), encoding="utf-8")


def write_omx_index(mcp_names: list[str], mapping: dict[str, Any]) -> None:
    omx_names = [name for name in mcp_names if name.startswith("omx_")]
    if not omx_names:
        return

    lines = [
        "# OMX MCPs",
        "",
        "Top-level folder for OMX-related MCP servers.",
        "",
        "| MCP | Source | Related skills | Page |",
        "| --- | --- | ---: | --- |",
    ]
    for name in omx_names:
        skills = mapping["mcps"].get(name, {}).get("skills", [])
        source_url = mapping["mcps"].get(name, {}).get("source_url", "")
        source = f"[link]({source_url})" if source_url else "-"
        lines.append(f"| `{name}` | {source} | {len(skills)} | `{mcp_page_path(name).relative_to('mcps/omx')}` |")

    omx_dir = MCPS_DIR / "omx"
    omx_dir.mkdir(parents=True, exist_ok=True)
    (omx_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    skills_root = Path(__import__("os").environ.get("SKILLS_ROOT", DEFAULT_SKILLS_ROOT))
    skills = load_skills(skills_root)
    rules = load_json(RULES_PATH)
    mcp_names = load_mcp_names()

    MCPS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    mapping: dict[str, Any] = {
        "skills_root": display_path(skills_root),
        "mcp_count": len(mcp_names),
        "skill_count": len(skills),
        "mcps": {},
    }

    lines = [
        "# MCP Skill Map",
        "",
        "Generated by `scripts/snapshot-mcp-skills.py`.",
        "",
        f"Skills root: `{display_path(skills_root)}`",
        "",
        "| MCP | Source | Related skills | Page |",
        "| --- | --- | ---: | --- |",
    ]

    for mcp_name in mcp_names:
        matches = match_skills(mcp_name, skills, rules)
        rule = rules.get(mcp_name, {})
        write_mcp_skill_page(mcp_name, matches, rule)
        mapping["mcps"][mcp_name] = {
            "page": str(mcp_page_path(mcp_name)),
            "source_url": str(rule.get("source_url", "")).strip(),
            "homepage": str(rule.get("homepage", "")).strip(),
            "package": str(rule.get("package", "")).strip(),
            "install": str(rule.get("install", "")).strip(),
            "health_command": str(rule.get("health_command", "")).strip(),
            "owners": rule.get("owners", []),
            "agent_surfaces": rule.get("agent_surfaces", []),
            "skills": matches,
        }
        source_url = str(rule.get("source_url", "")).strip()
        source = f"[link]({source_url})" if source_url else "-"
        lines.append(f"| `{mcp_name}` | {source} | {len(matches)} | `{mcp_page_path(mcp_name)}` |")

    write_omx_index(mcp_names, mapping)

    (CONFIGS_DIR / "mcp-skill-map.json").write_text(
        json.dumps(mapping, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (DOCS_DIR / "mcp-skill-map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"mapped {len(mcp_names)} MCPs to skills from {skills_root}")


if __name__ == "__main__":
    main()
