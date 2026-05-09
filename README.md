# recodeee mcps

Canonical, sanitized inventory of MCP server configuration used across local agents and editors.

## What is tracked

- MCP server names
- commands and arguments
- environment variable names
- source config paths
- install/setup notes

## What is not tracked

- API keys
- tokens
- passwords
- local credential files
- raw unredacted agent settings

## Snapshot

Refresh the sanitized inventory from this machine:

```sh
./scripts/snapshot-mcps.py
```

Generated files:

```text
configs/codex.sanitized.json
configs/claude.sanitized.json
configs/vscode.sanitized.json
docs/inventory.md
```

Review diffs before pushing. If a secret appears, remove it before commit.
