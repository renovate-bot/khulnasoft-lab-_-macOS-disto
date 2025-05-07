#!/bin/bash

# Exit immediately if any command fails
set -e

echo "Initializing and updating all git submodules recursively..."

# Initialize submodules
git submodule init

# Update submodules recursively
git submodule update --recursive --remote

echo "All submodules have been updated recursively."
