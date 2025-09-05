#!/usr/bin/env bash
set -euo pipefail
echo
echo "=== Create a Personal Access Token (PAT) for GHCR and add it as a repo secret ==="
echo
echo "This script prints instructions and will try to add the token to the current repository using the GitHub CLI (gh)."
echo
echo "Requirements:"
echo "  - gh (GitHub CLI) installed and authenticated (https://cli.github.com/)"
echo "  - You have 'repo' and 'read:packages' & 'write:packages' permission for your account or org"
echo
echo "STEP 1: Generate a token via the web UI (recommended):"
echo "  1. Go to https://github.com/settings/tokens -> Developer settings -> Personal access tokens -> Generate new token"
echo "  2. Choose an expiration (or no expiration)"
echo "  3. Check scopes: 'read:packages', 'write:packages', and 'repo' (if needed)"
echo "  4. Generate token and COPY IT NOW (you will not be able to view it again)"
echo
read -p "When you have the token copied to your clipboard, press ENTER to continue..."

echo
if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI not found. Please install and authenticate first: https://cli.github.com/"
  exit 1
fi

read -p "Paste the PAT now (it will be hidden): " -s PAT
echo
echo "Adding secret GHCR_PAT to the current repository using gh secret set..."

# Try to detect repo from git remote
REPO=$(git config --get remote.origin.url || true)
if [[ -z "$REPO" ]]; then
  echo "Cannot detect git remote. Make sure you're in the repository root and a remote 'origin' exists."
  exit 1
fi

# Use gh to set secret
echo "$PAT" | gh secret set GHCR_PAT --body -

echo "Secret GHCR_PAT added to the repository. The workflow will now prefer GHCR_PAT over GITHUB_TOKEN."
echo "NOTE: If you want the PAT to be accessible to workflows from forks, configure repo/org policies accordingly."
