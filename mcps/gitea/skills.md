# gitea skills

Related skills from the `soul/skills` registry.

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
| `github` | `github` | explicit | Use when user says "check the PR", "open an issue", "view CI logs", "merge this PR", or needs GitHub operations via gh: issues, PRs, checks, run logs, reviews, comments, and API queries. NOT for unconfigured gh auth or bulk cross-repo scripting. |
