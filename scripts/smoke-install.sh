#!/usr/bin/env bash
# Install this package into an empty project with APM and check that every skill arrives.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
expected="$(find "$repo/.apm/skills" -name SKILL.md | wc -l)"
consumer="$(mktemp -d)"

cd "$consumer"
cat > apm.yml <<'YAML'
name: consumer
version: "0.0.1"
targets:
  - copilot
  - claude
YAML
git init -q .

apm install "$repo" --verbose

echo "--- installed files"
find . -path ./.git -prune -o -type f -print | sort

found="$(find . -path ./.git -prune -o -name SKILL.md -print | wc -l)"
echo "SKILL.md files: expected at least ${expected}, found ${found}"
if [ "${found}" -lt "${expected}" ]; then
  echo "Not every skill was installed."
  exit 1
fi
