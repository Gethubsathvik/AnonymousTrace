#!/bin/bash
# Quick setup and run script for AnonymousTrace
# Usage: bash run.sh [username]

set -e

echo "=== AnonymousTrace ==="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q requests requests-futures certifi PySocks stem rich colorama pandas

# Run scan if username provided
if [ -n "$1" ]; then
    echo ""
    echo "Running scan for: $1"
    python3 -m anonymoustrace.main "$@"
else
    echo ""
    echo "Setup complete! Run a scan with:"
    echo "  python3 -m anonymoustrace.main <username>"
    echo ""
    echo "Or try:"
    echo "  python3 -m anonymoustrace.main --list-sites"
    echo "  python3 -m anonymoustrace.main --help"
fi