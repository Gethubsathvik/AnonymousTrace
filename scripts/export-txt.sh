#!/bin/bash
# python -m anonymoustrace.main - TXT Export
# Usage: scripts/export-txt.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: export-txt.sh <username> [site1] [site2] ..."
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --txt --output results.txt
echo "TXT exported to results.txt"

