#!/bin/bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
directory="$repo_root/logs"

if [ ! -d "$directory" ]; then
  mkdir -p "$directory"
fi

docker compose -f "$repo_root/deploy/docker-compose.yml" logs --tail=all \
  | sort -t'|' -k2.13,2.20 \
  > "$directory/$(date +%Y-%m-%d_%H-%M-%S)_all_containers.log"

echo "Logs saved to 'logs' directory."