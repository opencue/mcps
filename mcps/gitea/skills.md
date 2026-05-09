# gitea skills

Related skills from the `recodeee/skills` registry.

MCP source: [https://github.com/seepine/gitea-mcp](https://github.com/seepine/gitea-mcp)

| Skill | Reason | Description |
| --- | --- | --- |
| `gh-submodule-publish` | explicit | Create missing GitHub repositories and push a parent repository that tracks app repositories as Git submodules. Use when the user asks to finish publishing locally initialized repos, push a parent repo plus backend/storefront submodules, create repos under an org, recover from invalid `gh auth status` when `gh api user` works, fall back from SSH `Permission denied (publickey)` to `gh` HTTPS auth, handle missing `workflow` token scope for `.github/workflows/*`, or verify remote `main` refs after push. |
| `github` | explicit | GitHub operations via `gh` CLI: issues, PRs, CI runs, code review, API queries. Use when: (1) checking PR status or CI, (2) creating/commenting on issues, (3) listing/filtering PRs or issues, (4) viewing run logs. NOT for: complex web UI interactions requiring manual browser flows (use browser tooling when available), bulk operations across many repos (script with gh api), or when gh auth is not configured. |
