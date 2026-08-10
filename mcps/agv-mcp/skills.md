# agv-mcp

AGV3-specific MCP adapter backed by the `agvc` CLI. The server source lives at
`~/Documents/AGV3/AGV-cuda/tools/agv_mcp` and is launched as an installable
Python project with `uv run ... agv-mcp`.

Use it for structured AGV status, doctor, stage status, ROS node/topic/TF/parameter
inspection, component logs, and confirmation-gated lifecycle operations. Its
read-only tools should be preferred before any mutation. Bringup, stop, mapping,
localization, deploy, and map saving require explicit operator confirmation.

Motor arming, `/cmd_vel`, and navigation-goal tools are intentionally not exposed.
Do not bypass that boundary with generic ROS tools.

## Runtime

The registry uses `bash -lc` because MCP clients do not consistently expand
`${HOME}` in command arguments. The shell resolves the portable checkout path and
sets `AGVC_BIN` to `$HOME/.local/bin/agvc` unless the runtime already supplied an
override. No secret is stored in the registry.
