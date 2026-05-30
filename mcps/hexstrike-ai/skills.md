# HexStrike AI MCP

Autonomous offensive-security MCP: lets the agent drive 150+ pentest/recon
tools (nmap, masscan, rustscan, amass, subfinder, nuclei, gobuster, ffuf,
sqlmap, wpscan, radare2, ghidra, john, hashcat, hydra, prowler, trivy, …) for
authorized pentesting, vuln discovery, and bug-bounty automation.

- Repo: [github.com/0x4m4/hexstrike-ai](https://github.com/0x4m4/hexstrike-ai)
- License: MIT
- Type: `local` (two-part: HTTP backend + stdio MCP bridge)
- Used by profile: `cybersecurity`

## ⚠️ Authorization

This MCP can scan, fuzz, exploit, and crack against real targets. Only point it
at systems you are **explicitly authorized** to test (your own infra, a signed
pentest engagement, or an in-scope bug-bounty program). Unauthorized use is
illegal. Wiring the MCP does nothing on its own — it acts only when you invoke a
tool against a target.

## Architecture

Two processes:

1. **Backend** — `hexstrike_server.py`, an HTTP server on `:8888` that hosts the
   tools. You start this yourself; it is not spawned by cue.
2. **MCP bridge** — `hexstrike_mcp.py --server http://localhost:8888`, a stdio
   MCP server that cue registers and Claude Code launches. It talks to the
   backend. If the backend isn't running, the bridge starts but tool calls fail.

## One-time setup

cue's registry entry expects the clone at `~/.config/cue/cache/hexstrike-ai`
with its venv at `hexstrike-env/` (mirrors the `cve-search` convention):

```bash
git clone https://github.com/0x4m4/hexstrike-ai.git ~/.config/cue/cache/hexstrike-ai
cd ~/.config/cue/cache/hexstrike-ai
python3 -m venv hexstrike-env
./hexstrike-env/bin/pip install -r requirements.txt
```

Install the underlying security tools separately (most are in Kali/`apt`/`brew`;
the repo lists the full set). Missing tools just disable the matching MCP tools.

## Per-session: start the backend

```bash
~/.config/cue/cache/hexstrike-ai/hexstrike-env/bin/python3 \
  ~/.config/cue/cache/hexstrike-ai/hexstrike_server.py            # add --debug / --port as needed
```

Then launch `claude` under the `cybersecurity` profile — the `hexstrike-ai` MCP
bridge connects to `http://localhost:8888`.

## Health

`cue mcps health` will show the bridge as up only when the backend on `:8888`
is reachable.
