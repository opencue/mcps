# omx_trace skills

Related skills from the `recodeee/skills` registry.

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
| `hud` | `meta` | explicit | [OMX] Use when user says 'show hud', 'omx hud', 'configure statusline', 'change hud preset', 'live hud', or wants ralph/ultrawork/autopilot/team/pipeline mode state. Runs `omx hud [--watch\|--json\|--preset=minimal\|focused\|full]`, reads .omx/state/*.json, configures `[tui] status_line` in ~/.codex/config.toml. |
| `team` | `orchestration` | explicit | [OMX] Use when user says 'team', '$team', 'omx team', 'spawn workers', 'parallel workers', or wants N real Codex/Claude CLI sessions running in tmux panes coordinated by shared task state and mailbox. Requires being inside tmux. NOT for: in-process parallel calls (use $ultrawork), single persistence loop (use $ralph), or autonomous idea-to-PR (use $autopilot). |
| `trace` | `meta` | explicit | [OMX] Use when user says 'show trace', 'trace timeline', 'omx trace', 'what fired this session', 'why did this skill activate'. Calls trace_timeline + trace_summary MCP tools for chronological hook/keyword/skill/agent/tool flow; surfaces mode transitions, bottlenecks, keyword→skill→agent chains. NOT debugging — use $analyze. |
