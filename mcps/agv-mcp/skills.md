# agv-mcp

AGV3-specific MCP adapter backed by the `agvc` CLI. The server source lives at
`~/Documents/AGV3/AGV-cuda/tools/agv_mcp` and is launched as an installable
Python project with `uv run ... agv-mcp`.

Use it for structured, stage-aware AGV status, doctor, graph-contract validation,
duplicate node/publisher detection, parsed topic messages, rich/freshness-aware TF,
and component logs. Its read-only tools should be preferred before any mutation.

Lifecycle changes use a two-step protocol: prepare the exact operation, show its
impact and resolved robot identity to the operator, then execute the short-lived,
single-use token only after explicit confirmation. A boolean `confirmed` value is
not authorization. Operations are appended to the MCP audit log.

Motor arming, `/cmd_vel`, navigation goals, arbitrary mutating services, and
arbitrary parameter writes are intentionally not exposed, even with a token. Do
not bypass that boundary with generic ROS, SSH, or Docker tools.

## Runtime

The registry uses `bash -lc` because MCP clients do not consistently expand
`${HOME}` in command arguments. The shell resolves the portable checkout path and
sets `AGVC_BIN` to `$HOME/.local/bin/agvc` unless the runtime already supplied an
override. No secret is stored in the registry.

The launcher inherits optional target selectors `AGVC_ROBOT`, `AGVC_HOST`,
`AGVC_IP`, and `AGVC_CONTAINER` from the client environment. It intentionally
does not embed robot addresses or credentials. Security state is configurable via
`AGV_MCP_TOKEN_DIR`, `AGV_MCP_AUDIT_LOG`, and
`AGV_MCP_CONFIRMATION_TTL_SECONDS`; when omitted, the server uses its safe local
defaults under `~/.local/state/agv-mcp/` (`tokens/` and `audit.jsonl`). Keep token
and audit state out of source control, and never disclose token contents.
