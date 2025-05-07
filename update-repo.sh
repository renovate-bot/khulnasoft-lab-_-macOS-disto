#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Pulling latest changes from the main repository (with submodules)..."
git pull --recurse-submodules

echo "Updating submodules recursively and pulling from their remotes..."
git submodule update --recursive --remote

echo "Repository and submodules successfully updated."
