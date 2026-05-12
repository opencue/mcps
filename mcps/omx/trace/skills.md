# omx_trace skills

Related skills from the `soul/skills` registry.

MCP source: [https://github.com/NagyVikt/oh-my-codex](https://github.com/NagyVikt/oh-my-codex)

Homepage: [https://github.com/NagyVikt/oh-my-codex](https://github.com/NagyVikt/oh-my-codex)

Package: `oh-my-codex`

Install: `npm install && npm run build`

Expected type: `stdio`

Health command: `node /path/to/oh-my-codex/dist/mcp/trace-server.js --help`

Owners: `NagyVikt`

Agent surfaces: `codex`, `claude`

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `hud` | `meta` | explicit | [OMX] Show or configure the OMX HUD (two-layer statusline) |
| `team` | `orchestration` | explicit | [OMX] N coordinated agents on shared task list using tmux-based orchestration |
| `trace` | `meta` | explicit | [OMX] Use when user says "show trace", "trace timeline", or "why did this skill activate". Calls trace_timeline + trace_summary; surfaces hook/keyword/skill/agent flow. NOT debugging — use $analyze. |
