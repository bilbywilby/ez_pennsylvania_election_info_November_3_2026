#!/usr/bin/env bash
set -euo pipefail

readonly REPO="bilbywilby/ez_pennsylvania_election_info_November_3_2026"

usage() {
    echo "Usage: $0 <pages|wiki|both> <environment>" >&2
    exit 2
}

[[ $# -eq 2 ]] || usage
target=$1
environment=$2

case "$target" in
    pages|wiki|both) ;;
    *) echo "Error: target must be pages, wiki, or both." >&2; usage ;;
esac

if [[ -z "$environment" ]]; then
    echo "Error: environment must not be empty." >&2
    usage
fi

if [[ -z "${GH_TOKEN:-}" && -z "${GITHUB_TOKEN:-}" ]]; then
    echo "Error: set GH_TOKEN or GITHUB_TOKEN before triggering a dispatch." >&2
    exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
    echo "Error: GitHub CLI (gh) is required." >&2
    exit 1
fi

export GH_TOKEN="${GH_TOKEN:-$GITHUB_TOKEN}"
gh api \
    --method POST \
    -H "Accept: application/vnd.github+json" \
    "repos/$REPO/dispatches" \
    -f event_type=deploy \
    -f "client_payload[target]=$target" \
    -f "client_payload[env]=$environment"
