# Ruff Installation and Bootstrap

This reference helps an agent choose an installation path that matches the repository, then introduce Ruff with a low-risk first run.

## 1. Choose the Installation Scope

Use the installation method that matches the project's operational needs.

### Project-local installation

Best when Ruff is part of the repository's standard toolchain.

Use this when:

* CI should run the same version as local development.
* pre-commit hooks depend on a declared tool version.
* the repository already manages Python tooling with `uv`, `pip`, Poetry, or package metadata.

Common patterns:

```bash
uv add --dev ruff
```

```bash
pip install ruff
```

After project-local installation, prefer running Ruff through the project environment:

```bash
uv run ruff check
uv run ruff format
```

As an alternative to `uv run`, users can activate the virtual environment and invoke `ruff` directly.

### Global or ephemeral execution

Best for quick checks, one-off migrations, or environments where the project should not own the tool.

Common patterns:

```bash
uvx ruff check
uvx ruff format
```

```bash
uv tool install ruff@latest
```

```bash
pipx install ruff
```

Use this carefully for teams, since ephemeral or global execution can drift from CI behavior.

## 2. Package Manager and Platform Installs

Ruff is available through multiple distribution channels. Mention only the ones relevant to the user's environment.

### Standalone installers

Starting with Ruff `0.5.0`, standalone installers are available:

```bash
curl -LsSf https://astral.sh/ruff/install.sh | sh
```

```powershell
powershell -c "irm https://astral.sh/ruff/install.ps1 | iex"
```

Version-pinned installer example:

```bash
curl -LsSf https://astral.sh/ruff/0.5.0/install.sh | sh
```

Ruff ships with wheels for major platforms, so users do not need a Rust toolchain to install it through normal package managers.

### OS and ecosystem package managers

Useful options when the user explicitly prefers system-managed tools:

```bash
brew install ruff
conda install -c conda-forge ruff
pkgx install ruff
pacman -S ruff
apk add ruff
sudo zypper install python3-ruff
```

Treat these as environment-specific alternatives, not the default recommendation for repository automation.

### Docker and container execution

Ruff is published as `ghcr.io/astral-sh/ruff`.

Examples:

```bash
docker run -v .:/io --rm ghcr.io/astral-sh/ruff check
docker run -v .:/io --rm ghcr.io/astral-sh/ruff:0.3.0 check
```

For Podman on SELinux:

```bash
docker run -v .:/io:Z --rm ghcr.io/astral-sh/ruff check
```

Use containerized execution when CI or a local workflow wants Ruff without a Python environment bootstrap.

## 3. Pick the First Execution Mode

Avoid starting with auto-fixes in a repository you have not inspected.

Recommended order:

1. Run `ruff check` to see the current error surface.
2. Review whether Ruff is already configured by local files.
3. Add or adjust configuration.
4. Run `ruff check --fix` only after confirming fix scope is acceptable.
5. Run `ruff format` only if Ruff is intended to own formatting.

Representative first run:

```bash
uv run ruff check
uv run ruff check --fix
uv run ruff format
```

Use direct `ruff ...` invocations only when the executable source is already explicit.

## 4. Decide Where Configuration Should Live

Ruff supports:

* `pyproject.toml`
* `ruff.toml`
* `.ruff.toml`

Choose `pyproject.toml` when the repository centralizes Python tooling in one file. Choose `ruff.toml` or `.ruff.toml` when teams want Ruff settings isolated or layered more explicitly.

If multiple Ruff config files exist in the same directory, `.ruff.toml` takes precedence over `ruff.toml`, and `ruff.toml` takes precedence over `pyproject.toml`.

## 5. Safe Bootstrap Profiles

### Starter profile for new adoption

Use Ruff defaults first, or make a very small extension over the defaults.

```toml
[tool.ruff]
line-length = 120

[tool.ruff.lint]
extend-select = [
    "E",    # pycodestyle error: PEP 8 styling errors
    "I",    # isort: Import sorting
    "N",    # pep8-naming: Check PEP 8 naming conventions
    "S",    # flake8-bandit: Security testing
    "T10",  # flake8-debugger: Check for debugger imports and set_trace calls
    "T20",  # flake8-print: Check for print statements
    "TID",  # flake8-tidy-imports: Tidy up imports
    "UP",   # pyupgrade: Upgrade syntax for newer Python versions
    "W",    # pycodestyle warning: PEP 8 styling warnings
]
```

Why this works:

* It stays close to Ruff's default posture while broadening pycodestyle coverage in a predictable way.
* It catches common correctness and warning-level issues without jumping immediately to large plugin families.
* It avoids immediately importing large style debates into the migration.

### Formatter-first profile

Use this when the team wants fast formatting but is not ready to change lint policy.

```toml
[tool.ruff]
line-length = 120

[tool.ruff.format]
quote-style = "double"
```

### Lint-first profile

Use this when formatting is still owned by Black or another formatter.

Keep formatter-related lint conflicts in mind before enabling stylistic rules.

## 6. Choose the Version and Python Target Explicitly

Prefer recording the Python target or inferring it consistently from project metadata.

Set one of:

* `requires-python` in `pyproject.toml`
* `target-version` in Ruff settings

This avoids version-sensitive rule churn and keeps auto-fixes aligned with the supported interpreter range.

## 7. First Questions an Agent Should Answer

Before installing or editing Ruff, answer these:

* Is Ruff already present in dependencies or hooks?
* Is the project replacing Black, Flake8, isort, or only part of that stack?
* Is CI expected to fail on violations, auto-fix locally, or both?
* Are notebooks or Markdown code blocks part of the workflow?
* Does the user want repository-managed installation, host-level installation, or containerized execution?

## 8. Recommended First-Run Output

When helping a user bootstrap Ruff, report:

1. chosen installation path
2. chosen config file location
3. initial command sequence
4. whether Ruff is lint-only, format-only, or both
5. migration risks with existing tooling
