#!/bin/sh
set -e

# The install script runs as root.
# Options passed from devcontainer-feature.json are upper-cased.
# e.g., the 'version' option becomes $VERSION.
VERSION="${VERSION:-latest}"

# Clean up
rm -rf /var/lib/apt/lists/*

if [ "$(id -u)" -ne 0 ]; then
    echo 'Script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.'
    exit 1
fi

# Determine the appropriate non-root user
if [ "${_REMOTE_USER}" = "root" ] || [ -z "${_REMOTE_USER}" ]; then
    USERNAME="root"
else
    USERNAME="${_REMOTE_USER}"
fi

# Function to run apt-get if needed
apt_get_update() {
    if [ "$(find /var/lib/apt/lists/* | wc -l)" = "0" ]; then
        echo "Running apt-get update..."
        apt-get update -y
    fi
}

# Example OS Check (Debian/Ubuntu)
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [ "${ID}" != "debian" ] && [ "${ID}" != "ubuntu" ]; then
        echo "Unsupported OS: ${ID}"
        exit 1
    fi
else
    echo "Unsupported OS"
    exit 1
fi

echo "Installing Feature..."

# Install logic goes here...
# e.g., apt_get_update && apt-get install -y my-package

# Clean up caches to reduce layer size
rm -rf /var/lib/apt/lists/*

echo "Done!"
