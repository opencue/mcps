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
| `ai-slop-cleaner` | `review` | explicit | Use when user says "cleanup AI slop", "deslop", "refactor this AI code", or "simplify bloated code". Tests-first, smell-by-smell cleanup preserving behavior. NOT for security or general code review. |
| `analyze` | `meta` | explicit | [OMX] Use when user says "analyze", "investigate", "why does X", or "how is X wired". Read-only cross-file analysis: ranked explanations, evidence, file:line. NOT for edits — use $ralph or $plan. |
| `api-tester` | `review` | category | Use when user says "test API", "API endpoint", or "curl this endpoint". Request setup, auth, assertions, response checks. |
| `code-review` | `review` | explicit | Use when user says "review this code", "code review", "review my changes", or "/review". Structured quality/maintainability review with severity-rated findings. NOT for security audits — use security-review. |
| `gh-fix-ci` | `github` | explicit | Use when user says "fix CI", "GitHub checks failed", or "debug PR checks". Inspects failing Actions via gh; fix plan needs approval before implementation. |
| `security-best-practices` | `review` | category | Use when user asks "security best practices", "secure coding for python/typescript/go", or "how to harden this". Language/framework-specific secure-by-default guidance. NOT for auditing existing code — use security-review. |
| `security-review` | `review` | explicit | Use when user says "security review", "security audit", "check for vulnerabilities", "OWASP review", or "/security-review". Audits for OWASP Top 10, secrets, injection, auth flaws. NOT for general code quality — use code-review. |
