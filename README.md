```
   ┌───────────────────────────────────────────────────────────────┐
   │                                                               │
   │     r e c o d e e e  /  m c p s                               │
   │     ───────────────────────────                               │
   │     13 MCP servers · linked skills · sanitized configs        │
   │                                                               │
   └───────────────────────────────────────────────────────────────┘
```

> **My laptop's MCP registry.** This repo tracks the MCP servers used by
> Codex, Claude, and VS Code without committing raw settings or credentials.
> It also maps each MCP to the skills that depend on it.

---

## Why this exists

MCP config drifts even faster than skills: one agent has a server enabled,
another points at a local binary, VS Code has a separate entry, and the source
repo link gets forgotten. This repo is the audit layer.

It records:

- which MCP servers are configured
- where they come from
- which commands or hosted endpoints launch them
- which environment variable names they expect
- which agent skills are related to each server

It does **not** try to be the live secret store. Tokens stay in local config,
environment variables, password managers, or service-specific credential files.

---

## Layout

```text
configs/
  codex.sanitized.json      # ~/.codex/config.toml MCP block, redacted
  claude.sanitized.json     # ~/.claude/settings.json MCP block, redacted
  vscode.sanitized.json     # VS Code mcp.json, redacted
  mcp-skill-rules.json      # explicit source links and skill matching rules
  mcp-skill-map.json        # generated machine-readable MCP -> skills map
docs/
  health.md                 # generated local health summary
  inventory.md              # generated human inventory
  mcp-skill-map.md          # generated human MCP -> skills map
mcps/
  <mcp-name>/README.md      # per-MCP install and health notes
  <mcp-name>/skills.md      # per-MCP related skills and source link
  omx/                      # OMX MCP family grouped under one tree
scripts/
  check-no-secrets.sh       # fail if tracked docs/configs leak secret-shaped data
  check-mcp-health.py       # generate docs/health.md without network checks
  refresh-all.sh            # snapshot configs, map skills, health, scan, diff
  install-codex-mcps.py     # install placeholder MCP blocks into Codex config
  install-claude-mcps.py    # install placeholder MCP blocks into Claude settings
  snapshot-mcps.py          # refresh sanitized MCP config inventory
  snapshot-mcp-skills.py    # refresh MCP -> skills pages from recodeee/skills
templates/
  codex.mcp.toml            # placeholder-only Codex MCP config block
  claude.mcp.json           # placeholder-only Claude MCP config block
```

---

## MCP Inventory

| MCP | Source | Runtime surface |
| --- | --- | --- |
| `Higgsfield` | `https://mcp.higgsfield.ai/mcp` | hosted MCP endpoint |
| `MedusaDocs` | `https://docs.medusajs.com/mcp` | hosted docs MCP endpoint |
| `colony` | `https://github.com/recodeee/colony` | local CLI MCP |
| `coolify` | `https://github.com/StuMason/coolify-mcp` | local npm MCP |
| `gitea` | `https://github.com/seepine/gitea-mcp` | local binary MCP |
| `hostinger-api` | `https://github.com/hostinger/api-mcp-server` | local npm MCP |
| `letsfg` | `https://github.com/LetsFG/LetsFG` | local npm MCP |
| `react-grab-mcp` | `https://www.npmjs.com/package/@react-grab/mcp` | npm MCP |
| `omx/*` | `https://github.com/NagyVikt/oh-my-codex` | local Node MCP family |

OMX servers are grouped under:

```text
mcps/omx/
  code-intel/
  memory/
  state/
  trace/
  wiki/
```

---

## Refresh

Refresh sanitized MCP config snapshots:

```sh
./scripts/snapshot-mcps.py
```

Refresh MCP-to-skill mapping from the sibling `recodeee/skills` checkout:

```sh
./scripts/snapshot-mcp-skills.py
```

Common full refresh:

```sh
./scripts/refresh-all.sh
```

Review diffs before pushing. If a secret appears, remove it before commit and
tighten the redaction script.

Install placeholder MCP blocks only after reviewing the templates:

```sh
./scripts/install-codex-mcps.py --dry-run
./scripts/install-claude-mcps.py --dry-run
```

The install scripts write placeholders, not secrets. Replace local paths and
load credentials through environment variables or external secret stores.

---

## Related Skills

Every MCP gets a generated page:

```text
mcps/colony/skills.md
mcps/higgsfield/skills.md
mcps/medusadocs/skills.md
mcps/omx/state/skills.md
```

The rules live in `configs/mcp-skill-rules.json`:

- `source_url` records the upstream repo or hosted endpoint.
- `homepage`, `package`, `install`, and `health_command` record restore notes.
- `owners` and `agent_surfaces` record who owns the MCP and where it appears.
- `include_skills` maps exact skill names.
- `include_skill_prefixes` maps skill families like `higgsfield-*`.
- `include_skill_categories` maps whole `recodeee/skills` categories.
- keyword matching is off by default to avoid noisy false matches.

---

## Secrets

Do not store secrets in this repo.

Tracked files may show environment variable names, never values:

```text
COLONY_HOME
LETSFG_PYTHON
GITEA_ACCESS_TOKEN
```

Raw configs are intentionally excluded. Generated JSON and markdown normalize
local home paths to `~` and redact env values plus secret-loading shell args.

Before pushing, run:

```sh
./scripts/check-no-secrets.sh
```

It fails nonzero on local home paths, forbidden secret-like files, and common
token prefixes.

---

```
   ─── config map, not credential store. keep it boring. ───
```
