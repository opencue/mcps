#!/usr/bin/env bun
/**
 * agentshield — MCP wrapper around the `ecc-agentshield` CLI.
 *
 * Tools:
 *   scan          → run `ecc-agentshield scan --format json` against a path
 *                   and return parsed findings.
 *   scan_summary  → same scan, but return only grade + counts (low-token).
 *   list_rules    → list rule categories and counts the scanner can flag.
 *
 * Discovers the CLI via (in order): $AGENTSHIELD_BIN, `agentshield` on PATH,
 * `npx -y ecc-agentshield`. The npx fallback is slower on first run but
 * needs no install.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { spawnSync } from "node:child_process";
import { z } from "zod";

const server = new McpServer(
  { name: "agentshield", version: "0.1.0" },
  { capabilities: { tools: {} } },
);

const MAX_BUF = 32 * 1024 * 1024;

function text(value: string) {
  return { content: [{ type: "text" as const, text: value }] };
}

function err(value: string) {
  return { content: [{ type: "text" as const, text: value }], isError: true };
}

// Resolve the agentshield invocation. Returns [cmd, ...args] suitable for spawn.
function resolveBin(): string[] {
  const fromEnv = process.env.AGENTSHIELD_BIN;
  if (fromEnv && fromEnv.length > 0) return [fromEnv];

  const which = spawnSync("which", ["agentshield"], { stdio: ["ignore", "pipe", "ignore"] });
  if (which.status === 0) {
    const path = which.stdout.toString().trim();
    if (path.length > 0) return [path];
  }
  return ["npx", "-y", "ecc-agentshield"];
}

type ScanArgs = {
  path?: string;
  fix?: boolean;
};

function runScan(args: ScanArgs): { ok: true; data: unknown } | { ok: false; reason: string } {
  const bin = resolveBin();
  const cliArgs = [...bin.slice(1), "scan", "--format", "json"];
  if (args.path) cliArgs.push("--path", args.path);
  if (args.fix) cliArgs.push("--fix");

  const res = spawnSync(bin[0]!, cliArgs, {
    stdio: ["ignore", "pipe", "pipe"],
    maxBuffer: MAX_BUF,
    timeout: 120_000,
  });

  // agentshield exits non-zero when findings exist; that's not a failure for us.
  // A genuine failure is no JSON on stdout or a spawn error.
  if (res.error) return { ok: false, reason: `spawn failed: ${res.error.message}` };
  const stdout = res.stdout?.toString() ?? "";
  if (!stdout.trim()) {
    const stderr = res.stderr?.toString() ?? "";
    return { ok: false, reason: stderr || `agentshield produced no output (exit ${res.status})` };
  }
  try {
    return { ok: true, data: JSON.parse(stdout) };
  } catch (e) {
    return { ok: false, reason: `failed to parse agentshield JSON: ${(e as Error).message}` };
  }
}

server.tool(
  "scan",
  "Run AgentShield against a directory (e.g. a project's .claude/, .codex/, repo root) and return the full JSON report — grade, score breakdown, and every finding. Use when the user wants to audit an agent configuration for secrets, permission misconfigs, hook injection, MCP supply-chain risks, or prompt-injection vectors. Discovery auto-skips node_modules and build output.",
  {
    path: z.string().optional().describe("Directory or file to scan. Omit to scan the auto-discovered ~/.claude/ tree."),
    fix: z.boolean().default(false).describe("Apply safe auto-fixes (mainly: replace hardcoded secrets with ${ENV_VAR} references). Mutates files."),
  },
  async ({ path, fix }) => {
    const out = runScan({ path, fix });
    if (!out.ok) return err(`agentshield scan failed: ${out.reason}`);
    return text(JSON.stringify(out.data, null, 2));
  },
);

server.tool(
  "scan_summary",
  "Run AgentShield and return ONLY a compact summary: grade, total score, per-category score, and finding counts by severity. Use for a quick health check when full findings would blow the context budget.",
  {
    path: z.string().optional().describe("Directory or file to scan. Omit to auto-discover ~/.claude/."),
  },
  async ({ path }) => {
    const out = runScan({ path });
    if (!out.ok) return err(`agentshield scan failed: ${out.reason}`);
    const data = out.data as Record<string, unknown>;
    const findings = Array.isArray(data.findings) ? (data.findings as Array<{ severity?: string }>) : [];
    const counts: Record<string, number> = { critical: 0, high: 0, medium: 0, low: 0, info: 0 };
    for (const f of findings) {
      const sev = (f.severity ?? "info").toLowerCase();
      counts[sev] = (counts[sev] ?? 0) + 1;
    }
    return text(
      JSON.stringify(
        {
          grade: data.grade,
          score: data.score,
          breakdown: data.breakdown ?? data.scoreBreakdown,
          findings_total: findings.length,
          findings_by_severity: counts,
          files_scanned: data.filesScanned ?? data.files_scanned,
        },
        null,
        2,
      ),
    );
  },
);

server.tool(
  "list_rules",
  "List AgentShield's rule categories and per-category rule counts. Use when the user asks 'what does it check?' before running a scan.",
  {},
  async () => {
    return text(
      JSON.stringify(
        {
          categories: [
            { name: "secrets", rules: 10, scope: "API keys, tokens, passwords, env exposure, webhooks, private keys, base64 creds, internal IPs" },
            { name: "permissions", rules: 10, scope: "allow/deny analysis, dangerous flags, destructive git, mutable tools, sensitive paths, network access" },
            { name: "hooks", rules: 34, scope: "injection, exfiltration, persistence, container escape, clipboard, log tampering, reverse shells" },
            { name: "mcp", rules: 23, scope: "risky servers, env override, npx supply chain, auto-approve, timeout, bind-all, CORS" },
            { name: "agents", rules: 25, scope: "tool restriction gaps, prompt injection, reflection attacks, output manipulation, social engineering" },
          ],
          severity_deductions: { critical: -25, high: -15, medium: -5, low: -2, info: 0 },
          grade_thresholds: { A: 90, B: 75, C: 60, D: 40, F: 0 },
        },
        null,
        2,
      ),
    );
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
