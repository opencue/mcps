# omx_code_intel skills

Related skills from the `recodeee/skills` registry.

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
| `ai-slop-cleaner` | `review` | explicit | Use when user says 'cleanup AI slop', 'deslop', 'refactor this AI code', 'remove dead code', 'simplify bloated code', or asks to clean up AI-generated output. Tests-first, smell-by-smell cleanup that preserves behavior. NOT for security or general code review. |
| `analyze` | `meta` | explicit | [OMX] Use when user says 'analyze', 'investigate', 'why does X', 'what's causing', 'how is X wired'. Read-only cross-file repo analysis: ranked explanations, confidence, file:line evidence, evidence-vs-inference boundaries. NOT for edits/fixes — use $ralph or $plan. |
| `code-review` | `review` | explicit | Use when user says 'review this code', 'code review', 'review my changes', 'review the diff', or '/review'. Runs a structured quality and maintainability review with severity-rated feedback. NOT for security audits — use security-review. |
| `gh-fix-ci` | `github` | explicit | Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions; use `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treat external providers (for example Buildkite) as out of scope and report only the details URL. |
| `security-best-practices` | `review` | category | Use when user asks 'security best practices', 'secure coding for python/typescript/go', 'how to harden this', or wants language/framework-specific secure-by-default guidance. Loads language-specific security references. NOT for auditing existing code — use security-review. |
| `security-review` | `review` | explicit | Use when user says 'security review', 'security audit', 'check for vulnerabilities', 'OWASP review', 'find security issues', or '/security-review'. Audits code for OWASP Top 10, hardcoded secrets, injection, auth flaws, unsafe patterns. NOT for general code quality — use code-review. |
