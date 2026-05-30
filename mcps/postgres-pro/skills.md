# postgres-pro skills

`crystaldba/postgres-mcp` — Postgres MCP Pro. Schema inspection, query, plus
performance analysis, index tuning, and health checks. Maintained alternative
to the archived `@modelcontextprotocol/server-postgres`.

## Setup

- Runs via `uvx postgres-mcp` (needs `uv` installed).
- Required env: `DATABASE_URI` (e.g. `postgresql://user:pass@host:5432/db`).
- Default `--access-mode=restricted` (read-only-ish, safe). Switch to
  `--access-mode=unrestricted` in the registry only for a dev DB.

Profiles must export `DATABASE_URI` or materialize fails fast naming the var.

Related skills: pairs with the `postgres` profile's DB-ops skills.
