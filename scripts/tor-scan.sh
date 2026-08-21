#!/bin/bash
# python -m anonymoustrace.main - Tor Scan
# Usage: scripts/tor-scan.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: tor-scan.sh <username> [site1] [site2] ..."
    echo "Note: Tor service must be running on 127.0.0.1:9050"
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --tor --stealth --print-all

