#!/bin/bash
# python -m anonymoustrace.main - Browse Results
# Usage: scripts/browse-results.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: browse-results.sh <username> [site1] [site2] ..."
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --browse --print-found

