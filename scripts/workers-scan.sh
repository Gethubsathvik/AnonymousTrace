#!/bin/bash
# python -m anonymoustrace.main - Custom Workers Scan
# Usage: scripts/workers-scan.sh <username> <worker_count> [sites...]

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: workers-scan.sh <username> <worker_count> [site1] [site2] ..."
    echo "Example: workers-scan.sh octocat 50 github twitter"
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$1" --workers "$2" --timeout 15 "${@:3}"

