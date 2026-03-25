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
*   `ghcr.io/devcontainers/features/python:1`: Installs the provided version of Python, as well as PIPX, and other common Python utilities. JupyterLab is conditionally installed. [Documentation](https://github.com/devcontainers/features/tree/main/src/python)
*   `ghcr.io/devcontainers/features/node:1`: Installs Node.js, nvm, yarn, pnpm, and needed dependencies. [Documentation](https://github.com/devcontainers/features/tree/main/src/node)
*   `ghcr.io/devcontainers/features/java:1`: Installs Java, SDKMAN! (if not installed), and needed dependencies. [Documentation](https://github.com/devcontainers/features/tree/main/src/java)
*   `ghcr.io/devcontainers/features/go:1`: Installs Go and common Go utilities. Auto-detects latest version and installs needed dependencies. [Documentation](https://github.com/devcontainers/features/tree/main/src/go)
*   `ghcr.io/devcontainers/features/rust:1`: Installs Rust, common Rust utilities, and their required dependencies. [Documentation](https://github.com/devcontainers/features/tree/main/src/rust)
*   `ghcr.io/devcontainers/features/ruby:1`: Installs Ruby, rvm, rbenv, common Ruby utilities, and needed dependencies. [Documentation](https://github.com/devcontainers/features/tree/main/src/ruby)
*   `ghcr.io/devcontainers/features/php:1`: Installs PHP and optionally Composer. Includes PHP language extensions for PHP development. [Documentation](https://github.com/devcontainers/features/tree/main/src/php)
*   `ghcr.io/devcontainers/features/dotnet:2`: Installs the latest .NET SDK, which includes the .NET CLI and the shared runtime. [Documentation](https://github.com/devcontainers/features/tree/main/src/dotnet)
*   `ghcr.io/devcontainers/features/anaconda:1`: Includes Anaconda and the conda package manager for data science and Python development. [Documentation](https://github.com/devcontainers/features/tree/main/src/anaconda)
*   `ghcr.io/devcontainers/features/conda:1`: A cross-platform, language-agnostic binary package manager. [Documentation](https://github.com/devcontainers/features/tree/main/src/conda)
*   `ghcr.io/devcontainers/features/nix:1`: Installs the Nix package manager and optionally a set of packages. [Documentation](https://github.com/devcontainers/features/tree/main/src/nix)

### Docker & Kubernetes
*   `ghcr.io/devcontainers/features/docker-in-docker:2`: Create child containers *inside* a container, independent from the host's docker instance. (Requires running the container with `privileged: true`). [Documentation](https://github.com/devcontainers/features/tree/main/src/docker-in-docker)
*   `ghcr.io/devcontainers/features/docker-outside-of-docker:1`: Re-use the host docker socket, adding the Docker CLI to a container. [Documentation](https://github.com/devcontainers/features/tree/main/src/docker-outside-of-docker)
*   `ghcr.io/devcontainers/features/kubectl-helm-minikube:1`: Installs latest version of kubectl, Helm, and optionally minikube. [Documentation](https://github.com/devcontainers/features/tree/main/src/kubectl-helm-minikube)

### Tools & CLI
*   `ghcr.io/devcontainers/features/git:1`: Install an up-to-date version of Git, built from source as needed. [Documentation](https://github.com/devcontainers/features/tree/main/src/git)
*   `ghcr.io/devcontainers/features/git-lfs:1`: Installs Git Large File Support (Git LFS) along with needed dependencies. [Documentation](https://github.com/devcontainers/features/tree/main/src/git-lfs)
*   `ghcr.io/devcontainers/features/github-cli:1`: Installs the GitHub CLI. [Documentation](https://github.com/devcontainers/features/tree/main/src/github-cli)
*   `ghcr.io/devcontainers/features/copilot-cli:1`: Installs the GitHub Copilot CLI. [Documentation](https://github.com/devcontainers/features/tree/main/src/copilot-cli)
*   `ghcr.io/devcontainers/features/aws-cli:1`: Installs the AWS CLI along with needed dependencies. [Documentation](https://github.com/devcontainers/features/tree/main/src/aws-cli)
*   `ghcr.io/devcontainers/features/azure-cli:1`: Installs the Azure CLI along with needed dependencies. [Documentation](https://github.com/devcontainers/features/tree/main/src/azure-cli)
*   `ghcr.io/devcontainers/features/terraform:1`: Installs the Terraform CLI and optionally TFLint and Terragrunt. [Documentation](https://github.com/devcontainers/features/tree/main/src/terraform)
*   `ghcr.io/devcontainers/features/powershell:2`: Installs PowerShell along with needed dependencies. [Documentation](https://github.com/devcontainers/features/tree/main/src/powershell)

### System & Infrastructure
*   `ghcr.io/devcontainers/features/common-utils:2`: Installs a set of common command line utilities, Oh My Zsh!, and sets up a non-root user. [Documentation](https://github.com/devcontainers/features/tree/main/src/common-utils)
*   `ghcr.io/devcontainers/features/desktop-lite:1`: Adds a lightweight Fluxbox-based desktop to the container that can be accessed using a VNC viewer or the web. [Documentation](https://github.com/devcontainers/features/tree/main/src/desktop-lite)
*   `ghcr.io/devcontainers/features/sshd:1`: Adds a SSH server into a container so that you can use an external terminal, sftp, or SSHFS to interact with it. [Documentation](https://github.com/devcontainers/features/tree/main/src/sshd)
*   `ghcr.io/devcontainers/features/nvidia-cuda:2`: Installs shared libraries for NVIDIA CUDA. [Documentation](https://github.com/devcontainers/features/tree/main/src/nvidia-cuda)
*   `ghcr.io/devcontainers/features/hugo:1`: Installs Hugo, a popular open-source static site generator written in Go. [Documentation](https://github.com/devcontainers/features/tree/main/src/hugo)
*   `ghcr.io/devcontainers/features/oryx:2`: Installs the oryx CLI. [Documentation](https://github.com/devcontainers/features/tree/main/src/oryx)
