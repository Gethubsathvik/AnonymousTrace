#!/bin/bash
# python -m anonymoustrace.main - Skip Flaky Sites Scan
# Usage: scripts/skip-flaky-scan.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: skip-flaky-scan.sh <username> [site1] [site2] ..."
    echo "Skips known problematic sites with DNS/timeout issues"
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --skip-flaky

