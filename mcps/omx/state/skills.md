# omx_state skills

Related skills from the `soul/skills` registry.

MCP source: [https://github.com/NagyVikt/oh-my-codex](https://github.com/NagyVikt/oh-my-codex)

Homepage: [https://github.com/NagyVikt/oh-my-codex](https://github.com/NagyVikt/oh-my-codex)

Package: `oh-my-codex`

Install: `npm install && npm run build`

Expected type: `stdio`

Health command: `node /path/to/oh-my-codex/dist/mcp/state-server.js --help`

Owners: `NagyVikt`

Agent surfaces: `codex`, `claude`

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `autopilot` | `orchestration` | explicit | [OMX] Strict autonomous loop: $ralplan -> $ralph -> $code-review |
| `cancel` | `orchestration` | explicit | [OMX] Cancel any active OMX mode (autopilot, ralph, ultrawork, ecomode, ultraqa, swarm, ultrapilot, pipeline, team) |
| `hud` | `meta` | explicit | [OMX] Show or configure the OMX HUD (two-layer statusline) |
| `pipeline` | `orchestration` | explicit | [OMX] Configurable pipeline orchestrator for sequencing stages |
| `ralph` | `orchestration` | explicit | [OMX] Self-referential loop until task completion with architect verification |
| `ralplan` | `orchestration` | category | [OMX] Alias for $plan --consensus |
| `team` | `orchestration` | explicit | [OMX] N coordinated agents on shared task list using tmux-based orchestration |
| `ultraqa` | `orchestration` | explicit | [OMX] QA cycling workflow - test, verify, fix, repeat until goal met |
| `ultrawork` | `orchestration` | explicit | [OMX] Parallel execution engine for high-throughput task completion |
| `visual-ralph` | `orchestration` | category | [OMX] Visual Ralph orchestration for frontend UI from generated references, static references, or live URL targets, using $ralph with built-in visual verdict and pixel-diff evidence until the implementation matches and leaves a reproducible design system. |
| `worker` | `orchestration` | category | [OMX] Team worker protocol (ACK, mailbox, task lifecycle) for tmux-based OMX teams |
