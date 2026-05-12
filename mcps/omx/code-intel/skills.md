# omx_code_intel skills

Related skills from the `soul/skills` registry.

MCP source: [https://github.com/NagyVikt/oh-my-codex](https://github.com/NagyVikt/oh-my-codex)

Homepage: [https://github.com/NagyVikt/oh-my-codex](https://github.com/NagyVikt/oh-my-codex)

Package: `oh-my-codex`

Install: `npm install && npm run build`

Expected type: `stdio`

Health command: `node /path/to/oh-my-codex/dist/mcp/code-intel-server.js --help`

Owners: `NagyVikt`

Agent surfaces: `codex`, `claude`

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `ai-slop-cleaner` | `review` | explicit | [OMX] Run an anti-slop cleanup/refactor/deslop workflow |
| `analyze` | `meta` | explicit | [OMX] Run read-only deep repository analysis and return a ranked synthesis with explicit confidence, concrete file references, and clear evidence-vs-inference boundaries. Use when a user says 'analyze', 'investigate', 'why does', 'what's causing', or needs grounded cross-file explanation before any changes are proposed. |
| `api-tester` | `review` | category | Use when user says "test API", "API endpoint", or "curl this endpoint". Request setup, auth, assertions, response checks. |
| `code-review` | `review` | explicit | [OMX] Run a comprehensive code review |
| `gh-fix-ci` | `github` | explicit | Use when user says "fix CI", "GitHub checks failed", or "debug PR checks". Inspects failing Actions via gh; fix plan needs approval before implementation. |
| `security-best-practices` | `review` | category | Use when user asks "security best practices", "secure coding for python/typescript/go", or "how to harden this". Language/framework-specific secure-by-default guidance. NOT for auditing existing code — use security-review. |
| `security-review` | `review` | explicit | Use when user says "security review", "security audit", "check for vulnerabilities", "OWASP review", or "/security-review". Audits for OWASP Top 10, secrets, injection, auth flaws. NOT for general code quality — use code-review. |
