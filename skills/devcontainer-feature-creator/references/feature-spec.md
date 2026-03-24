# Feature Specification

A Dev Container Feature consists primarily of metadata and an installation script.

## Metadata (`devcontainer-feature.json`)

This JSON file describes the Feature.

| Property       | Description                                                                                               |
|----------------|-----------------------------------------------------------------------------------------------------------|
| `id`           | Required. A short, unique identifier (e.g., `python`).                                                    |
| `version`      | Required. Semantic version (e.g., `1.0.0`).                                                               |
| `name`         | Required. Human-readable name.                                                                            |
| `description`  | Required. A brief description of what the feature does.                                                   |
| `options`      | An object defining user-configurable settings. Values are passed as environment variables to `install.sh`.|
| `instantiates` | Used primarily for testing/tooling to specify a base image (e.g., `{"image": "ubuntu:22.04"}`).           |
| `dependsOn`    | An object of other Features to install before this one.                                                   |

### Options Schema
Options define configurable parameters:
```json
"options": {
    "version": {
        "type": "string",
        "enum": ["latest", "2.0", "1.0"],
        "default": "latest",
        "description": "Choose the version to install"
    }
}
```

## Implementation (`install.sh`)

The entry point for installing a Feature.

### Execution Context
- **User:** The script executes as the `root` user during the container build process.
- **Environment Variables:** Options declared in `devcontainer-feature.json` are exposed to the script as uppercase environment variables (e.g., `optionName` becomes `$OPTIONNAME`).
- **CLI Injected Variables:**
  - `_REMOTE_USER`: The username of the non-root user (e.g., `vscode` or `node`).
  - `_REMOTE_USER_HOME`: The home directory of the `_REMOTE_USER`.
  - `_CONTAINER_USER`: The user the container will run as (might be different from remote user).

### Constraints
- The script must be executable (`chmod +x install.sh`).
- It must handle cases where required tools (like `curl`, `wget`, `bash`) are not present on minimal base images.
