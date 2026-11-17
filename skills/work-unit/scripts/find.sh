#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 || -z ${2:-} ]]; then
  printf 'Usage: %s PROJECT_ROOT REFERENCE\n' "$0" >&2
  exit 2
fi

project_root=$(cd -- "$1" && pwd -P)
reference=$2
scripts_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
registry="$project_root/.agents/work-units"

if [[ ! -d "$registry" ]]; then
  printf 'Work-unit registry not found: %s\n' "$registry" >&2
  exit 1
fi

# Buffer output so a failed batch cannot produce a partial success response.
result=$(
  find "$registry" -maxdepth 1 -type f -name '*.json' \
    -exec jq -n --arg ref "$reference" -f "$scripts_dir/find.jq" {} + |
    jq -s 'add // []'
)
printf '%s\n' "$result"
