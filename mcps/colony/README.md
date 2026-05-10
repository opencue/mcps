# colony MCP

Multi-agent coordination + memory layer. The MCP exposes the
`hivemind_context`, `attention_inbox`, `task_*`, `task_claim_file`,
`task_hand_off`, `task_post`, `agent_*`, and related coordination tools
that other agents use to claim files, hand off work, and post notes
across sessions.

## Source

- Repo: <https://github.com/recodeee/colony>
- npm package: `@imdeadpool/colony-cli` (published from `apps/cli/`)
- Current version on this workstation: run `colony --version` to check
  (the global symlink may lag behind the repo if you've been doing
  local dev — see `colony-rebuild` recipe in `~/Documents/Justfile`).

## Install

The colony onboarding is four steps, in order. The first three are
documented in the upstream README at <https://github.com/recodeee/colony>.

```sh
# 1. CLI — installs the `colony` binary
npm install -g @imdeadpool/colony-cli

# 2. MCP — registers the colony MCP server + lifecycle hooks for one IDE
colony install --ide codex            # or claude-code, cursor, gemini-cli

# 3. Skill — teaches skill-aware agents (Claude Code, Cursor, Codex) to
#    invoke colony first
npx skills add recodeee/colony/skills/colony-mcp

# 4. Verify
colony health
```

## MCP server registration

When the bouncer wires the colony MCP into a runtime config, the entry
shape is:

```text
command: colony
args: mcp
type: stdio
```

## Required env vars

```text
COLONY_HOME           # state + sqlite db root (default: ~/.colony)
```

## Related skills

```text
colony                  — wraps the contract: hivemind_context → attention_inbox
                          → task_ready_for_agent → claim files → note_working
                          → handoff before quota stop
gitguardex              — repo guardrail flow (gx status / doctor)
guardex-merge-skills-to-dev — multi-agent SKILL.md merge into dev
team                    — N coordinated agents on a shared task list
trace                   — chronological hook/keyword/skill/agent flow
worker                  — leader-spawned worker contract for $team
```

## Quick health check

```sh
command -v colony && colony --version && colony health
```

## Local-dev notes

If you're working from the recodee/colony source tree (rather than the
published npm package), the global `colony` binary is typically a
`npm link` symlink to `~/Documents/recodee/colony/apps/cli/dist/index.js`.
After a `git clean` or `pnpm dlx tsup --clean`, rebuild with:

```sh
just colony-rebuild
# = pnpm install && pnpm --filter @imdeadpool/colony-cli build
#   in ~/Documents/recodee/colony/
```

The `pnpm --filter @imdeadpool/colony-cli` matches the package.json
`name` field in `apps/cli/package.json`.
