#!/bin/bash
# python -m anonymoustrace.main - Confidence Filter
# Usage: scripts/confidence-filter.sh <username> <confidence_level> [sites...]
# Levels: found, likely, unknown

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: confidence-filter.sh <username> <confidence_level> [site1] [site2] ..."
    echo "Levels: found, likely, unknown"
    echo "Example: confidence-filter.sh octocat likely github twitter"
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --min-confidence "$2" --print-found

