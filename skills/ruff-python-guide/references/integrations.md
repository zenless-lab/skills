# Integrations: pre-commit, CI, and editors

This reference explains when to choose each integration pattern.

The copy-paste-ready templates live in `assets/`:

* `assets/github_actions_ci.yml`
* `assets/github_actions_ruff_action.yml`
* `assets/gitlab-ci.yml`
* `assets/pre-commit-basic.yml`
* `assets/pre-commit-fix.yml`
* `assets/pre-commit-no-notebooks.yml`

## 1. GitHub Actions

### Direct CLI workflow

Use this when the workflow already controls Python installation and dependencies explicitly.

Template: `assets/github_actions_ci.yml`

This mode is easier to align with an existing Python dependency strategy.

### ruff-action workflow

Use this when you want Ruff installation handled by the action itself.

Template: `assets/github_actions_ruff_action.yml`

You can also extract the single step from the asset into a larger workflow if only the install-and-run behavior is needed.

Useful `with:` parameters:

* `version`: Ruff version to install
* `args`: command arguments, defaulting to `check`
* `src`: source paths, defaulting to `.` and `src`

Example:

Typical customization:

* `version` for pinning Ruff
* `args` for changing the command
* `src` for restricting paths

## 2. GitLab CI/CD

This pattern runs `ruff check` and `ruff format --diff` in parallel, while also emitting a GitLab code quality artifact.

Template: `assets/gitlab-ci.yml`

## 3. pre-commit

### Basic lint and format hooks

Template: `assets/pre-commit-basic.yml`

### Enable automatic fixes

When using `--fix`, run the lint hook before the formatter, and before Black, isort, or any downstream formatter.

Template: `assets/pre-commit-fix.yml`

### Exclude notebooks

Template: `assets/pre-commit-no-notebooks.yml`

Operational rules:

* If `ruff-check` runs with `--fix`, place it before `ruff-format`.
* If Ruff formatter coexists with Black or isort, keep ordering explicit.
* If Ruff is verify-only in CI, prefer `ruff check` and `ruff format --check` or `ruff format --diff`.

## 4. Markdown and Docker integrations

### mdformat plugin

`mdformat-ruff` lets `mdformat` format Python code blocks inside Markdown.

### Docker images

Ruff publishes distroless and base-image variants, including:

* `ruff:latest`
* `ruff:{major}.{minor}.{patch}`
* `ruff:{major}.{minor}`
* `ruff:alpine`
* `ruff:alpine3.20`
* `ruff:debian-slim`
* `ruff:bookworm-slim`
* `ruff:debian`
* `ruff:bookworm`

Versioned base-image tags also exist, such as `ruff:0.6.6-alpine`.

## 5. Editor workflow guidance

Keep editor behavior aligned with repository policy:

* prefer the project-managed Ruff version when possible
* do not silently run multiple formatters on save unless the ordering is intentional
* keep local save actions aligned with CI commands

## 6. Integration checklist

Before finalizing automation, confirm:

1. the Ruff version source is explicit
2. local and CI commands are intentionally aligned
3. fix behavior is enabled only where mutation is acceptable
4. notebooks, docs, and generated files are included only by choice
5. overlapping tools like Black, isort, and Pylint have clear ownership
