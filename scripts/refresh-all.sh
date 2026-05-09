#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

./scripts/snapshot-mcps.py
./scripts/snapshot-mcp-skills.py
./scripts/check-mcp-health.py
./scripts/check-no-secrets.sh
git diff
