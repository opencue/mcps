# omx_memory skills

Related skills from the `recodeee/skills` registry.

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
| `note` | `meta` | explicit | [OMX] Save context to .omx/notepad.md so it survives compaction. Use when user says /note, save this note, remember this for later, /note --priority, or /note --show. Three sections: Priority Context (always loaded), Working Memory (timestamped, auto-pruned), MANUAL (never pruned). |
| `wiki` | `meta` | explicit | [OMX] Persistent project wiki under .omx/wiki with keyword search and lifecycle capture. Use when user says wiki add, wiki query, wiki lint, wiki read, wiki delete, or asks to save architectural decisions / ingest project knowledge into a searchable markdown KB. |
