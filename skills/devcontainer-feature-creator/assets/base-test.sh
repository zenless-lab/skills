#!/bin/bash
set -e

# Optional: Import test library
source dev-container-features-test-lib

# Use the `check` command to assert success.
# Format: check <LABEL> <cmd> [args...]
check "Feature is available" my-feature --version
check "Feature output is correct" bash -c "my-feature run | grep 'Expected Output'"

# Report results
reportResults
