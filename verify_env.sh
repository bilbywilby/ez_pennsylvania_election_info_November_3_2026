#!/bin/bash
# Carter's Pre-Flight Environment Check
set -euo pipefail

REQUIRED_DIRS=("public" "docs")
MISSING_DIR=0

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ Error: Directory $dir not found."
        MISSING_DIR=1
    else
        echo "✅ Directory $dir verified."
    fi
done

if [ "$MISSING_DIR" -eq 1 ]; then
    echo "Environment check failed. Please create missing directories."
    exit 1
fi

# Check if WIKI_SYNC_TOKEN is set in current shell for local testing
if [ -z "${WIKI_SYNC_TOKEN:-}" ]; then
    echo "⚠️  Warning: WIKI_SYNC_TOKEN not found in local environment."
    echo "Ensure this secret is added to GitHub Repository Secrets."
else
    echo "✅ WIKI_SYNC_TOKEN is present."
fi

echo "Environment is ready for deployment."
