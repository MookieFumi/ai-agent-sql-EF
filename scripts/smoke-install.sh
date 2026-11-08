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

echo "--- deployed skills (outside apm_modules)"
find . \( -path ./.git -o -path ./apm_modules \) -prune -o -name SKILL.md -print | sort

echo "--- deployed agents and other files (outside apm_modules, excluding skills)"
find . \( -path ./.git -o -path ./apm_modules \) -prune -o -type f -not -name SKILL.md -not -path '*/references/*' -not -name apm.yml -not -name apm.lock.yaml -print | sort

# Every deployed location must contain every skill; a location is the folder that holds the skill folders.
status=0
for location in $(find . \( -path ./.git -o -path ./apm_modules \) -prune -o -name SKILL.md -print | sed -E 's#/[^/]+/SKILL.md$##' | sort -u); do
  count="$(find "${location}" -maxdepth 2 -name SKILL.md | wc -l)"
  echo "${location}: ${count} skills (expected ${expected})"
  if [ "${count}" -ne "${expected}" ]; then
    status=1
  fi
done

if [ -z "$(find . \( -path ./.git -o -path ./apm_modules \) -prune -o -name SKILL.md -print)" ]; then
  echo "No skill was deployed outside apm_modules."
  status=1
fi
exit "${status}"
