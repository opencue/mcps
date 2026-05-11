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
| `autopilot` | `orchestration` | explicit | [OMX] Use when user says "autopilot", "$autopilot", "autonomous", "full auto", "build me", or "make me X" from idea/PRD. Strict ralplan → ralph → code-review loop. NOT for single edits ($ralph), planning only ($ralplan). |
| `cancel` | `orchestration` | explicit | [OMX] Use when user says "cancel", "/cancel", "stop", "abort", or "--force". Terminates active OMX mode (autopilot/ralph/ultrawork/ultraqa/swarm/pipeline/team); tmux team shutdown. |
| `hud` | `meta` | explicit | [OMX] Use when user says "show hud", "omx hud", "configure statusline", or "live hud". Runs `omx hud`; configures `[tui] status_line` for ralph/ultrawork/autopilot/team state. |
| `pipeline` | `orchestration` | explicit | [OMX] Use when user says "$pipeline" or "run the pipeline" with custom stages/workers/iterations. ralplan → team-exec → ralph-verify via PipelineStage with persisted resume. NOT for hands-off delivery — use $autopilot. |
| `ralph` | `orchestration` | explicit | [OMX] Use when user says "ralph", "$ralph", "do not stop", "finish this", or "keep going" on one task. Persistence loop with delegation, architect verification, regression check. NOT for planning — use ralplan. |
| `ralplan` | `orchestration` | category | [OMX] Use when user says "ralplan", "$ralplan", "plan this", or "PRD for". Planner/Architect/Critic consensus with RALPLAN-DR, ADR, pre-mortem, test spec. NOT for implementing code. |
| `team` | `orchestration` | explicit | [OMX] Use when user says "team", "$team", "spawn workers", or "parallel workers". Real Codex/Claude CLI sessions in tmux panes, shared state + mailbox. Requires tmux. NOT for native subagents. |
| `ultraqa` | `orchestration` | explicit | [OMX] Use when user says "ultraqa", "/ultraqa", "--tests", "--build", "--lint", or "fix until tests pass". qa-tester → architect → executor cycle until verification met. NOT for new features — use $ralph. |
| `ultrawork` | `orchestration` | explicit | [OMX] Use when user says "ulw", "ultrawork", "parallel execution", or "multiple independent tasks". Concurrent work, context discipline, delegation. NOT for sequential tasks or idea-to-PR autonomy. |
| `visual-ralph` | `orchestration` | category | Use when user says "visual ralph", "iterate visually", or "keep fixing UI". Persistent visual iteration: screenshot, verdict, edit, re-verify. |
| `worker` | `orchestration` | category | Use when user says "worker", "team worker", or "assigned slice". Worker-lane execution: ownership, scope, blocker reporting, handoff. |
