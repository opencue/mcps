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
| `ai-slop-cleaner` | `review` | explicit | Use when user says 'cleanup AI slop', 'deslop', 'refactor this AI code', 'remove dead code', 'simplify bloated code', or asks to clean up AI-generated output. Tests-first, smell-by-smell cleanup that preserves behavior. NOT for security or general code review. |
| `analyze` | `meta` | explicit | [OMX] Use when user says 'analyze', 'investigate', 'why does X', 'what's causing', 'how is X wired'. Read-only cross-file repo analysis: ranked explanations, confidence, file:line evidence, evidence-vs-inference boundaries. NOT for edits/fixes — use $ralph or $plan. |
| `api-tester` | `review` | category | Use when user says "test API", "API endpoint", or "curl this endpoint" and needs API validation. Covers request setup, auth, assertions, response checks, and failure evidence. |
| `architecture-review` | `review` | category | Use when user says "architecture review", "review design", or "system design critique" and needs architecture feedback. Covers boundaries, tradeoffs, risks, scalability, and tests. |
| `code-review` | `review` | explicit | Use when user says "review this code", "code review", "review my changes", "review the diff", or "/review". Runs a structured quality and maintainability review with severity-rated findings. NOT for security audits; use security-review. |
| `code-review-handling` | `review` | category | Use when user says "handle review comments", "fix PR feedback", or "address code review" and needs review-response guidance. Covers triage, patches, evidence, and replies. |
| `code-review-requesting` | `review` | category | Use when user says "request review", "ask for code review", or "prepare PR review" and needs review-request guidance. Covers context, scope, risk, checklist, and reviewer notes. |
| `gh-fix-ci` | `github` | explicit | Use when user says "fix CI", "GitHub checks failed", "debug PR checks", "view Actions logs", or needs failing GitHub Actions inspected with gh. Summarize failure context, draft a fix plan, and implement only after explicit approval. External providers are out of scope. |
| `security-best-practices` | `review` | category | Use when user asks 'security best practices', 'secure coding for python/typescript/go', 'how to harden this', or wants language/framework-specific secure-by-default guidance. Loads language-specific security references. NOT for auditing existing code — use security-review. |
| `security-review` | `review` | explicit | Use when user says 'security review', 'security audit', 'check for vulnerabilities', 'OWASP review', 'find security issues', or '/security-review'. Audits code for OWASP Top 10, hardcoded secrets, injection, auth flaws, unsafe patterns. NOT for general code quality — use code-review. |
| `systematic-debugging` | `review` | category | Use when user says "debug this", "investigate the failure", "find root cause", "flaky test", or needs evidence-first diagnosis of a bug, regression, failing command, broken integration, or unclear runtime behavior. |
| `test-driven-development` | `review` | category | Use when user says "TDD", "test first", or "write failing test" and needs test-driven development guidance. Covers regression tests, minimal implementation, refactor, and validation. |
| `verification-before-completion` | `review` | category | Use when user expects final proof, or before saying "done", "complete", "fixed", "verified", or after code, config, deployment, data, content, or workflow changes that need evidence before final reporting. |
