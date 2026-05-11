# omx_memory skills

Related skills from the `soul/skills` registry.

MCP source: [https://github.com/NagyVikt/oh-my-codex](https://github.com/NagyVikt/oh-my-codex)

Homepage: [https://github.com/NagyVikt/oh-my-codex](https://github.com/NagyVikt/oh-my-codex)

Package: `oh-my-codex`

Install: `npm install && npm run build`

Expected type: `stdio`

Health command: `node /path/to/oh-my-codex/dist/mcp/memory-server.js --help`

Owners: `NagyVikt`

Agent surfaces: `codex`, `claude`

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `note` | `meta` | explicit | Use when user says "note this", "save note", or "remember this" and needs a local note workflow. Covers note placement, concise capture, retrieval, and confirmation. |
| `wiki` | `meta` | explicit | Use when user says "wiki", "document knowledge", or "knowledge base" and needs wiki guidance. Covers structure, linking, maintenance, and retrieval.triggers: ["wiki add", "wiki lint", "wiki query", "wiki read", "wiki delete"] |
