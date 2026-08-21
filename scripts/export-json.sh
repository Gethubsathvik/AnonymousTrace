#!/bin/bash
# python -m anonymoustrace.main - JSON Export
# Usage: scripts/export-json.sh <username> [sites...] [output.json]

if [ -z "$1" ]; then
    echo "Usage: export-json.sh <username> [site1] [site2] ... [output.json]"
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --json results.json
echo "JSON exported to results.json"

