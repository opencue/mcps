# soul MCP

Source URL: (local — no remote MCP server; skill-driven workflow)

Install command:

```sh
# No install — the soul workflow is delivered as a SKILL.md, not a server.
# Skill is automatically symlinked from soul/skills/skills/meta/soul/
# into ~/.claude/skills/soul and ~/.codex/skills/soul on the next sync fire.
ls ~/Documents/soul/skills/skills/meta/soul/SKILL.md
```

Expected command/type:

```text
command: (none)
args: (none)
type: skill-only
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
test -L "$HOME/.claude/skills/soul" && echo OK || echo "not symlinked yet — wait for next sync or run install-local.sh"
```

## What this is

Catalog stub for the `soul` skill workflow. Unlike other entries in this
folder (`colony`, `coolify`, `obsidian-vault`, etc.) the soul workflow is
**not a running MCP server** — it's a skill that Claude follows when the
user wants to create a new skill or MCP catalog entry under `soul/`.

The skill knows:

- The `soul/skills/skills/<category>/<name>/SKILL.md` path layout
- The 16-category taxonomy (caveman, colony, content, deployment, design,
  github, higgsfield, hostinger, medusa, meta, obsidian, orchestration,
  private, research, review, stripe)
- The canonical SKILL.md frontmatter shape
- The MCP catalog README.md template (this very file's shape)
- That `install-local.sh` is fired automatically by the systemd timer +
  Stop hook — the user never has to manually symlink anything

## When the user wants a real MCP server here

If you later add a real soul-skills MCP server (one that exposes
`soul_skill_create` etc. as MCP tools so Claude can call them
programmatically), update this README to match the convention used by
`colony/README.md` — fill in the source URL, install command, real
command/args/type, env vars, and a meaningful health check. Then add the
server to `~/.claude.json` with `claude mcp add soul-skills ...`. The
sync timer will propagate it into Claude Desktop's
`claude_desktop_config.json` automatically.
