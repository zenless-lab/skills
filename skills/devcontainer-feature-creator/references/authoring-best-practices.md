# Authoring Best Practices

When building Dev Container Features, adhere to the following best practices recommended by the official Dev Container specification.

## 1. Ensure Idempotency
Features must be safely runnable multiple times. If another Feature depends on yours, or a user specifies it alongside a template that already includes it, the script may be executed multiple times. Ensure that redundant executions do not result in failures or duplicated configurations (e.g., use `grep` before appending to `.bashrc`).

## 2. Handle the Non-Root User
Installation scripts always run as `root` during the image build. However, the developer often connects as a non-root user (e.g., `vscode` or `node`).
- Use the `_REMOTE_USER` and `_REMOTE_USER_HOME` environment variables injected by the Dev Container CLI to set correct file ownership.
- Apply `chown` to directories or files that the developer will need to modify.

## 3. OS Compatibility and Portability
Features are meant to be portable across different base images.
- **Distro Check:** At the start of `install.sh`, verify the OS/distribution (e.g., using `/etc/os-release`) and provide a clean error message if the distro is unsupported.
- **Shell Compatibility:** Use `#!/bin/sh` instead of `#!/bin/bash` to maximize compatibility (especially for Alpine), or include a robust bootstrap mechanism to install `bash` if your script strictly requires it.

## 4. Minimize Image Layers
To ensure dev containers start quickly, keep the image size small.
- Clean up temporary files, tarballs, and package manager caches within the same execution block (e.g., `rm -rf /var/lib/apt/lists/*` at the end of the script).

## 5. Comprehensive Testing
Always utilize the `devcontainer features test` command.
- Test against multiple distributions (Ubuntu, Debian, Alpine).
- Test varying option combinations using `scenarios.json`.
- Implement `duplicate.sh` tests to formally verify idempotency.

## 6. Meaningful Metadata
A well-defined `devcontainer-feature.json` is crucial.
- Provide a clear `name` and `description`.
- Document every option thoroughly, providing sensible `default` values.
