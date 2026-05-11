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
| `hud` | `meta` | explicit | [OMX] Use when user says "show hud", "omx hud", "configure statusline", or "live hud". Runs `omx hud`; configures `[tui] status_line` for ralph/ultrawork/autopilot/team state. |
| `team` | `orchestration` | explicit | [OMX] Use when user says "team", "$team", "spawn workers", or "parallel workers". Real Codex/Claude CLI sessions in tmux panes, shared state + mailbox. Requires tmux. NOT for native subagents. |
| `trace` | `meta` | explicit | [OMX] Use when user says "show trace", "trace timeline", or "why did this skill activate". Calls trace_timeline + trace_summary; surfaces hook/keyword/skill/agent flow. NOT debugging — use $analyze. |
