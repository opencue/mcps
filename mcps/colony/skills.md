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
| `gitguardex` | `github` | explicit | Use when user says "repo safety is broken", "gx doctor", "dirty worktree", or "finish the agent branch" and needs gitguardex guardrails for branch, worktree, lock, PR, or cleanup state. Runs gx status, gx doctor, and strict verification. NOT for code-quality review; use code-review. |
| `guardex-merge-skills-to-dev` | `github` | explicit | Use when user says "merge skill updates", "skills to dev", "promote SKILL.md changes", "agent branch skills", or needs SKILL.md updates merged from agent branches/worktrees into the local base branch with the multiagent-safety flow. |
| `team` | `orchestration` | explicit | [OMX] Use when user says "team", "$team", "omx team", "spawn workers", "parallel workers", or wants real Codex/Claude CLI sessions in tmux panes coordinated by shared state and mailbox. Requires tmux. NOT for native in-session subagents, single persistence loops, or idea-to-PR autonomy. |
| `trace` | `meta` | explicit | [OMX] Use when user says 'show trace', 'trace timeline', 'omx trace', 'what fired this session', 'why did this skill activate'. Calls trace_timeline + trace_summary MCP tools for chronological hook/keyword/skill/agent/tool flow; surfaces mode transitions, bottlenecks, keyword→skill→agent chains. NOT debugging — use $analyze. |
| `worker` | `orchestration` | explicit | Use when user says "worker", "team worker", or "assigned slice" and needs worker-lane execution guidance. Covers ownership, scope, blocker reporting, and handoff to the leader. |
