#!/usr/bin/env bun
/**
 * cue-dashboard — MCP server that wraps the running cue studio dashboard's REST
 * API (`cue dashboard`, default http://127.0.0.1:7891/api/v1/*) as tools, so an
 * agent can query live profile/skill/MCP/gap data and perform dashboard
 * mutations (add-mcp, kill-session, merge) as typed tool calls.
 *
 * This is a thin HTTP client; `src/lib/dashboard-server.ts` in the cue repo is
 * the only source of truth for the endpoints. The `cue dash` CLI wraps the same
 * API for shell use. The dashboard must be running.
 *
 * Target host/port come from CUE_DASH_HOST / CUE_DASH_PORT (default
 * 127.0.0.1 / 7891).
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const HOST = process.env.CUE_DASH_HOST || "127.0.0.1";
const PORT = Number(process.env.CUE_DASH_PORT) || 7891;

const server = new McpServer(
  { name: "cue-dashboard", version: "0.1.0" },
  { capabilities: { tools: {} } },
);

function text(t: string) {
  return { content: [{ type: "text" as const, text: t }] };
}
function err(t: string) {
  return { content: [{ type: "text" as const, text: t }], isError: true };
}

type Envelope = { ok: true; data: unknown } | { ok: false; error: string };

/** Call one dashboard endpoint and unwrap the `{ok, data|error}` envelope. */
async function dashFetch(
  path: string,
  opts: { query?: Record<string, string>; method?: "GET" | "POST"; body?: unknown } = {},
): Promise<unknown> {
  const qs = opts.query && Object.keys(opts.query).length > 0
    ? "?" + new URLSearchParams(opts.query).toString()
    : "";
  const url = `http://${HOST}:${PORT}/api/v1${path}${qs}`;
  let res: Response;
  try {
    res = await fetch(url, {
      method: opts.method ?? "GET",
      headers: opts.body ? { "content-type": "application/json" } : undefined,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
  } catch (e) {
    throw new Error(`cannot reach the dashboard at ${HOST}:${PORT} (${(e as Error).message}). Start it with \`cue dashboard\`.`);
  }
  let env: Envelope;
  try { env = (await res.json()) as Envelope; }
  catch { throw new Error(`dashboard returned non-JSON (HTTP ${res.status}) for ${path}`); }
  if (!env.ok) throw new Error(env.error);
  return env.data;
}

/** Register a tool that GETs a fixed path and returns its JSON. */
function readTool(name: string, desc: string, path: string): void {
  server.tool(name, desc, {}, async () => {
    try { return text(JSON.stringify(await dashFetch(path), null, 2)); }
    catch (e) { return err((e as Error).message); }
  });
}

// ─── Read tools ──────────────────────────────────────────────────────────────
readTool("dashboard_status", "Dashboard + active-profile + runtime status.", "/status");
readTool("dashboard_profiles", "Every profile cue knows about, with skill/mcp/plugin counts.", "/profiles");
readTool("dashboard_skill_report", "Per-skill usage report across the active profile.", "/skill-report");
readTool("dashboard_pairs", "Profile pair-affinity suggestions (which profiles get combined).", "/pairs");
readTool("dashboard_active_sessions", "Currently-running cue sessions (pid, profile, cwd).", "/active-sessions");
readTool("dashboard_mcp_catalog", "The MCP catalog cue can wire into profiles.", "/mcps/catalog");
readTool("dashboard_plugins", "Plugins discovered on the machine.", "/plugins/discovered");
readTool("dashboard_timeline", "Telemetry timeline of recent activity.", "/telemetry/timeline");

server.tool(
  "dashboard_profile_detail",
  "Resolve one profile's full skills/mcps/plugins/commands (what materializes when you launch it).",
  { profile: z.string().describe("Profile name or composite selector, e.g. 'browser' or 'core+skill-writer'.") },
  async ({ profile }) => {
    try { return text(JSON.stringify(await dashFetch("/profile-detail", { query: { profile } }), null, 2)); }
    catch (e) { return err((e as Error).message); }
  },
);

server.tool(
  "dashboard_trigger_gaps",
  "Skills whose triggers matched a recent prompt but never fired — coverage gaps to fix.",
  { profile: z.string().default("").describe("Optional profile to scope to; empty = active profile.") },
  async ({ profile }) => {
    try { return text(JSON.stringify(await dashFetch("/trigger-gaps", { query: profile ? { profile } : undefined }), null, 2)); }
    catch (e) { return err((e as Error).message); }
  },
);

// ─── Mutating tools ──────────────────────────────────────────────────────────
server.tool(
  "dashboard_add_mcp",
  "MUTATES: add an MCP server to a profile. Confirm with the user before calling.",
  {
    profile: z.string().describe("Target profile name."),
    mcp: z.string().describe("MCP id from the catalog (dashboard_mcp_catalog), e.g. 'playwright'."),
  },
  async ({ profile, mcp }) => {
    try { return text(JSON.stringify(await dashFetch("/mcps/add", { method: "POST", body: { profile, id: mcp } }), null, 2)); }
    catch (e) { return err((e as Error).message); }
  },
);

server.tool(
  "dashboard_kill_session",
  "MUTATES: terminate a running cue session by pid (the server refuses non-cue pids). Confirm first.",
  {
    pid: z.number().int().describe("Pid of the session, from dashboard_active_sessions."),
    sigkill: z.boolean().default(false).describe("Send SIGKILL instead of SIGTERM."),
  },
  async ({ pid, sigkill }) => {
    try { return text(JSON.stringify(await dashFetch("/sessions/kill", { method: "POST", body: { pid, signal: sigkill ? "SIGKILL" : "SIGTERM" } }), null, 2)); }
    catch (e) { return err((e as Error).message); }
  },
);

server.tool(
  "dashboard_merge_preview",
  "Preview merging 2+ profiles into one (no write). Returns the combined resource set.",
  { profiles: z.array(z.string()).min(2).describe("Profile names to merge, e.g. ['frontend','backend'].") },
  async ({ profiles }) => {
    try { return text(JSON.stringify(await dashFetch("/merge/preview", { method: "POST", body: { names: profiles } }), null, 2)); }
    catch (e) { return err((e as Error).message); }
  },
);

server.tool(
  "dashboard_merge_save",
  "MUTATES: save a merge of 2+ profiles as a new profile on disk. Confirm first.",
  {
    profiles: z.array(z.string()).min(2).describe("Profile names to merge."),
    name: z.string().default("").describe("Name for the merged profile (optional)."),
  },
  async ({ profiles, name }) => {
    try { return text(JSON.stringify(await dashFetch("/merge/save", { method: "POST", body: { names: profiles, name: name || undefined } }), null, 2)); }
    catch (e) { return err((e as Error).message); }
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
