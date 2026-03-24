---
name: devcontainer-template-creator
description: Create, configure, and update Dev Container Templates. Trigger this skill when asked to scaffold a new template, configure devcontainer-template.json, create template tests, or publish/distribute a dev container template.
---

# Dev Container Template Creator

This skill serves as a comprehensive guide to assist you in scaffolding, developing, configuring, testing, and distributing Dev Container Templates according to the official Dev Containers specifications.

## Core Principles

- **Spec Adherence:** Templates must contain a `devcontainer-template.json` and a `.devcontainer/devcontainer.json` file. The metadata must strictly follow the schema.
- **Distribution via OCI:** Templates are packaged as tarballs and distributed through OCI registries.
- **Testing:** Include a test script in `test/<template-name>/test.sh` to automatically build and verify the template.

## Workflow

Follow these steps to construct or update a Dev Container Template:

### 1. Analyze & Scaffold
- Verify the workspace structure. Templates reside in `src/<template-name>/` and their tests in `test/<template-name>/`.
- Create these directories if they don't exist.

### 2. Configure Metadata
- Create or update `src/<template-name>/devcontainer-template.json`.
- Define the `id`, `version`, `name`, `description`, `publisher`, `options`, and `optionalPaths`.
- Use `assets/devcontainer-template.json` as a starting point.
- See `references/template-spec.md` for metadata schema and option resolution details.

### 3. Develop Template
- Scaffold `.devcontainer/devcontainer.json` inside `src/<template-name>/.devcontainer/`.
- This file should define the starting point for containerizing the project. It can utilize options via `${templateOption:optionName}` syntax.
- Optionally add boilerplate project code, scripts, or other configurations. If certain files are optional, configure `optionalPaths` in `devcontainer-template.json`.
- Use `assets/devcontainer.json` as a boilerplate for the devcontainer config.

### 4. Testing
- Scaffold a test script: `test/<template-name>/test.sh`.
- The test should verify that the dev container builds successfully and functions as intended.
- Use `assets/test.sh` as a boilerplate for test scripts.

### 5. Distribution
- If the user wants to publish the template, ensure they have a `devcontainer-collection.json` and are using standard tools like `@devcontainers/cli` or the GitHub Action.
- Refer to `references/distribution.md` for details on the packaging and OCI registry distribution mechanism.

## Reference Materials

- [template-spec.md](references/template-spec.md): Schema for `devcontainer-template.json`, options, and optional paths.
- [distribution.md](references/distribution.md): Guidelines on how templates are packaged into tarballs and distributed via OCI registries.
