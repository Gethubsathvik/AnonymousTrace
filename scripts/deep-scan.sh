#!/bin/bash
# python -m anonymoustrace.main - Deep Scan Mode
# Usage: scripts/deep-scan.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: deep-scan.sh <username> [site1] [site2] ..."
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --deep

