# cue/mcps — MCP Server Registry

> The MCP server configurations used by [cue](https://github.com/opencue/cue). Each profile references servers from this registry by ID.

## What's here

```
mcps/
├── configs/              Sanitized JSON configs (no secrets)
│   ├── claude.sanitized.json
│   ├── claude_runtime.sanitized.json
│   └── codex.sanitized.json
├── mcps/                 Per-server documentation
│   ├── gbrain/           Personal wiki with embeddings
│   ├── colony/           Multi-agent coordination
│   ├── coolify/          Deployment management
│   ├── higgsfield/       AI image/video generation
│   └── ...               13+ servers
├── plugins/              Claude Code plugin configs
├── scripts/              Sync and maintenance scripts
└── templates/            New MCP server templates
```

## How cue uses this

When you run `cue use backend`, cue reads `configs/claude.sanitized.json` to find the MCP server entries for that profile's declared MCPs. The materializer writes them into the runtime's `settings.json`.

```yaml
# profiles/backend/profile.yaml
mcps:
  - coolify        # ← looked up in configs/claude.sanitized.json
  - gbrain         # ← inherited from core
```

## Adding a new MCP

1. Add the server config to `configs/claude.sanitized.json`:
   ```json
   "my-server": {
     "command": "npx",
     "args": ["my-mcp-server"]
   }
   ```

2. Create docs at `mcps/my-server/skills.md` describing what tools it exposes.

3. Reference it in a profile: `mcps: [my-server]`

## Security

Configs are **sanitized** — no API keys, tokens, or secrets. Environment variables use `<redacted>` placeholders. Real values live in `~/.claude.json` (never committed).

## Related

- [cue](https://github.com/opencue/cue) — the profile manager that consumes this registry
- [resources/skills](../skills/) — the skill library
