# soul-skills MCP

Source URL: (local — `soul/mcps/mcps/soul-skills/server.py`)

Install command:

```sh
# uv handles deps via PEP 723 inline metadata in server.py — no install step needed
test -f /home/deadpool/Documents/soul/mcps/mcps/soul-skills/server.py
```

Expected command/type:

```text
command: /home/deadpool/.local/bin/uv
args:
  - run
  - --quiet
  - --script
  - /home/deadpool/Documents/soul/mcps/mcps/soul-skills/server.py
type: stdio
```

Required env vars:

```text
(none)
```

Related skills:

```text
soul
skill
plugin-creator
doctor
```

Quick health check:

```sh
timeout 3 /home/deadpool/.local/bin/uv run --quiet --with "mcp>=1.0.0" python3 -c "import sys; sys.path.insert(0, '/home/deadpool/Documents/soul/mcps/mcps/soul-skills'); from server import mcp; print('ok')"
```

## Tools exposed

| Tool | Purpose |
|---|---|
| `soul_categories` | List the 16 skill categories |
| `soul_skill_list(category=None)` | List skills, optionally filtered |
| `soul_skill_get(name)` | Fetch one skill's frontmatter + body |
| `soul_skill_create(name, category, description, body)` | Write a new SKILL.md with collision check |
| `soul_mcp_list` | List MCP catalog entries |
| `soul_mcp_create(name, source_url, install_command, command, args=[], server_type="stdio", env_vars=[], related_skills=[], health_check="")` | Write a new MCP catalog README.md |
| `soul_lint` | Run the SKILL.md linter, return JSON findings |

## Why a real server (not just the `soul` skill)

The `soul` skill (markdown at `soul/skills/skills/meta/soul/SKILL.md`) walks Claude through creating a skill conversationally — multi-turn, with the model writing the file via Write tool. That's fine for ad-hoc use.

This MCP server lets Claude (Code or Desktop) **call the create function as a tool** with all params at once. One round-trip. Catches collisions before writing. Returns the path. Reports description-quality warnings inline. Useful when:

- Another skill or agent needs to create soul entries programmatically
- You want batch creation (e.g. scaffold 5 related skills in one turn)
- You want introspection without scrolling: `soul_categories()`, `soul_skill_list(category="medusa")` etc.

The skill and the server complement each other; the skill defers to the server's `soul_skill_create` tool when available.

## Registration

Lives in `~/.claude.json` `mcpServers.soul-skills`:

```json
{
  "command": "/home/deadpool/.local/bin/uv",
  "args": ["run", "--quiet", "--script", "/home/deadpool/Documents/soul/mcps/mcps/soul-skills/server.py"]
}
```

The `sync-claude-desktop-mcps.sh` script propagates this entry into Claude Desktop's `claude_desktop_config.json` automatically on the next sync (≤15 min via `soul-sync.timer`, or end of next Claude Code turn).

## Lint hook

The same `lint.py` module is used standalone by `soul/skills/scripts/soul-lint.sh` (called from `sync-all.sh` in `--quiet` mode every sync). When the linter finds errors, they surface in the sync log (`~/.cache/soul-sync.log`).
