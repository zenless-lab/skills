# Integrations: pre-commit, CI, and editors

This reference explains how to integrate Ruff into GitHub Actions, GitLab CI/CD, pre-commit, Markdown formatting workflows, Docker-based execution, and editor automation.

The copy-paste-ready templates live in `assets/`:

* `assets/github_actions_ci.yml`
* `assets/github_actions_ruff_action.yml`
* `assets/gitlab-ci.yml`
* `assets/pre-commit-basic.yml`
* `assets/pre-commit-fix.yml`
* `assets/pre-commit-no-notebooks.yml`

## 1. GitHub Actions

GitHub Actions can run Ruff directly with a normal Python setup, or indirectly through `ruff-action`.

### Direct CLI workflow

Use this when the workflow already manages Python installation and dependencies explicitly.

Template: `assets/github_actions_ci.yml`

Representative pattern:

```yaml
name: CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff
      - name: Run Ruff
        run: ruff check --output-format=github .
```

`--output-format=github` enables GitHub-style inline annotations in workflow output.

### `ruff-action` workflow

Use this when you want Ruff installation handled by the action itself.

Template: `assets/github_actions_ruff_action.yml`

Minimal workflow:

```yaml
name: Ruff
on: [ push, pull_request ]
jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/ruff-action@v3
```

You can also embed the action into an existing workflow as a single step:

```yaml
- uses: astral-sh/ruff-action@v3
```

By default, `ruff-action` runs Ruff as a pass-fail lint step using the repository configuration. Under the hood it installs and runs Ruff directly, so it can execute any supported Ruff command, including `ruff check --fix`.

Useful `with:` parameters:

* `version`: Ruff version to install. Default is the latest published version.
* `args`: Command-line arguments passed to Ruff. Default is `check`.
* `src`: Source paths passed to Ruff. Default is `.` and `src`.

Example customization:

```yaml
- uses: astral-sh/ruff-action@v3
  with:
    version: 0.8.0
    args: check --select B
    src: "./src"
```

Use this form when you want to pin Ruff independently of the base image or Python dependency installation logic.

## 2. GitLab CI/CD

Use this when you want `ruff check` and `ruff format --diff` in CI, while also producing a GitLab code quality artifact.

Template: `assets/gitlab-ci.yml`

Representative pattern:

```yaml
.base_ruff:
  stage: build
  interruptible: true
  image:
    name: ghcr.io/astral-sh/ruff:0.15.6-alpine
  before_script:
    - cd $CI_PROJECT_DIR
    - ruff --version

Ruff Check:
  extends: .base_ruff
  script:
    - ruff check --output-format=gitlab --output-file=code-quality-report.json
  artifacts:
    reports:
      codequality: $CI_PROJECT_DIR/code-quality-report.json

Ruff Format:
  extends: .base_ruff
  script:
    - ruff format --diff
```

This keeps lint diagnostics machine-readable for GitLab while still checking formatting without mutating files.

## 3. pre-commit

Ruff can be installed through `ruff-pre-commit` and used for linting, auto-fixing, and formatting.

### Basic lint and format hooks

Template: `assets/pre-commit-basic.yml`

Representative pattern:

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.15.6
  hooks:
    - id: ruff-check
    - id: ruff-format
```

This matches Ruff's documented pattern for integrating both linter and formatter through `ruff-pre-commit`.

### Enable automatic fixes

Template: `assets/pre-commit-fix.yml`

Use `--fix` on the lint hook when mutation is acceptable:

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.15.6
  hooks:
    - id: ruff-check
      args: [ --fix ]
    - id: ruff-format
```

### Exclude notebooks

Template: `assets/pre-commit-no-notebooks.yml`

To avoid running on Jupyter Notebooks, remove `jupyter` from the accepted file types:

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.15.6
  hooks:
    - id: ruff-check
      types_or: [ python, pyi ]
      args: [ --fix ]
    - id: ruff-format
      types_or: [ python, pyi ]
```

Use this when the repository wants Ruff for Python modules but not for notebook files.

Operational rules:

* If `ruff-check` runs with `--fix`, place it before `ruff-format`.
* If `ruff-check --fix` is used alongside Black, isort, or another formatter, keep Ruff's lint hook before those tools too.
* If Ruff runs without `--fix`, the linter and formatter order is flexible.
* If Ruff is verify-only in CI, prefer `ruff check`, `ruff format --check`, or `ruff format --diff`.
* If your Ruff configuration avoids formatter-linter conflicts, `ruff format` should not introduce new lint violations after `ruff check --fix`.

## 4. Markdown and Docker integrations

### `mdformat`

`mdformat` can format code blocks inside Markdown. The `mdformat-ruff` plugin lets it format Python code blocks with Ruff.

Use this only when Markdown code samples are part of the repository quality bar.

### Docker

Ruff publishes a distroless image containing the `ruff` binary, plus additional base-image variants.

Published tags include:

* `ruff:latest`
* `ruff:{major}.{minor}.{patch}`, for example `ruff:0.6.6`
* `ruff:{major}.{minor}`, for example `ruff:0.6`
* `ruff:alpine`
* `ruff:alpine3.20`
* `ruff:debian-slim`
* `ruff:bookworm-slim`
* `ruff:debian`
* `ruff:bookworm`

Versioned base-image tags also exist, such as `ruff:0.6.6-alpine`.

Use distroless when you only need Ruff itself. Use Alpine or Debian-based variants when the CI job needs shell access or auxiliary tooling.

## 5. Editor workflow guidance

Keep editor behavior aligned with repository policy:

* prefer the project-managed Ruff version when possible
* do not silently run multiple formatters on save unless the ordering is intentional
* keep local save actions aligned with CI commands
* avoid enabling fix-on-save if CI is intended to be report-only
* prefer notebook-prefixed code actions in VS Code notebooks over generic `source.*` actions

For notebooks, Ruff needs full-notebook context for accurate diagnostics and fixes. Generic per-cell `source.organizeImports` or `source.fixAll` save actions can therefore produce confusing results.

## 6. Integration checklist

Before finalizing automation, confirm:

1. the Ruff version source is explicit
2. local and CI commands are intentionally aligned
3. fix behavior is enabled only where mutation is acceptable
4. notebooks, docs, and generated files are included only by choice
5. overlapping tools like Black, isort, and Pylint have clear ownership
