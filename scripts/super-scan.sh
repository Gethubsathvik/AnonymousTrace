#!/bin/bash
# python -m anonymoustrace.main - Super Scan Mode
# Usage: scripts/super-scan.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: super-scan.sh <username> [site1] [site2] ..."
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --super

