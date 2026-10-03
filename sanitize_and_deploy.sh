#!/bin/bash
# Carter's Repo Sanitizer & Deployment Tool - Optimized
set -euo pipefail

# Environment Check
if [[ -z "${GH_TOKEN:-}" ]]; then
    echo "Error: GH_TOKEN environment variable is not set."
    echo "Execute: export GH_TOKEN='your_token_here'"
    exit 1
fi

echo "--- Cleaning Root Directory ---"
mkdir -p ./archive
find . -maxdepth 1 -name "*.pdf" -exec mv {} ./archive/ \;
find . -maxdepth 1 -name "[0-9]*.txt" -exec mv {} ./archive/ \;

echo "--- Updating .gitignore ---"
{
    echo "*.pdf"
    echo "[0-9]*.txt"
    echo "archive/"
} >> .gitignore
# Remove duplicates from .gitignore
sort -u .gitignore -o .gitignore

git add .
git commit -m "OPSEC: Sanitize root directory and update .gitignore"

if git push origin main; then
    echo "✅ Cleanup complete and deployment triggered."
else
    echo "❌ Push failed. Verify GH_TOKEN permissions and remote URL."
    exit 1
fi
