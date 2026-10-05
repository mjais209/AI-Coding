#!/usr/bin/env bash
# Build every pattern and run its demo. Optional argument filters by name, e.g. ./run_all.sh observer
set -euo pipefail
cd "$(dirname "$0")"

cmake -S . -B build -DCMAKE_BUILD_TYPE=Release > /dev/null
cmake --build build -j > /dev/null

filter="${1:-}"
for category in creational structural behavioral; do
  for source in "$category"/*.cpp; do
    name="$(basename "$source" .cpp)"
    [[ -n "$filter" && "$name" != *"$filter"* ]] && continue
    echo
    echo "=== $category: $name ==="
    head -n 1 "$source" | sed 's|^// ||'
    echo "------------------------------------------------------------"
    "./build/$name"
  done
done
