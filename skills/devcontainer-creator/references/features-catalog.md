# Features Catalog

This is a list of commonly used official Dev Container Features. Features are self-contained scripts that install additional tools into an existing container.

They are hosted on the GitHub Container Registry (`ghcr.io`).

## How to reference a feature in devcontainer.json

```json
"features": {
    "ghcr.io/devcontainers/features/python:1": {
        "version": "3.10",
        "installTools": true
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
}
```

## Available Features

### Languages & Runtimes
*   `ghcr.io/devcontainers/features/python:1`
*   `ghcr.io/devcontainers/features/node:1`
*   `ghcr.io/devcontainers/features/java:1`
*   `ghcr.io/devcontainers/features/go:1`
*   `ghcr.io/devcontainers/features/rust:1`
*   `ghcr.io/devcontainers/features/ruby:1`
*   `ghcr.io/devcontainers/features/php:1`
*   `ghcr.io/devcontainers/features/dotnet:2`
*   `ghcr.io/devcontainers/features/anaconda:1`
*   `ghcr.io/devcontainers/features/conda:1`
*   `ghcr.io/devcontainers/features/nix:1`

### Docker & Kubernetes
*   **Docker-in-Docker**: `ghcr.io/devcontainers/features/docker-in-docker:2` (Requires running the container with `privileged: true`).
*   **Docker-from-Docker**: `ghcr.io/devcontainers/features/docker-outside-of-docker:1`
*   **Kubernetes / Helm / Minikube**: `ghcr.io/devcontainers/features/kubectl-helm-minikube:1`

### Tools & CLI
*   **Git**: `ghcr.io/devcontainers/features/git:1`
*   **Git LFS**: `ghcr.io/devcontainers/features/git-lfs:1`
*   **GitHub CLI**: `ghcr.io/devcontainers/features/github-cli:1`
*   **GitHub Copilot CLI**: `ghcr.io/devcontainers/features/copilot-cli:1`
*   **AWS CLI**: `ghcr.io/devcontainers/features/aws-cli:1`
*   **Azure CLI**: `ghcr.io/devcontainers/features/azure-cli:1`
*   **Terraform**: `ghcr.io/devcontainers/features/terraform:1`
*   **PowerShell**: `ghcr.io/devcontainers/features/powershell:2`

### System & Infrastructure
*   **Common Utils**: `ghcr.io/devcontainers/features/common-utils:2`
*   **Desktop Lite**: `ghcr.io/devcontainers/features/desktop-lite:1`
*   **SSHD**: `ghcr.io/devcontainers/features/sshd:1`
*   **Nvidia CUDA**: `ghcr.io/devcontainers/features/nvidia-cuda:2`
*   **Hugo**: `ghcr.io/devcontainers/features/hugo:1`
*   **Oryx**: `ghcr.io/devcontainers/features/oryx:2`
