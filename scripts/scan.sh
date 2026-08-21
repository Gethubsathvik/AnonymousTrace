#!/bin/bash
# python -m anonymoustrace.main - Quick Scan Script
# Usage: scripts/scan.sh <username> [site1] [site2] ...

if [ -z "$1" ]; then
    echo "Usage: scan.sh <username> [site1] [site2] ..."
    echo "Example: scan.sh octocat github twitter"
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@"

