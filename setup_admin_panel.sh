#!/bin/bash
# Carter's Admin Panel Provisioning Script
set -euo pipefail

# Environment Setup
mkdir -p ./scripts ./admin_panel/logs
touch ./admin_panel/logs/deploy.log

# Create the trigger script for GitHub Repository Dispatch
cat << 'INNER' > ./scripts/trigger_dispatch.sh
#!/bin/bash
TARGET=$1
ENV=$2
TOKEN="YOUR_GITHUB_PAT" # Ensure this is stored in an ENV var in production
REPO="bilbywilby/ez_pennsylvania_election_info_November_3_2026"

curl -X POST -H "Accept: application/vnd.github.v3+json" \
     -H "Authorization: token $TOKEN" \
     -d "{\"event_type\": \"deploy\", \"client_payload\": {\"target\": \"$TARGET\", \"env\": \"$ENV\"}}" \
     "https://api.github.com/repos/$REPO/dispatches"
INNER

chmod +x ./scripts/trigger_dispatch.sh

echo "✓ Infrastructure provisioned. Admin panel directories and dispatch scripts active."
