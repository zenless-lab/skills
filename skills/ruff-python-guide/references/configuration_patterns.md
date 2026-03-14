# Ruff Configuration Patterns

This reference summarizes practical configuration layouts for common repository shapes.

## 1. File Selection Strategy

Ruff reads the closest matching configuration file for each analyzed file.

Supported files:

* `pyproject.toml`
* `ruff.toml`
* `.ruff.toml`

Use this decision rule:

* Use `pyproject.toml` when Python tooling is centralized.
* Use `ruff.toml` when Ruff needs a dedicated, readable configuration.
* Use `.ruff.toml` only when hidden-file precedence is intentional.

Ruff does not implicitly merge parent configurations. If you need inheritance, use `extend` deliberately.

## 2. Baseline Shared Settings

Most repositories should make these choices explicit:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F"]

[tool.ruff.format]
quote-style = "double"
```

Key points:

* `line-length` should match the formatter policy used by the repository.
* `target-version` should match supported Python, not the newest local interpreter by accident.
* `select` should be explicit once the team moves beyond pure defaults.

## 3. Common Configuration Patterns

### Unified lint and format

Use Ruff for both linting and formatting when the project wants one primary toolchain.

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "B", "I", "UP"]

[tool.ruff.format]
quote-style = "double"
docstring-code-format = true
```

### Lint-only alongside Black

Use this when Black remains the formatter of record.

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "B", "I", "UP"]
ignore = ["E501"]
```

Why ignore `E501` here:

* formatters make a best effort on line wrapping, but lint line-length enforcement can still fire on long comments or strings.

### Formatter-only adoption

Use this when a team wants fast formatting first and will revisit lint policy later.

Keep lint settings narrow or absent until rule policy is ready.

### Incremental tightening for mature teams

Add rule families one category at a time, for example:

* `B` for bugbear
* `I` for import sorting
* `UP` for modernization
* `D` for docstring policy

Avoid enabling a broad set without checking interaction with existing code and automation.

## 4. Per-File and Scoped Overrides

Use `per-file-ignores` when a rule is valid generally but noisy in specific locations.

Common examples:

* allowing import placement exceptions in package initializers
* relaxing rules for generated code
* treating notebooks differently from library modules

Example:

```toml
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["E402"]
"*.ipynb" = ["T20"]
```

## 5. Notebook and Markdown Considerations

Ruff can operate on notebooks, and some formatting features also extend to code blocks in documentation-focused files.

Use explicit include or exclude settings when notebooks or documentation are intentionally out of scope. Keep lint and format exclusions separate if only one behavior should apply.

## 6. Monorepo and Extended Configs

Use `extend` when multiple packages should inherit a shared Ruff baseline while allowing local overrides.

Pattern:

```toml
[tool.ruff]
extend = "../pyproject.toml"
line-length = 100
```

Use this when:

* teams want one central baseline
* packages need local exceptions
* local config should stay small and reviewable

## 7. Configuration Review Checklist

Before finalizing a Ruff config, confirm:

1. the file location matches repo conventions
2. target Python is explicit
3. line length matches formatter policy
4. rule selection is intentional, not accidental drift
5. per-file overrides are narrow and justified
6. CI and pre-commit commands match the config's purpose
