# solidcraft

SolidCraft parametric CAD over MCP (stdio). Runs `solidcraft-cli mcp`: bridges to the open SolidCraft app when its control channel is on, otherwise starts a headless design session. Tools appear as `mcp__solidcraft__*`. https://github.com/tangency-labs/solidcraft

## Requirements

- `solidcraft-cli` on the login shell's `PATH`. The Linux AppImage writes a launcher to
  `~/.local/bin/solidcraft-cli` on its first run; deb/rpm put it in `/usr/bin`; the macOS
  app links it into `/opt/homebrew/bin` or `/usr/local/bin`. Snap and Flatpak keep it off
  `PATH` (`solidcraft.cli`, `flatpak run --command=solidcraft-cli io.tangencylabs.solidcraft`);
  change the command in this entry for those.
- To watch the agent model in the open app, turn on Preferences > Assistant > Agents
  through MCP > "Let AI agents connect". With it off, the server runs headless.

## Designs folder

The server only reads and writes inside the open design's folder, its own scratch and
recovery folders, and folders passed with `--allow-path`, so a new headless design has
nowhere to save. This entry creates and allows one designs folder:
`$SOLIDCRAFT_DESIGNS`, default `~/Documents/solidcraft`. Give `save` and `export` absolute
paths inside it; relative paths are refused.

## Related skill

`cad/solidcraft` in the cue skills library.
