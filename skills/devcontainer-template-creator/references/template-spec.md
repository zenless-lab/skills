# Dev Container Templates Reference

A Template is a folder containing source files packaged together that encode configuration for a complete development environment.

## Folder structure

```
+-- template
|   +-- devcontainer-template.json
|   +-- .devcontainer
|       +-- devcontainer.json
|       +-- (other files)
|   +-- (other files)
```

## devcontainer-template.json properties

| Property | Type | Description |
| :--- | :--- | :--- |
| `id` | string | ID of the Template (must match directory name). |
| `version` | string | Semantic version (e.g., "1.0.0"). |
| `name` | string | Name of the Template. |
| `description` | string | Description of the Template. |
| `documentationURL` | string | Url to the documentation. |
| `licenseURL` | string | Url to the license. |
| `options` | object | Map of configurable options for the Template. |
| `platforms` | array | Languages and platforms supported. |
| `publisher` | string | Publisher/maintainer name. |
| `keywords` | array | Search keywords. |
| `optionalPaths` | array | Array of optional files or directories. Directories end with `/*`. |

### The `options` property

The `options` property allows tools to prompt the user to choose configurations. Selected values replace `${templateOption:optionId}` inside files in the template's sub-directory.

```json
{
  "options": {
    "imageVariant": {
      "type": "string",
      "description": "Specify version of java.",
      "proposals": ["17-bullseye", "11-bullseye"],
      "default": "17-bullseye"
    },
    "installMaven": {
      "type": "boolean",
      "description": "Install Maven.",
      "default": "false"
    }
  }
}
```

### The `optionalPaths` property

Allows tooling to prompt users whether to include specific files/folders.

```json
{
    "optionalPaths": [
         "GETTING-STARTED.md",
         ".github/*"
     ]
}
```

### Option Resolution
If an option `imageVariant` is set to `17-bullseye`, any occurrence of `${templateOption:imageVariant}` in `.devcontainer/devcontainer.json` will be replaced with `17-bullseye`.
