#!/bin/bash
# python -m anonymoustrace.main - List All Sites
# Usage: scripts/list-sites.sh

cd "$(dirname "$0")/.."
python -m anonymoustrace.main --list-sites

