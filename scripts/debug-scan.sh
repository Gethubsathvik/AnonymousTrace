#!/bin/bash
# python -m anonymoustrace.main - Debug/Dump Response
# Usage: scripts/debug-scan.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: debug-scan.sh <username> [site1] [site2] ..."
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --dump-response --verbose --print-all

