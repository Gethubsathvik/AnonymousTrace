#!/bin/bash
# python -m anonymoustrace.main - Custom Registry
# Usage: scripts/custom-registry.sh <username> <registry.json> [sites...]

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: custom-registry.sh <username> <registry.json> [site1] [site2] ..."
    echo "Example: custom-registry.sh octocat my_sites.json github twitter"
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$1" --data-file "$2" --timeout 15 --print-all

