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
import { readFileSync } from "node:fs";
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

// ─── 6. find_text ────────────────────────────────────────────────────────────
// Tesseract OCR with bounding boxes. The killer tool for redaction work:
// give it an image + a substring query, get back where that text is in the frame.

server.tool(
  "find_text",
  "Run tesseract OCR on an image and return the bounding boxes of any words/lines that match `query` (substring, case-insensitive). Use this to locate text dynamically — e.g. find where an email row is in each video frame so you can mask it.",
  {
    image_path: z.string().describe("Absolute path to a PNG/JPG"),
    query: z.string().describe("Case-insensitive substring to match against OCR text"),
    level: z.enum(["word", "line", "paragraph"]).default("line").describe("Granularity of returned boxes"),
  },
  async ({ image_path, query, level }) => {
    // tesseract tsv output gives per-word coords; line/para need post-aggregation
    const out = spawnSync("tesseract", [image_path, "stdout", "-l", "eng", "tsv"], {
      encoding: "utf8",
      maxBuffer: MAX_BUF,
    });
    if (out.status !== 0) return err(`tesseract failed: ${out.stderr}`);

    type Row = { level: number; page: number; block: number; par: number; line: number; word: number; left: number; top: number; width: number; height: number; conf: number; text: string };
    const rows: Row[] = [];
    const lines = out.stdout.split("\n");
    const header = lines[0]!.split("\t");
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i]!.split("\t");
      if (cols.length < header.length) continue;
      const r: any = {};
      for (let j = 0; j < header.length; j++) r[header[j]!] = cols[j];
      rows.push({
        level: +r.level, page: +r.page_num, block: +r.block_num, par: +r.par_num,
        line: +r.line_num, word: +r.word_num,
        left: +r.left, top: +r.top, width: +r.width, height: +r.height,
        conf: +r.conf, text: r.text || "",
      });
    }

    const wantLevel = level === "word" ? 5 : level === "line" ? 4 : 3;
    const q = query.toLowerCase();

    // Aggregate words within each line/paragraph and check if combined text contains query
    const groups = new Map<string, Row[]>();
    for (const r of rows) {
      if (r.level !== 5) continue;            // only words have text
      const key = level === "word"
        ? `${r.block}-${r.par}-${r.line}-${r.word}`
        : level === "line"
          ? `${r.block}-${r.par}-${r.line}`
          : `${r.block}-${r.par}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(r);
    }

    const matches: Array<{ text: string; x: number; y: number; w: number; h: number; conf: number }> = [];
    for (const [, words] of groups) {
      const combined = words.map((w) => w.text).join(" ").trim();
      if (!combined.toLowerCase().includes(q)) continue;
      const x = Math.min(...words.map((w) => w.left));
      const y = Math.min(...words.map((w) => w.top));
      const right = Math.max(...words.map((w) => w.left + w.width));
      const bottom = Math.max(...words.map((w) => w.top + w.height));
      const avgConf = words.reduce((s, w) => s + w.conf, 0) / words.length;
      matches.push({ text: combined, x, y, w: right - x, h: bottom - y, conf: Math.round(avgConf) });
    }

    if (!matches.length) return text(`No matches for "${query}".`);
    return text(JSON.stringify(matches, null, 2));
  }
);

// ─── 7. ask_about_image ──────────────────────────────────────────────────────
// Vision Q&A via ollama + moondream. Fast yes/no-style queries about a screenshot.

server.tool(
  "ask_about_image",
  "Ask a question about an image using the moondream vision LLM (via ollama). Best for binary/categorical questions: 'is the splash visible?', 'is there a redaction box?', 'what state is this UI in?'. Returns the model's text answer.",
  {
    image_path: z.string().describe("Absolute path to a PNG/JPG"),
    question: z.string().describe("The question to ask about the image"),
    model: z.string().default("moondream").describe("ollama model name"),
  },
  async ({ image_path, question, model }) => {
    const imgB64 = readFileSync(image_path).toString("base64");
    const body = JSON.stringify({ model, prompt: question, images: [imgB64], stream: false });
    const r = spawnSync("curl", [
      "-sS", "-X", "POST",
      "http://localhost:11434/api/generate",
      "-H", "Content-Type: application/json",
      "-d", "@-",
    ], { input: body, encoding: "utf8", maxBuffer: MAX_BUF });
    if (r.status !== 0) return err(`ollama call failed: ${r.stderr}`);
    try {
      const j = JSON.parse(r.stdout);
      return text((j.response ?? "").trim() || "(empty response)");
    } catch {
      return err(`Bad JSON from ollama: ${r.stdout.slice(0, 200)}`);
    }
  }
);

// ─── 8. detect_scenes ────────────────────────────────────────────────────────
// PySceneDetect: find scene cut timestamps in a video. Use to discover
// "splash appears at t=22", "response renders at t=28" automatically.

server.tool(
  "detect_scenes",
  "Run PySceneDetect (content-aware) on a video file and return scene cut timestamps. Use to discover scene boundaries (splash appears / scrolls / response renders) without manual probing.",
  {
    video_path: z.string().describe("Absolute path to an MP4/MKV/etc"),
    threshold: z.number().min(1).max(100).default(27).describe("Content detector threshold (lower = more sensitive)"),
    python: z.string().default(`${process.env.HOME}/.venvs/video/bin/python`).describe("Python interpreter (must have scenedetect installed)"),
  },
  async ({ video_path, threshold, python }) => {
    const script = `
import sys, json
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
video = open_video(sys.argv[1])
sm = SceneManager()
sm.add_detector(ContentDetector(threshold=float(sys.argv[2])))
sm.detect_scenes(video)
scenes = sm.get_scene_list()
print(json.dumps([{"start": s[0].get_seconds(), "end": s[1].get_seconds()} for s in scenes]))
`;
    const r = spawnSync(python, ["-c", script, video_path, String(threshold)], { encoding: "utf8", maxBuffer: MAX_BUF });
    if (r.status !== 0) return err(`scenedetect failed: ${r.stderr}`);
    return text(r.stdout.trim() || "[]");
  }
);

// ─── 9. redact_video ─────────────────────────────────────────────────────────
// THE big tool: walks the video, OCRs each frame, finds the query text,
// builds a per-frame drawbox filter, and outputs a redacted mp4.

server.tool(
  "redact_video",
  "Auto-redact a moving text region across a whole video. Samples N frames per second, OCRs each one with tesseract to find `query`, then renders an output video where the matched region is covered with a styled placeholder box on every frame the text appears. Solves the 'email scrolls up and my drawbox is in the wrong place' problem in one call.",
  {
    input_path: z.string().describe("Source MP4 path"),
    output_path: z.string().describe("Destination MP4 path"),
    query: z.string().describe("Substring to find and redact (e.g. 'webubusiness')"),
    label: z.string().default("[ redacted ]").describe("Text to show inside the redaction box"),
    samples_per_second: z.number().int().min(1).max(30).default(4).describe("How many OCR samples per second"),
    python: z.string().default(`${process.env.HOME}/.venvs/video/bin/python`),
    pad: z.number().int().default(6).describe("Pixels of padding around detected bbox"),
  },
  async ({ input_path, output_path, query, label, samples_per_second, python, pad }) => {
    const script = `
import sys, json, subprocess, tempfile, os, re
from pathlib import Path

inp, outp, query, label, sps, pad = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6])

# 1. probe duration + fps
probe = subprocess.run(['ffprobe','-v','error','-select_streams','v:0',
    '-show_entries','stream=duration,r_frame_rate','-of','json',inp],
    capture_output=True, text=True, check=True)
meta = json.loads(probe.stdout)['streams'][0]
num,den = meta['r_frame_rate'].split('/')
fps = float(num)/float(den)
duration = float(meta['duration'])

# 2. extract sample frames + OCR each
tmpdir = tempfile.mkdtemp(prefix='redact-')
boxes = []  # list of (t_start, t_end, x, y, w, h)
step = 1.0 / sps
t = 0.0
prev = None
while t < duration:
    f = f"{tmpdir}/f-{t:.3f}.png"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{t}','-i',inp,
                    '-frames:v','1',f], check=True)
    tsv = subprocess.run(['tesseract',f,'stdout','-l','eng','tsv'],
                         capture_output=True, text=True).stdout
    found = None
    lines = {}
    for row in tsv.split('\\n')[1:]:
        c = row.split('\\t')
        if len(c) < 12 or not c[11].strip(): continue
        key = (c[2],c[3],c[4])
        lines.setdefault(key, []).append((int(c[6]),int(c[7]),int(c[8]),int(c[9]),c[11]))
    for key,words in lines.items():
        combined = ' '.join(w[4] for w in words).lower()
        if query.lower() in combined:
            x = min(w[0] for w in words)
            y = min(w[1] for w in words)
            r = max(w[0]+w[2] for w in words)
            b = max(w[1]+w[3] for w in words)
            found = (x-pad, y-pad, r-x+2*pad, b-y+2*pad)
            break
    if found != prev:
        if prev is not None:
            boxes[-1] = (boxes[-1][0], t, *boxes[-1][2:])
        if found is not None:
            boxes.append((t, duration, *found))
        prev = found
    t += step

# remove tmp frames
import shutil; shutil.rmtree(tmpdir)

# 3. build the drawbox+drawtext filter chain
filters = []
F = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
for (ts, te, x, y, w, h) in boxes:
    en = f"between(t,{ts:.3f},{te:.3f})"
    filters.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0x334155:t=1:enable='{en}'")
    filters.append(f"drawbox=x={x+1}:y={y+1}:w={w-2}:h={h-2}:color=0x14141e:t=fill:enable='{en}'")
    filters.append(f"drawtext=text='{label}':fontcolor=0x94a3b8:fontsize=13:x={x}+({w}-text_w)/2:y={y}+({h}-text_h)/2:enable='{en}':fontfile={F}")
vf = ','.join(filters) if filters else 'null'

# 4. encode
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',inp,'-vf',vf,
                '-c:v','libx264','-preset','medium','-pix_fmt','yuv420p',outp],
               check=True)
print(json.dumps({"boxes_found": len(boxes), "boxes": [{"t_start":ts,"t_end":te,"x":x,"y":y,"w":w,"h":h} for (ts,te,x,y,w,h) in boxes]}))
`;
    const r = spawnSync(python, ["-c", script, input_path, output_path, query, label, String(samples_per_second), String(pad)], {
      encoding: "utf8", maxBuffer: MAX_BUF,
    });
    if (r.status !== 0) return err(`redact_video failed: ${r.stderr}`);
    return text(r.stdout.trim());
  }
);

// ─── start ───────────────────────────────────────────────────────────────────

const transport = new StdioServerTransport();
await server.connect(transport);
