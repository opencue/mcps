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
| `gitguardex` | `github` | explicit | Use when user says "gx doctor", "dirty worktree", or "finish the agent branch". gitguardex guardrails for branch/worktree/lock/PR state. NOT for code-quality review (use code-review). |
| `guardex-merge-skills-to-dev` | `github` | explicit | Use when user says "merge skill updates", "promote SKILL.md changes", or "agent branch skills". Merges SKILL.md updates from agent branches into base with multiagent-safety flow. |
| `team` | `orchestration` | explicit | [OMX] N coordinated agents on shared task list using tmux-based orchestration |
| `trace` | `meta` | explicit | [OMX] Use when user says "show trace", "trace timeline", or "why did this skill activate". Calls trace_timeline + trace_summary; surfaces hook/keyword/skill/agent flow. NOT debugging — use $analyze. |
| `worker` | `orchestration` | explicit | [OMX] Team worker protocol (ACK, mailbox, task lifecycle) for tmux-based OMX teams |
