#!/bin/bash
# python -m anonymoustrace.main - Stealth Scan Mode
# Usage: scripts/stealth-scan.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: stealth-scan.sh <username> [site1] [site2] ..."
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --stealth --tor

