# Supporting Tools and Services

This page outlines specific configurations available for popular Dev Container supporting tools.

## Editors

### Visual Studio Code
Visual Studio Code specific properties go under `vscode` inside `customizations`.

```json
"customizations": {
  "vscode": {
    "settings": {},
    "extensions": []
  }
}
```
*   `extensions`: An array of extension IDs that should be installed inside the container (e.g. `["ms-python.python"]`).
*   `settings`: Adds default `settings.json` values into a container specific settings file.

*(Note: GitHub Codespaces also supports the VS Code properties).*

## Cloud Services

### GitHub Codespaces
Codespaces specific properties are placed within a `codespaces` namespace inside the `customizations` property.

#### Repository Permissions
If your codespaces project needs additional permissions for other repositories:
```json
"customizations": {
  "codespaces": {
    "repositories": {
      "my_org/my_repo": {
        "permissions": {
          "issues": "write"
        }
      }
    }
  }
}
```

#### Open Files
You can customize which files are initially opened when the codespace is created:
```json
"customizations": {
  "codespaces": {
    "openFiles": [
      "README.md",
      "src/index.js"
    ]
  }
}
```

#### Disable Automatic Configuration
Codespaces automatically performs some default setup when no `postCreateCommand` is specified. To disable:
```json
"customizations": {
  "codespaces": {
    "disableAutomaticConfiguration": true
  }
}
```

*Note: Codespaces reads these properties directly from `devcontainer.json`, not from image metadata.*

### CodeSandbox, DevPod, and Ona (Gitpod)
Other tools like CodeSandbox, DevPod, and Ona also fully support the `devcontainer.json` specification to provision dedicated, reproducible environments natively in their respective platforms.
