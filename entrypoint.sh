#!/bin/bash
set -e

echo "Cloning repo with submodules..."
git clone --recurse-submodules https://github.com/YOUR_USER/YOUR_REPO.git /repo

cd /repo

echo "Running manage action..."
bash .github/actions/manage/action.yml || true

echo "Running observability action..."
echo "Submodule update complete" | bash .github/actions/observability/action.yml || true

echo "Running commit-stream action..."
python3 .github/actions/commit-stream/stream_commits.py

echo "Done."
