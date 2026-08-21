#!/bin/bash
# python -m anonymoustrace.main - CSV Export
# Usage: scripts/export-csv.sh <username> [sites...]

if [ -z "$1" ]; then
    echo "Usage: export-csv.sh <username> [site1] [site2] ..."
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$@" --csv --output results.csv
echo "CSV exported to results.csv"

