#!/bin/bash
# python -m anonymoustrace.main - Proxy Scan
# Usage: scripts/proxy-scan.sh <username> <proxy_url> [sites...]

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: proxy-scan.sh <username> <proxy_url> [site1] [site2] ..."
    echo "Example: proxy-scan.sh octocat socks5://127.0.0.1:1080 github twitter"
    exit 1
fi

cd "$(dirname "$0")/.."
python -m anonymoustrace.main "$1" --proxy "$2" --timeout 15 --print-all

