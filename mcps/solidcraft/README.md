# solidcraft

SolidCraft parametric CAD over MCP (stdio). Runs `solidcraft-cli mcp`: bridges to the open SolidCraft app when its control channel is on, otherwise starts a headless design session. Tools appear as `mcp__solidcraft__*`. https://github.com/tangency-labs/solidcraft

## Requirements

- `solidcraft-cli` on the login shell's `PATH`. The Linux AppImage writes a launcher to
  `~/.local/bin/solidcraft-cli` on its first run; deb/rpm put it in `/usr/bin`; the macOS
  app links it into `/opt/homebrew/bin` or `/usr/local/bin`.
- To watch the agent model in the open app, turn on Preferences > Assistant > Agents
  through MCP > "Let AI agents connect". With it off, the server runs headless.

## Related skill

`cad/solidcraft` in the cue skills library.
