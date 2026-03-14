# Ruff Installation and Bootstrap

This reference helps an agent choose a practical Ruff installation path and establish a low-risk first workflow.

## 1. Choose the Installation Scope

Use the installation method that matches the project's operational needs.

### Project-local installation

Best when Ruff is part of the repository's standard toolchain.

Use this when:

* CI should run the same version as local development.
* pre-commit hooks depend on a declared tool version.
* the repository already manages Python tooling with `uv` or package metadata.

Common patterns:

```bash
uv add --dev ruff
```

```bash
pip install ruff
```

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

Use this carefully for teams, since ephemeral or global execution can drift from CI behavior.

## 2. Pick the First Execution Mode

Avoid starting with auto-fixes in a repository you have not inspected.

Recommended order:

1. Run `ruff check` to see the current error surface.
2. Review whether Ruff is already configured by local files.
3. Add or adjust configuration.
4. Run `ruff check --fix` only after confirming fix scope is acceptable.
5. Run `ruff format` only if Ruff is intended to own formatting.

## 3. Decide Where Configuration Should Live

Ruff supports:

* `pyproject.toml`
* `ruff.toml`
* `.ruff.toml`

Choose `pyproject.toml` when the repository centralizes Python tooling in one file. Choose `ruff.toml` or `.ruff.toml` when teams want Ruff settings isolated or layered more explicitly.

If multiple Ruff config files exist in the same directory, the more specific Ruff file takes precedence over `pyproject.toml`.

## 4. Safe Bootstrap Profiles

### Starter profile for new adoption

Use Ruff defaults or near-defaults first.

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F"]
```

Why this works:

* It catches common correctness issues with low noise.
* It avoids immediately importing large style debates into the migration.

### Formatter-first profile

Use this when the team wants fast formatting but is not ready to change lint policy.

```toml
[tool.ruff]
line-length = 88

[tool.ruff.format]
quote-style = "double"
```

### Lint-first profile

Use this when formatting is still owned by Black or another formatter.

Keep formatter-related lint conflicts in mind before enabling stylistic rules.

## 5. Choose the Version and Python Target Explicitly

Prefer recording the Python target or inferring it consistently from project metadata.

Set one of:

* `requires-python` in `pyproject.toml`
* `target-version` in Ruff settings

This avoids version-sensitive rule churn and keeps auto-fixes aligned with the supported interpreter range.

## 6. First Questions an Agent Should Answer

Before installing or editing Ruff, answer these:

* Is Ruff already present in dependencies or hooks?
* Is the project replacing Black, Flake8, isort, or only part of that stack?
* Is CI expected to fail on violations, auto-fix locally, or both?
* Are notebooks or Markdown code blocks part of the workflow?

## 7. Recommended First-Run Output

When helping a user bootstrap Ruff, report:

1. chosen installation path
2. chosen config file location
3. initial command sequence
4. whether Ruff is lint-only, format-only, or both
5. migration risks with existing tooling
