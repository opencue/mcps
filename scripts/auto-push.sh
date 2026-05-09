#!/usr/bin/env bash
# Auto-push for the mcps repo.
#
# Runs after each Claude turn (Stop hook) and from the systemd backstop timer.
# If `mcps/`, `configs/`, `templates/`, `docs/`, or `README.md` have
# uncommitted changes, auto-commits and pushes to origin/main.
#
# Silent on no-op. Best-effort: never blocks the session.
# Disable per-session by exporting MCPS_AUTO_PUSH=0.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if [[ "${MCPS_AUTO_PUSH:-1}" == "0" ]]; then
  exit 0
fi

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
git remote get-url origin >/dev/null 2>&1 || exit 0

# Skip during rebase/merge
if [[ -d .git/rebase-merge ]] || [[ -d .git/rebase-apply ]] || [[ -f .git/MERGE_HEAD ]]; then
  exit 0
fi

paths_to_stage=()
for p in mcps configs templates docs README.md .gitignore scripts; do
  [[ -e "$p" ]] && paths_to_stage+=("$p")
done

[[ ${#paths_to_stage[@]} -eq 0 ]] && exit 0

git add -A "${paths_to_stage[@]}" 2>/dev/null || exit 0

if git diff --cached --quiet; then
  exit 0
fi

short_summary() {
  local added modified renamed deleted
  added=$(git diff --cached --name-only --diff-filter=A | wc -l | tr -d ' ')
  modified=$(git diff --cached --name-only --diff-filter=M | wc -l | tr -d ' ')
  renamed=$(git diff --cached --name-only --diff-filter=R | wc -l | tr -d ' ')
  deleted=$(git diff --cached --name-only --diff-filter=D | wc -l | tr -d ' ')

  local parts=()
  [[ "$added"    -gt 0 ]] && parts+=("+$added added")
  [[ "$modified" -gt 0 ]] && parts+=("~$modified modified")
  [[ "$renamed"  -gt 0 ]] && parts+=("→$renamed renamed")
  [[ "$deleted"  -gt 0 ]] && parts+=("-$deleted deleted")

  IFS=', '
  echo "${parts[*]}"
}

summary="$(short_summary)"
top_paths=$(git diff --cached --name-only | awk -F/ '{print $1}' | sort -u | head -3 | tr '\n' ',' | sed 's/,$//')

git commit -q -m "auto: mcps sync — ${summary} (${top_paths})" 2>/dev/null || exit 0

git push --quiet origin main 2>/dev/null || {
  echo "[mcps auto-push] push failed; commit is local on $(git rev-parse --abbrev-ref HEAD)" >&2
  exit 0
}

echo "[mcps auto-push] pushed: ${summary}" >&2
