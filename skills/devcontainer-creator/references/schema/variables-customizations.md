# Variables and Customizations

## Supported Variables
Variables can be referenced in certain string values within `devcontainer.json` using the `${variableName}` format.

| Variable | Description |
|----------|-------------|
| `${localEnv:VARIABLE_NAME}` | Value of an environment variable on the **host machine**. E.g., `${localEnv:HOME}`. Support default values: `${localEnv:VAR:default}`. |
| `${containerEnv:VARIABLE_NAME}` | Value of an existing environment variable **inside** the container. Supported inside `remoteEnv`. E.g., `${containerEnv:PATH}`. |
| `${localWorkspaceFolder}` | Path of the local folder opened by the tool. |
| `${containerWorkspaceFolder}` | Path where workspace files are found in the container. |
| `${localWorkspaceFolderBasename}` | Name of the local folder. |
| `${containerWorkspaceFolderBasename}`| Name of the workspace folder in the container. |
| `${devcontainerId}` | A unique, stable identifier for the specific dev container instance. Ideal for isolating mounts (e.g., `my-volume-${devcontainerId}`). |

## Tool-Specific Customizations
The `customizations` property allows adding tool-specific settings.

### VS Code (`customizations.vscode`)
| Property | Type | Description |
|----------|------|-------------|
| `extensions` | array | Array of extension IDs to install inside the container (e.g., `["ms-python.python", "golang.go"]`). |
| `settings` | object | Default `settings.json` values injected into the container (e.g., `{"python.defaultInterpreterPath": "/usr/local/bin/python"}`). |

### Codespaces (`customizations.codespaces`)
| Property | Type | Description |
|----------|------|-------------|
| `openFiles` | array | Array of files to automatically open when the codespace is created. |
| `repositories` | object | Request additional permissions for other repositories (e.g., `{"org/repo": {"permissions": {"issues": "write"}}}`). |
