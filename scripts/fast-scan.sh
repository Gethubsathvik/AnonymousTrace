#!/bin/bash
# python -m anonymoustrace.main - Fast Scan Mode
# Usage: scripts/fast-scan.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: fast-scan.sh <username> [site1] [site2] ..."
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --fast

