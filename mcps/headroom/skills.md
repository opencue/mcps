# headroom skills

Related skills from the cue skills registry: `tools/headroom`.

MCP source: [https://github.com/chopratejas/headroom](https://github.com/chopratejas/headroom)

Homepage: [https://headroom-docs.vercel.app/docs](https://headroom-docs.vercel.app/docs)

Package: `headroom-ai` (PyPI / npm)

Install: `pip install "headroom-ai[all]"` (or `pip install "headroom-ai[mcp]"` for just the MCP server)

MCP install (auto-detect agents): `headroom mcp install`

Serve (stdio): `headroom mcp serve`

Expected type: `stdio`

Health command: `headroom mcp status`

Owners: `chopratejas`

Agent surfaces: `claude`, `codex`

API key: none. Runs fully local; your data stays on the machine. Anonymous
telemetry is on by default — set `HEADROOM_TELEMETRY=off` to disable.

## Tools

- `headroom_compress` — compress a blob of context (tool output, log, file, RAG
  chunk, conversation) before it reaches the model. Auto-routes by content type
  (JSON → SmartCrusher, code → AST, prose → Kompress-base).
- `headroom_retrieve` — fetch the original, uncompressed content for a prior
  compression (Compress-Cache-Retrieve / CCR). Compression is reversible.
- `headroom_stats` — token-savings and compression observability for the session.

## Notes

- The MCP server gives compression tools to any MCP host (no proxy required).
- For transparent, whole-session compression of **all** Claude traffic, use the
  proxy/wrap instead: `headroom wrap claude` (sets `ANTHROPIC_BASE_URL` to a local
  `headroom proxy`). The MCP and the proxy can be used together or independently.
- `headroom learn` mines failed sessions and writes corrections into `CLAUDE.md`
  / `AGENTS.md`.
