# cue-tty-watch

> MCP server that gives Claude eyes inside X displays and tmux panes.

Built for the kitty + Xvfb + tmux GIF-capture pipeline ([`scripts/record-demo-kitty.sh`](../../../scripts/record-demo-kitty.sh)) where the only way to know what the headless terminal is doing was to wait for a human to take a screenshot. With this MCP, Claude can `screenshot` and `tmux_pane` directly.

## Tools

| Tool | Purpose | Returns |
|---|---|---|
| `screenshot` | PNG of an X display (default `:99`) | Image |
| `tmux_pane` | Rendered text of a tmux pane | Text |
| `send_keys_tmux` | `tmux send-keys` into a pane | Text confirmation |
| `send_keys_xdotool` | `xdotool key` to a window by class | Text confirmation |
| `list_xwindows` | Windows on a display + their class/geom | Text table |

## Requirements

Already on most Linux dev boxes; install with `apt` if missing:

```bash
sudo apt install xvfb x11-apps imagemagick xdotool
# tmux and bun should already be there
```

The `xwd` binary (from `x11-apps`) is what captures the display; ImageMagick's `convert` turns the XWD blob into PNG.

## Install dependencies

```bash
cd resources/mcps/cue-tty-watch
bun install
```

## Register with Claude Code

Add to your `~/.claude.json` (or `~/.config/claude/claude.json`) under `mcpServers`:

```json
{
  "mcpServers": {
    "cue-tty-watch": {
      "command": "/absolute/path/to/cue/resources/mcps/cue-tty-watch/bin/cue-tty-watch"
    }
  }
}
```

Then **restart Claude Code** for the MCP to load.

## Register with cue profile

Add to any profile's `profile.yaml` that needs it (typically `readme-writer` for demo recording):

```yaml
mcps:
  - cue-tty-watch
```

## Usage from Claude

Once registered, Claude can call:

```
screenshot(display=":99")                                    # → see what's on Xvfb
tmux_pane(socket="cue-demo", session="demo")                 # → see what tmux is showing
send_keys_tmux(socket="cue-demo", session="demo",
               keys=["cue list", "Enter"])                   # → drive a demo
list_xwindows(display=":99")                                 # → find a window by class
```

## Why this exists

Claude Code's built-in tools (`Bash`, `Read`, `Write`, etc.) can run commands and read files but can't *see* a graphical session. When debugging the kitty-graphics GIF capture, every iteration meant: run script (~50 s), wait for a human screenshot, infer what went wrong, patch, repeat.

With this MCP, the loop is: `send_keys → screenshot → adjust → send_keys → screenshot`, all inside one Claude turn.

## License

MIT (same as parent repo).
