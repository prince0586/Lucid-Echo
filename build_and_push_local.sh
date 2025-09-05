#!/usr/bin/env bash
set -euo pipefail
echo
echo "=== Build and Push Docker image to GHCR locally ==="
echo
echo "Requirements:"
echo "  - docker installed and running"
echo "  - gh CLI authenticated (gh auth login) or docker logged into ghcr.io"
echo
if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker CLI not found."
  exit 1
fi
if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI not found."
  exit 1
fi

OWNER=$(gh api user --jq .login)
REPO_NAME=$(basename -s .git $(git config --get remote.origin.url || 'lucid-echo'))
IMAGE=ghcr.io/${OWNER}/lucid-echo:local

echo "Detected owner: ${OWNER}"
echo "Image will be tagged as: ${IMAGE}"

echo "Building Docker image..."
docker build -t ${IMAGE} .

echo "Pushing to GHCR..."
# Ensure gh auth is available; login docker to ghcr if needed
echo "Logging into ghcr via gh CLI..."
echo "${OWNER}"

# Use gh to authenticate Docker to ghcr
echo "Authenticating docker to ghcr..."
echo | gh auth login --with-token >/dev/null 2>&1 || true
# Attempt docker login via gh auth token
TOKEN=$(gh auth token)
echo $TOKEN | docker login ghcr.io -u ${OWNER} --password-stdin

docker push ${IMAGE}

echo "Image pushed: ${IMAGE}"
echo "You may now find it in https://ghcr.io/${OWNER}/lucid-echo"
