#!/bin/bash
# python -m anonymoustrace.main - Plain Text Output
# Usage: scripts/plain.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: plain.sh <username> [site1] [site2] ..."
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --plain

