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
| `executing-development-plans` | `orchestration` | category | Use when user says "execute the plan", "run the implementation plan", or "work through tasks" and needs plan execution guidance. Covers sequencing, edits, validation, and status reporting. |
| `hud` | `meta` | explicit | [OMX] Use when user says 'show hud', 'omx hud', 'configure statusline', 'change hud preset', 'live hud', or wants ralph/ultrawork/autopilot/team/pipeline mode state. Runs `omx hud [--watch\|--json\|--preset=minimal\|focused\|full]`, reads .omx/state/*.json, configures `[tui] status_line` in ~/.codex/config.toml. |
| `parallel-agent-dispatching` | `orchestration` | category | Use when user says "dispatch agents", "parallel agents", or "split this up" and needs parallel subtask guidance. Covers ownership, non-overlap, integration, and verification. |
| `pipeline` | `orchestration` | explicit | [OMX] Use when user says '$pipeline', 'run the pipeline', or wants explicit configurable stage sequencing (custom stage list, custom worker count, custom iteration ceilings). Runs ralplan -> team-exec -> ralph-verify by default through the PipelineStage interface with persisted resume. NOT for: standard hands-off delivery (use $autopilot). |
| `ralph` | `orchestration` | explicit | [OMX] Use when user says "ralph", "$ralph", "do not stop", "must complete", "finish this", or "keep going until done" on one concrete task. Persistence loop with delegation, architect verification, cleanup pass, and regression re-verify. NOT for planning; use ralplan. |
| `ralplan` | `orchestration` | category | [OMX] Use when user says "ralplan", "$ralplan", "plan this", "plan with consensus", "PRD for", or gives a vague execution request. Runs Planner, Architect, and Critic consensus with RALPLAN-DR, ADR, pre-mortem, and test spec. NOT for implementing code. |
| `subagent-driven-development` | `orchestration` | category | Use when user says "use subagents", "delegate work", or "subagent development" and needs bounded native subagent guidance. Covers slicing, prompts, integration, and validation. |
| `team` | `orchestration` | explicit | [OMX] Use when user says "team", "$team", "omx team", "spawn workers", "parallel workers", or wants real Codex/Claude CLI sessions in tmux panes coordinated by shared state and mailbox. Requires tmux. NOT for native in-session subagents, single persistence loops, or idea-to-PR autonomy. |
| `ultraqa` | `orchestration` | explicit | [OMX] Use when user says 'ultraqa', '/ultraqa', '--tests', '--build', '--lint', '--typecheck', or 'fix until tests/build/lint/types pass'. Runs the qa-tester -> architect diagnosis -> executor fix cycle (max 5) until the chosen verification goal is met or the same failure repeats. NOT for: implementing new features (use $ralph) or full delivery (use $autopilot). |
| `ultrawork` | `orchestration` | explicit | [OMX] Use when user says "ulw", "ultrawork", "parallel execution", "multiple independent tasks", or wants concurrent work without persistence. Provides parallelism, context discipline, and delegation guidance. NOT for guaranteed completion, idea-to-PR autonomy, or one sequential task. |
| `visual-ralph` | `orchestration` | category | Use when user says "visual ralph", "iterate visually", or "keep fixing UI" and needs persistent visual iteration. Covers screenshot evidence, visual verdicts, edits, and re-verification. |
| `worker` | `orchestration` | category | Use when user says "worker", "team worker", or "assigned slice" and needs worker-lane execution guidance. Covers ownership, scope, blocker reporting, and handoff to the leader. |
