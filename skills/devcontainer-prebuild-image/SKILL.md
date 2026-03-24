---
name: devcontainer-prebuild-image
description: Use this skill when asked to create, configure, build, or publish pre-built Dev Container images, or when setting up a repository for maintaining base images for Dev Containers.
---

# Dev Container Prebuilt Images Guide

This skill guides the creation, configuration, and publication of pre-built Development Container images. Pre-building images speeds up container startup times, ensures consistency across teams, and simplifies `devcontainer.json` configurations.

## 1. Using a Prebuilt Image

Instead of building from a Dockerfile locally, you can use a prebuilt image hosted in a container registry (e.g., GHCR, Docker Hub, MCR).

Modify `devcontainer.json` to use the `image` property:

```json
{
  "name": "My Prebuilt Dev Environment",
  "image": "ghcr.io/your-org/your-image:latest"
  // Note: Remove the "build" block if switching to "image"
}
```

## 2. Creating a Prebuilt Image

To create a prebuilt image, you typically define a `devcontainer.json` (and optionally a `Dockerfile`) in a workspace, and then use the Dev Container CLI to build it. The CLI automatically embeds metadata (like VS Code extensions and port forwarding) into the image via labels.

### Building Locally

1. **Install the CLI:**
   ```bash
   npm install -g @devcontainers/cli
   ```
2. **Build and Push:**
   Run this command from the directory containing your `.devcontainer` folder (or where `devcontainer.json` is located):
   ```bash
   devcontainer build --workspace-folder . --push true --image-name <your-registry>/<image-name>:<tag>
   ```

## 3. Recommended Repository Structure (Multi-Image)

If you are maintaining a repository with multiple prebuilt images (similar to the official `devcontainers/images` repo), follow this structure:

```text
src/
  ├── <image-name>/
  │   ├── .devcontainer/
  │   │   ├── devcontainer.json   # Base configuration and features
  │   │   └── Dockerfile          # (Optional) Base OS and custom setup
  │   ├── README.md               # Documentation, tags, and registry info
  │   └── history/                # (Optional) Version history of packages
  └── <another-image>/
      └── ...
```

### Dockerfile Best Practices
- **Layer Optimization:** Combine commands in `RUN` statements using `&&` and include cleanup steps in the same layer to reduce image size.
  ```dockerfile
  RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
      && apt-get -y install --no-install-recommends some-package \
      && apt-get clean -y && rm -rf /var/lib/apt/lists/*
  ```
- **Base Images:** Consider using universal or base images from `mcr.microsoft.com/devcontainers/base:*`.
- **Features:** Leverage Dev Container Features (e.g., `ghcr.io/devcontainers/features/common-utils:2`) in the `devcontainer.json` before building the image, rather than manually scripting tool installations in the Dockerfile.

## 4. Automation via CI/CD (GitHub Actions)

Use the official `devcontainers/ci` GitHub Action to automate building and pushing your image when changes are made.

Example `.github/workflows/build-image.yml`:

```yaml
name: Build and Push Dev Container Image

on:
  push:
    branches: [ main ]
    paths:
      - 'src/<image-name>/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push dev container image
        uses: devcontainers/ci@v0.3
        with:
          imageName: ghcr.io/${{ github.repository_owner }}/<image-name>
          imageTag: latest
          subFolder: src/<image-name>
          push: always
```

## 5. References and Ecosystem
- **Official Base Images:** https://github.com/devcontainers/images
