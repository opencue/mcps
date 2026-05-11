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
| `api-tester` | `review` | category | Batch-validate LLM API keys across 7 providers (OpenAI, Anthropic, Gemini, DeepSeek, SiliconCloud, xAI, OpenRouter) via the local `api-tester` CLI. Use when user says "test these keys", "validate api keys", "are these keys still good", "audit these tokens", "check which keys work", or pastes a list of candidate keys (sk-, sk-ant-, xai-, AIza, sk-or-) and asks if they're real. NOT for sending an actual chat completion as a one-off (use the relevant provider SDK) or for quality/code review (use code-review / security-review). |
| `architecture-review` | `review` | category | Use when reviewing system design, boundaries, scalability, coupling, data flow, failure modes, or technical tradeoffs. |
| `code-review` | `review` | explicit | Use when user says 'review this code', 'code review', 'review my changes', 'review the diff', or '/review'. Runs a structured quality and maintainability review with severity-rated feedback. NOT for security audits — use security-review. |
| `code-review-handling` | `review` | category | Use when responding to reviewer comments, CI findings, PR feedback, requested changes, or conflicting review recommendations. |
| `code-review-requesting` | `review` | category | Use when preparing work for review, asking another agent for review, opening a PR, or producing a review-ready summary. |
| `gh-fix-ci` | `github` | explicit | Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions; use `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treat external providers (for example Buildkite) as out of scope and report only the details URL. |
| `security-best-practices` | `review` | category | Use when user asks 'security best practices', 'secure coding for python/typescript/go', 'how to harden this', or wants language/framework-specific secure-by-default guidance. Loads language-specific security references. NOT for auditing existing code — use security-review. |
| `security-review` | `review` | explicit | Use when user says 'security review', 'security audit', 'check for vulnerabilities', 'OWASP review', 'find security issues', or '/security-review'. Audits code for OWASP Top 10, hardcoded secrets, injection, auth flaws, unsafe patterns. NOT for general code quality — use code-review. |
| `systematic-debugging` | `review` | category | Use when diagnosing a bug, regression, flaky behavior, failing command, broken integration, or unclear runtime behavior that needs evidence-first root cause analysis. |
| `test-driven-development` | `review` | category | Use when the user asks for TDD, test-first development, regression-first bug fixing, or behavior changes that should be locked by tests before implementation. |
| `verification-before-completion` | `review` | category | Use before claiming work is done, especially after code, config, deployment, data, content, or workflow changes that need proof. |
