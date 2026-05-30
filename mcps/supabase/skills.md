# supabase skills

`supabase-community/supabase-mcp` (🎖️ official). Manage tables, fetch config,
and query a Supabase project from the agent. Wired with `--read-only` by default.

## Setup

- Runs via `npx -y @supabase/mcp-server-supabase@latest`.
- Required env: `SUPABASE_ACCESS_TOKEN` (a Supabase **management API** token).

## Caveat — self-hosted vs cloud

This server targets **Supabase Cloud** (management API via access token). If you
**self-host** Supabase (per the VPS setup), the management API may not apply;
point `postgres-pro` at the self-hosted Postgres connection string instead.
Use this server for Cloud-hosted Supabase projects.

Related skills: pairs with `backend` / `medusa-*` data-layer work.
