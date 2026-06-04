# context7 skills

Related skills from the cue skills registry.

MCP source: [https://github.com/upstash/context7](https://github.com/upstash/context7)

Homepage: [https://context7.com](https://context7.com)

Package: `@upstash/context7-mcp`

Install: `npx -y @upstash/context7-mcp`

Expected type: `stdio`

Health command: `npx -y @upstash/context7-mcp --help`

Owners: `upstash`

Agent surfaces: `claude`, `codex`

API key: optional. Works with no key at lower rate limits; set `CONTEXT7_API_KEY`
(free at [context7.com/dashboard](https://context7.com/dashboard)) for higher limits.
Remote alternative: `https://mcp.context7.com/mcp` with a `CONTEXT7_API_KEY` header.

## Tools

| Tool | Purpose |
| --- | --- |
| `resolve-library-id` | Resolve a library name (e.g. "next.js") to a Context7 id (e.g. `/vercel/next.js`). |
| `query-docs` | Fetch version-specific docs + code examples for a Context7 library id. |

## CLI (no MCP required)

The `ctx7` CLI exposes the same data:

| Command | Purpose |
| --- | --- |
| `ctx7 library <name> <query>` | Search the index, return matching library ids. |
| `ctx7 docs <libraryId> <query>` | Retrieve docs for a Context7-compatible id. |

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `tools/context7` | `tools` | explicit | Use when fetching up-to-date library/API docs to avoid hallucinated or outdated APIs. |
