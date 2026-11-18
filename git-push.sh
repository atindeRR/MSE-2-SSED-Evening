#!/usr/bin/env bash
# Run this in Git Bash to push to GitHub
# Usage: bash git-push.sh
cd "$(dirname "$0")"
echo "Pushing to GitHub..."
git push origin main
echo "Done! Now go create the PR at:"
echo "https://github.com/Priya342-gif/MSE-2-SSED-Evening/compare"
