#!/bin/bash
# python -m anonymoustrace.main - Batch Scan from File
# Usage: scripts/batch-scan.sh <input_file> [sites...]

if [ -z "$1" ]; then
    echo "Usage: batch-scan.sh <input_file> [site1] [site2] ..."
    echo "Example: batch-scan.sh users.txt github twitter"
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main --input-file "$1" --timeout 15 --print-found

