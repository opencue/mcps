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
| `autopilot` | `orchestration` | explicit | [OMX] Use when user says 'autopilot', '$autopilot', 'autonomous', 'full auto', 'handle it all', 'build me', 'create me', or 'make me X' from an idea/issue/PRD. Runs the strict ralplan -> ralph -> code-review loop, returning to ralplan automatically when review is not clean. NOT for: single focused edits (use $ralph), planning only (use $ralplan), or review only (use $code-review). |
| `cancel` | `orchestration` | explicit | [OMX] Use when user says 'cancel', '/cancel', 'stop', 'abort', 'cancelomc', 'stopomc', or '--force'. Detects the active OMX mode (autopilot, ralph, ultrawork, ultraqa, swarm, ultrapilot, pipeline, team) and terminalizes its state cleanly, including tmux team shutdown and linked-mode cleanup. Preserves autopilot for resume; clears others. |
| `executing-development-plans` | `orchestration` | category | Use when implementing from an existing plan, PRD, task list, OpenSpec change, or staged execution checklist. |
| `hud` | `meta` | explicit | [OMX] Use when user says 'show hud', 'omx hud', 'configure statusline', 'change hud preset', 'live hud', or wants ralph/ultrawork/autopilot/team/pipeline mode state. Runs `omx hud [--watch\|--json\|--preset=minimal\|focused\|full]`, reads .omx/state/*.json, configures `[tui] status_line` in ~/.codex/config.toml. |
| `parallel-agent-dispatching` | `orchestration` | category | Use when a task has independent lanes that can run in parallel with bounded ownership and verification. |
| `pipeline` | `orchestration` | explicit | [OMX] Use when user says '$pipeline', 'run the pipeline', or wants explicit configurable stage sequencing (custom stage list, custom worker count, custom iteration ceilings). Runs ralplan -> team-exec -> ralph-verify by default through the PipelineStage interface with persisted resume. NOT for: standard hands-off delivery (use $autopilot). |
| `ralph` | `orchestration` | explicit | [OMX] Use when user says ralph, $ralph, do not stop, must complete, finish this, or keep going until done on a single concrete task. Persistence loop with parallel delegation, architect verification, deslop pass, regression re-verify. NOT for idea→PR autonomy (use $autopilot) or planning (use $ralplan). |
| `ralplan` | `orchestration` | category | [OMX] Use when user says 'ralplan', '$ralplan', 'plan this', 'plan with consensus', 'PRD for', or when an execution request is too vague (e.g. 'ralph fix this', 'autopilot build the app'). Runs the Planner -> Architect -> Critic consensus loop with RALPLAN-DR deliberation, ADR, pre-mortem, and test spec; outputs an approved plan. NOT for: implementing code (use $ralph or $team). |
| `subagent-driven-development` | `orchestration` | category | Use when implementing a plan with bounded subagents, separate review passes, and integration ownership. |
| `team` | `orchestration` | explicit | [OMX] Use when user says 'team', '$team', 'omx team', 'spawn workers', 'parallel workers', or wants N real Codex/Claude CLI sessions running in tmux panes coordinated by shared task state and mailbox. Requires being inside tmux. NOT for: in-process parallel calls (use $ultrawork), single persistence loop (use $ralph), or autonomous idea-to-PR (use $autopilot). |
| `ultraqa` | `orchestration` | explicit | [OMX] Use when user says 'ultraqa', '/ultraqa', '--tests', '--build', '--lint', '--typecheck', or 'fix until tests/build/lint/types pass'. Runs the qa-tester -> architect diagnosis -> executor fix cycle (max 5) until the chosen verification goal is met or the same failure repeats. NOT for: implementing new features (use $ralph) or full delivery (use $autopilot). |
| `ultrawork` | `orchestration` | explicit | [OMX] Use when user says ulw, ultrawork, or wants parallel execution of multiple independent tasks. Provides parallelism, context discipline, and smart delegation guidance — but no persistence. NOT for guaranteed completion (use $ralph), full idea→PR pipeline (use $autopilot), or a single sequential task (just execute). |
| `visual-ralph` | `orchestration` | category | [OMX] Visual Ralph orchestration for frontend UI from generated references, static references, or live URL targets, using $ralph with $visual-verdict and pixel-diff evidence until the implementation matches and leaves a reproducible design system. |
| `worker` | `orchestration` | category | [OMX] Auto-loaded by Codex sessions started as an OMX Team worker (a tmux pane spawned by $team). Defines the worker startup ACK, mailbox poll loop, and task lifecycle. Use when OMX_TEAM_WORKER is set or the worker inbox tells you to load it. NOT user-invocable — leader-spawned only. |
