# figma skills

`GLips/Figma-Context-MCP` (`figma-developer-mcp`, 15K★). Pulls Figma file
layout, components, styles, and frames into agent context so the agent can
turn a Figma design into accurate code instead of guessing from a screenshot.

## Setup

- Wired via npx: `npx -y figma-developer-mcp --stdio`. Needs Node.
- Required env: `FIGMA_API_KEY` (a Figma personal access token with file-read
  scope). Set it in the env field — the server also accepts a `--figma-api-key`
  flag, but cue config keeps secrets in `env`.

## Tools

- `get_figma_data` — fetch layout/metadata for a file or node (the main one).
- `download_figma_images` — pull image/SVG assets referenced in a node.

Pairs with the `designer` profile's image-to-code and redesign skills: give it
a Figma file URL/node and it grounds the generated UI in the real design tokens.
