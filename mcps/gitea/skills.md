# gitea skills

Related skills from the `recodeee/skills` registry.

MCP source: [https://github.com/seepine/gitea-mcp](https://github.com/seepine/gitea-mcp)

Homepage: [https://github.com/seepine/gitea-mcp](https://github.com/seepine/gitea-mcp)

Package: `gitea-mcp`

Install: `see upstream release instructions`

Expected type: `stdio`

Health command: `gitea-mcp --help`

Owners: `seepine`

Agent surfaces: `vscode`

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `gh-submodule-publish` | `medusa` | explicit | Create missing GitHub repos and push a parent repo that tracks app repos as Git submodules. Use when user asks to publish locally-initialized repos, push parent + backend/storefront submodules, create org-scoped repos, recover from broken `gh auth` / SSH publickey errors, or fix missing workflow token scope. |
| `github` | `github` | explicit | GitHub operations via the `gh` CLI — issues, PRs, CI runs, code review, API queries. Use when checking PR status or CI, creating/commenting on issues, listing/filtering PRs or issues, or viewing run logs. NOT for bulk cross-repo work (script with `gh api`) or unconfigured `gh auth`. |
