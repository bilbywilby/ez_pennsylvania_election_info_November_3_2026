#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
REQUIRED_PATHS=("public" "public/index.html" "public/css/styles.css" "docs" ".github/workflows")
missing_path=0

for path in "${REQUIRED_PATHS[@]}"; do
    if [[ ! -e "$REPO_ROOT/$path" ]]; then
        echo "Error: required path '$path' was not found." >&2
        missing_path=1
    else
        echo "Verified: $path"
    fi
done

if [[ "$missing_path" -ne 0 ]]; then
    echo "Environment check failed." >&2
    exit 1
fi

if [[ -z "${WIKI_SYNC_TOKEN:-}" ]]; then
    echo "Warning: WIKI_SYNC_TOKEN is unset; wiki deployment will require it."
else
    echo "WIKI_SYNC_TOKEN is configured."
fi

echo "Repository layout is ready for deployment."
