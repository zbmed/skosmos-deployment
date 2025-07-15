#!/bin/bash

# Function to print usage
usage() {
  echo "Usage: $0 --repo_name owner/repo"
  exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --repo_name) REPO_NAME="$2"; shift ;;
    *) usage ;;
  esac
  shift
done

# Check if REPO_NAME is set
if [[ -z "$REPO_NAME" ]]; then
  usage
fi

# Fetch the latest release info from GitHub API
RELEASE_INFO=$(curl -s "https://api.github.com/repos/${REPO_NAME}/releases/latest")

# Extract and clean the release name
RELEASE_NAME=$(echo "$RELEASE_INFO" | grep '"name":' | head -n 1 | sed -E 's/.*"name": "Release ([^"]+)".*/\1/')

# Fallback if no "Release " prefix
if [[ -z "$RELEASE_NAME" ]]; then
  RELEASE_NAME=$(echo "$RELEASE_INFO" | grep '"name":' | head -n 1 | sed -E 's/.*"name": "([^"]+)".*/\1/')
fi

# Print the release name
echo "$RELEASE_NAME"
