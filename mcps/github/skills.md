# github skills

`github/github-mcp-server` (🎖️ official GitHub). Repository management, PRs,
issues, Actions, code search as callable tools.

## Setup

- Wired via Docker: `docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server`.
  Requires Docker installed and running.
- Required env: `GITHUB_PERSONAL_ACCESS_TOKEN` (fine-grained or classic PAT).
- Alternative if you prefer no Docker: GitHub's remote hosted MCP at
  `https://api.githubcopilot.com/mcp/` (HTTP transport — needs a different
  registry shape than this stdio entry; swap if/when cue supports http MCPs).

Overlaps the `github/github` skill + `gh` CLI; adds a structured tool surface.

Related skills: pairs with every dev profile's PR/issue workflows.
