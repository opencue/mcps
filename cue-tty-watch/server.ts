#!/usr/bin/env bun
/**
 * cue-tty-watch — MCP server giving Claude eyes inside X displays and tmux panes.
 *
 * Tools:
 *   screenshot          → PNG of an X display (default :99 for Xvfb capture flows)
 *   tmux_pane           → text contents of a tmux pane
 *   send_keys_tmux      → tmux send-keys (Enter, Up, Down, "literal text", etc.)
 *   send_keys_xdotool   → xdotool key against a window by --class
 *   list_xwindows       → enumerate windows + their class on a display
 *
 * Designed for the kitty + Xvfb + tmux demo-capture pipeline in scripts/record-demo-kitty.sh.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { spawnSync } from "node:child_process";
import { z } from "zod";

const server = new McpServer(
  { name: "cue-tty-watch", version: "0.1.0" },
  { capabilities: { tools: {} } }
);

// ─── helpers ─────────────────────────────────────────────────────────────────

const MAX_BUF = 100 * 1024 * 1024;

function err(text: string) {
  return { content: [{ type: "text" as const, text }], isError: true };
}

function text(text: string) {
  return { content: [{ type: "text" as const, text }] };
}

function image(base64: string) {
  return { content: [{ type: "image" as const, data: base64, mimeType: "image/png" }] };
}

// ─── 1. screenshot ───────────────────────────────────────────────────────────

server.tool(
  "screenshot",
  "Capture a frame of an X display as a PNG. Use this to SEE what's actually rendering inside a kitty/tmux/Xvfb session. Default display ':99' matches the Xvfb capture pipeline in scripts/record-demo-kitty.sh. Image is downscaled to max 1400px width to keep payload reasonable.",
  {
    display: z.string().default(":99").describe("X display, e.g. ':99' (Xvfb) or ':0' (real)"),
    max_width: z.number().int().min(200).max(2400).default(1400).describe("Resize to at most this width"),
  },
  async ({ display, max_width }) => {
    const xwd = spawnSync("xwd", ["-root", "-silent", "-display", display], {
      stdio: ["ignore", "pipe", "pipe"],
      maxBuffer: MAX_BUF,
    });
    if (xwd.status !== 0) return err(`xwd failed (display ${display}): ${xwd.stderr?.toString() ?? "no output"}`);

    const conv = spawnSync("convert", ["xwd:-", "-resize", `${max_width}>`, "png:-"], {
      input: xwd.stdout,
      stdio: ["pipe", "pipe", "pipe"],
      maxBuffer: MAX_BUF,
    });
    if (conv.status !== 0) return err(`ImageMagick convert failed: ${conv.stderr?.toString() ?? "no output"}`);

    return image(conv.stdout.toString("base64"));
  }
);

// ─── 2. tmux_pane ────────────────────────────────────────────────────────────

server.tool(
  "tmux_pane",
  "Read the current rendered text of a tmux pane. Use to verify what command was typed, what output appeared, whether a prompt is waiting.",
  {
    socket: z.string().default("").describe("tmux -L socket name (e.g. 'cue-demo'). Empty = default socket."),
    session: z.string().describe("Session name, e.g. 'demo'"),
    target: z.string().default("0").describe("Window.pane target, e.g. '0' or '0.1'"),
    history_lines: z.number().int().min(0).max(5000).default(0).describe("Include this many scrollback lines (0 = visible only)"),
  },
  async ({ socket, session, target, history_lines }) => {
    const args: string[] = [];
    if (socket) args.push("-L", socket);
    args.push("capture-pane", "-p", "-t", `${session}:${target}`);
    if (history_lines > 0) args.push("-S", `-${history_lines}`);

    const res = spawnSync("tmux", args, { encoding: "utf8" });
    if (res.status !== 0) return err(`tmux capture-pane failed: ${res.stderr}`);
    return text(res.stdout || "(empty pane)");
  }
);

// ─── 3. send_keys_tmux ───────────────────────────────────────────────────────

server.tool(
  "send_keys_tmux",
  "Send keystrokes into a tmux pane via tmux send-keys. Each item in 'keys' is a separate argument: 'Enter', 'Up', 'Down', 'C-c', 'BSpace', or literal text strings.",
  {
    socket: z.string().default("").describe("tmux -L socket name. Empty = default socket."),
    session: z.string().describe("Session name"),
    target: z.string().default("0").describe("Window.pane target"),
    keys: z.array(z.string()).min(1).describe("Array of args passed to tmux send-keys. Example: ['echo hi', 'Enter']"),
  },
  async ({ socket, session, target, keys }) => {
    const args: string[] = [];
    if (socket) args.push("-L", socket);
    args.push("send-keys", "-t", `${session}:${target}`, ...keys);

    const res = spawnSync("tmux", args, { encoding: "utf8" });
    if (res.status !== 0) return err(`tmux send-keys failed: ${res.stderr}`);
    return text(`sent ${keys.length} arg(s) to ${session}:${target}`);
  }
);

// ─── 4. send_keys_xdotool ────────────────────────────────────────────────────

server.tool(
  "send_keys_xdotool",
  "Send keystrokes directly to an X window matched by WM_CLASS. Use when targeting a kitty window before tmux is attached, or for keys tmux can't pass cleanly.",
  {
    display: z.string().default(":99"),
    window_class: z.string().describe("WM_CLASS to match (e.g. 'cue-demo')"),
    keys: z.array(z.string()).min(1).describe("xdotool key specs, e.g. ['Down', 'Down', 'Return']"),
    delay_ms: z.number().int().min(0).max(2000).default(80).describe("Inter-key delay"),
  },
  async ({ display, window_class, keys, delay_ms }) => {
    const env = { ...process.env, DISPLAY: display };
    const find = spawnSync("xdotool", ["search", "--class", window_class], { env, encoding: "utf8" });
    if (find.status !== 0 || !find.stdout.trim()) {
      return err(`No window matching class '${window_class}' on display ${display}`);
    }
    const wid = find.stdout.trim().split("\n")[0]!;

    for (const k of keys) {
      const r = spawnSync("xdotool", ["key", "--window", wid, "--delay", String(delay_ms), k], { env });
      if (r.status !== 0) return err(`xdotool key '${k}' failed`);
    }
    return text(`sent ${keys.length} key(s) to window ${wid} (class=${window_class})`);
  }
);

// ─── 5. list_xwindows ────────────────────────────────────────────────────────

server.tool(
  "list_xwindows",
  "List X windows on a display with their class and geometry. Use to find the right window_class before sending keys.",
  {
    display: z.string().default(":99"),
  },
  async ({ display }) => {
    const env = { ...process.env, DISPLAY: display };
    const search = spawnSync("xdotool", ["search", ".*"], { env, encoding: "utf8" });
    if (search.status !== 0) return err(`xdotool search failed: ${search.stderr}`);

    const wids = search.stdout.trim().split("\n").filter(Boolean);
    if (!wids.length) return text("(no windows)");

    const rows: string[] = [];
    rows.push("WID         CLASS                          GEOMETRY");
    for (const wid of wids) {
      const cls = spawnSync("xdotool", ["getwindowclassname", wid], { env, encoding: "utf8" });
      const geo = spawnSync("xdotool", ["getwindowgeometry", "--shell", wid], { env, encoding: "utf8" });
      const className = (cls.stdout || "").trim();
      if (!className) continue; // skip unmapped / decoration-only windows

      const geoVars: Record<string, string> = {};
      for (const line of (geo.stdout || "").split("\n")) {
        const m = line.match(/^(\w+)=(.+)$/);
        if (m) geoVars[m[1]!] = m[2]!;
      }
      const geomStr = geoVars.WIDTH && geoVars.HEIGHT
        ? `${geoVars.WIDTH}x${geoVars.HEIGHT}+${geoVars.X ?? "?"}+${geoVars.Y ?? "?"}`
        : "?";
      rows.push(`${wid.padEnd(11)} ${className.padEnd(30)} ${geomStr}`);
    }
    return text(rows.join("\n"));
  }
);

// ─── start ───────────────────────────────────────────────────────────────────

const transport = new StdioServerTransport();
await server.connect(transport);
