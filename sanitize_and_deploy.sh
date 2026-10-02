#!/bin/bash
# Carter's Repo Sanitizer & Deployment Tool
set -euo pipefail

# 1. Auth Restoration
if [ -z "${GH_TOKEN:-}" ]; then
    echo "⚠️  GH_TOKEN not found. Please enter your GitHub PAT:"
    read -s GH_TOKEN
    export GH_TOKEN
fi

# 2. Root Directory Cleanup
echo "--- Cleaning Root Directory ---"
mkdir -p ./archive
# Move all PDFs and numerically-named txt files to archive
find . -maxdepth 1 -name "*.pdf" -exec mv {} ./archive/ \;
find . -maxdepth 1 -name "[0-9]*.txt" -exec mv {} ./archive/ \;

# 3. Update .gitignore to prevent future clutter
echo "*.pdf" >> .gitignore
echo "[0-9]*.txt" >> .gitignore
echo "archive/" >> .gitignore

# 4. Stage and Push
git add .
git commit -m "OPSEC: Sanitize root directory and update .gitignore"
if git push origin main; then
    echo "✅ Cleanup complete and deployment triggered."
else
    echo "❌ Push failed. Check remote permissions."
    exit 1
fi
