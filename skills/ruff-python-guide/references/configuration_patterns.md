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

If multiple Ruff config files exist in the same directory, `.ruff.toml` takes precedence over `ruff.toml`, and `ruff.toml` takes precedence over `pyproject.toml`.

Two discovery rules matter during troubleshooting:

* Ruff ignores a `pyproject.toml` that does not contain `[tool.ruff]` when searching for the closest config.
* If `--config path/to/file` is passed on the command line, that config is used for all analyzed files, and relative paths inside it are resolved from the current working directory.

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

If `target-version` is omitted, Ruff may infer it from a nearby `pyproject.toml` via the `requires-python` field. Prefer setting one of the two intentionally.

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

Use this only if the repository intends Ruff to own formatting. If Black is still active, remove overlapping formatter ownership first.

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

Use `lint.exclude` or `format.exclude` when notebooks should participate in only one side of Ruff's behavior.

## 5. Notebook and Markdown Considerations

Ruff discovers `*.py`, `*.pyi`, `*.ipynb`, and `pyproject.toml` by default. In preview mode, it also discovers `*.pyw` by default.

Ruff has built-in notebook support and, as of `0.6.0`, lints and formats notebooks by default.

Ruff can operate on notebooks, and some formatting features also extend to code blocks in documentation-focused files.

Use explicit include or exclude settings when notebooks or documentation are intentionally out of scope. Keep lint and format exclusions separate if only one behavior should apply.

Important include rule:

* `include` patterns must match files, not directories. `include = ["src"]` is invalid.

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

Remember that `extend` is Ruff's explicit inheritance mechanism. Parent configs are otherwise ignored.

## 7. Command-line Overrides

Use dedicated flags for common overrides such as `--select`, `--line-length`, or `--target-version`.

Use `--config` in two distinct ways:

* to point Ruff at a config file
* to override individual settings with TOML fragments, such as `--config "lint.per-file-ignores = {'__init__.py' = ['E402']}"`

Dedicated command-line flags take precedence over `--config` overrides for the same option.

## 8. Configuration Review Checklist

Before finalizing a Ruff config, confirm:

1. the file location matches repo conventions
2. target Python is explicit
3. line length matches formatter policy
4. rule selection is intentional, not accidental drift
5. per-file overrides are narrow and justified
6. CI and pre-commit commands match the config's purpose
