# cue-dashboard MCP

Wraps the running **cue studio dashboard** REST API (`cue dashboard`, default
`http://127.0.0.1:7891/api/v1/*`) as MCP tools, so an agent can query live
profile / skill / MCP / gap data and run dashboard mutations as typed tool calls.

It is a thin HTTP client. `src/lib/dashboard-server.ts` in the cue repo is the
only source of truth for the endpoints; the `cue dash` CLI wraps the same API
for shell use.

## Requirements

- The dashboard must be running: `cue dashboard` (or `cue dashboard --port N`).
- `bun` on PATH (or `~/.bun/bin/bun`).
- Target host/port via `CUE_DASH_HOST` / `CUE_DASH_PORT` (default `127.0.0.1` / `7891`).

## Install

```bash
cd resources/mcps/cue-dashboard && bun install
```

## Register

In the MCP registry (`resources/mcps/configs/claude.sanitized.json`):

```json
"cue-dashboard": {
  "command": "<repo>/resources/mcps/cue-dashboard/bin/cue-dashboard"
}
```

Then add `cue-dashboard` to a profile's `mcps:` list.

## Tools

Read: `dashboard_status`, `dashboard_profiles`, `dashboard_profile_detail`,
`dashboard_trigger_gaps`, `dashboard_skill_report`, `dashboard_pairs`,
`dashboard_active_sessions`, `dashboard_mcp_catalog`, `dashboard_plugins`,
`dashboard_timeline`.

Mutating (confirm before calling): `dashboard_add_mcp`, `dashboard_kill_session`,
`dashboard_merge_preview` (read-only), `dashboard_merge_save`.
