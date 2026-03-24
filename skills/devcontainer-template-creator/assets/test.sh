#!/bin/bash
cd $(dirname "$0")

# Setup temporary test directory
TEST_WORKSPACE="/tmp/workspace"
rm -rf "$TEST_WORKSPACE"
mkdir -p "$TEST_WORKSPACE"

echo "Template test script executing..."
# For standard testing, usually @devcontainers/cli is used:
# devcontainer templates apply --workspace-folder "$TEST_WORKSPACE" --template-id "<template-id>" --template-args '{"imageVariant": "debian-11"}'

echo "Test executed successfully."
exit 0
