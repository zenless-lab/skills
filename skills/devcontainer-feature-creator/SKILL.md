---
name: devcontainer-feature-creator
description: Create, edit, and update Dev Container Features. Trigger this skill when asked to create a reusable dev container feature, scaffold a new feature directory with install.sh and devcontainer-feature.json, write feature tests, or review a feature against best practices.
---

# Dev Container Feature Creator

This skill acts as an implementation manual to assist you in scaffolding, developing, updating, and extensively testing Dev Container Features. It leverages the official Dev Container Features specification, testing framework, and authoring best practices.

## Core Principles

- **Mandatory Planning:** Before scaffolding or modifying a feature, you MUST draft a design plan and obtain user approval. The plan should outline the feature ID, options, installation strategy, and testing scenarios.
- **Idempotency:** Installation scripts MUST be idempotent. They should be safe to run multiple times with different options without failing or causing unintended side effects.
- **OS Compatibility:** Installation scripts should verify the OS/distro at the beginning and support a diverse set of base images, defaulting to `sh` or safely bootstrapping `bash`.
- **Handling Non-Root Users:** Scripts run as `root`, but the final user might not be root. Use `_REMOTE_USER` to set permissions appropriately.
- **Comprehensive Testing:** Always implement auto-generated tests, scenario tests, and duplicate tests using the `devcontainer features test` command framework.

## Workflow

Follow these steps to construct or update a Dev Container Feature:

### 1. Analyze & Scaffold
- Check the workspace structure. Features usually live in `src/<feature-name>/` and their tests in `test/<feature-name>/`.
- Create these directories if they don't exist.

### 2. Configure Metadata
- Create or update `src/<feature-name>/devcontainer-feature.json`.
- Define the feature `id`, `version`, `name`, `description`, and any configurable `options`.
- Use `assets/base-devcontainer-feature.json` as a starting point.
- See `references/feature-spec.md` for metadata schema details.

### 3. Implementation & Best Practices
- Draft the entry point script: `src/<feature-name>/install.sh`.
- Options defined in the metadata are passed to the script as uppercase environment variables (e.g., `OPTIONNAME`).
- Adhere strictly to the guidelines in `references/authoring-best-practices.md`:
  - Check for OS support.
  - Set up logic for the `_REMOTE_USER`.
  - Minimize layers by cleaning package manager caches within the script.
- Ensure the script is executable (`chmod +x`).
- Use `assets/base-install.sh` as a template.

### 4. Documentation
- Create a `src/<feature-name>/README.md` to document the feature, its options, and examples of usage.
- Alternatively, if the devcontainer CLI is available, suggest running `devcontainer features generate-docs` to auto-generate the README from the metadata.

### 5. Testing
- Setup a comprehensive test suite in `test/<feature-name>/`.
- **Auto-generated test:** Create `test/<feature-name>/test.sh` to test default behavior.
- **Scenarios:** Create `test/<feature-name>/scenarios.json` and a corresponding `<scenario-name>.sh` to test specific option combinations or multi-feature configurations.
- **Duplicate tests:** Create `test/<feature-name>/duplicate.sh` to assert that installing the feature twice with different options does not conflict (ensuring idempotency).
- Use `assets/base-test.sh` as a boilerplate for test scripts and utilize the `dev-container-features-test-lib` framework.
- Reference `references/testing-spec.md` for comprehensive details on the testing framework.

## Reference Materials

- [feature-spec.md](references/feature-spec.md): Schema for `devcontainer-feature.json` and context for `install.sh`.
- [testing-spec.md](references/testing-spec.md): Guidelines on how to write tests for dev container features.
- [authoring-best-practices.md](references/authoring-best-practices.md): Official best practices for creating resilient and efficient features.
