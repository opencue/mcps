# colony skills

Related skills from the `soul/skills` registry.

MCP source: [https://github.com/recodeee/colony](https://github.com/recodeee/colony)

Homepage: [https://github.com/recodeee/colony](https://github.com/recodeee/colony)

Package: `colony`

Install: `npm install -g colony`

Expected type: `stdio`

Health command: `colony --help`

Owners: `recodeee`

Agent surfaces: `codex`, `claude`

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `gitguardex` | `github` | explicit | Use when repo safety might be broken (failing CI, dirty working tree, dropped submodules, weird branch state). Runs the gx (gitguardex) guardrail flow — gx status to assess, gx doctor to repair, gx status --strict to verify. Bootstrap via gx setup. NOT for code-quality review — use code-review. |
| `guardex-merge-skills-to-dev` | `github` | explicit | Use when you need to merge SKILL.md updates from agent branches/worktrees into the local base branch (default: dev) with the multiagent-safety flow. |
| `team` | `orchestration` | explicit | [OMX] Use when user says 'team', '$team', 'omx team', 'spawn workers', 'parallel workers', or wants N real Codex/Claude CLI sessions running in tmux panes coordinated by shared task state and mailbox. Requires being inside tmux. NOT for: in-process parallel calls (use $ultrawork), single persistence loop (use $ralph), or autonomous idea-to-PR (use $autopilot). |
| `trace` | `meta` | explicit | [OMX] Use when user says 'show trace', 'trace timeline', 'omx trace', 'what fired this session', 'why did this skill activate'. Calls trace_timeline + trace_summary MCP tools for chronological hook/keyword/skill/agent/tool flow; surfaces mode transitions, bottlenecks, keyword→skill→agent chains. NOT debugging — use $analyze. |
| `worker` | `orchestration` | explicit | [OMX] Auto-loaded by Codex sessions started as an OMX Team worker (a tmux pane spawned by $team). Defines the worker startup ACK, mailbox poll loop, and task lifecycle. Use when OMX_TEAM_WORKER is set or the worker inbox tells you to load it. NOT user-invocable — leader-spawned only. |
