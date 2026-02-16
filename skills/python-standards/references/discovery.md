# Python Style Discovery Guide for LLMs

This reference guide helps an LLM quickly identify and adhere to a project's existing Python coding style by scanning specific configuration files.

## 1. General Configuration: `.editorconfig`

The universal standard for cross-editor settings.

* **Target:** Look for `[*.py]` or `[*]` blocks.
* **Key Fields:**
    - `indent_style`: `space` or `tab`.
    - `indent_size`: Usually `4` or `2`.
    - `max_line_length`: The hard limit for line wrapping.

## 2. The Modern Hub: `pyproject.toml`

The primary configuration file for most modern Python tools. Check the `[tool.*]` sections:

* **Black:** `[tool.black]`
    - *Focus on:* `line-length` (default is 88).
* **Ruff:** `[tool.ruff]`
    - *Focus on:* `line-length`, `target-version`, and `lint.select` (rule sets like E, F, I).
* **Pylint:** `[tool.pylint.format]` or `[tool.pylint.messages_control]`
    - *Focus on:* `max-line-length`, `disable`.
* **isort:** `[tool.isort]`
    - *Focus on:* `profile` (e.g., `profile = "black"`).

## 3. Tool-Specific Configuration Files

If configurations are not in `pyproject.toml`, check these standalone files:

| Tool | Config Files (Ordered by Priority) |
| --- | --- |
| **Ruff** | `ruff.toml`, `.ruff.toml` |
| **Pylint** | `.pylintrc`, `pylintrc`, `setup.cfg`, `tox.ini` |
| **Black** | Almost exclusively in `pyproject.toml` |
| **Flake8** | `.flake8`, `setup.cfg`, `tox.ini` |
| **Autopep8** | `.pep8`, `setup.cfg` |

## 4. Style Inference Logic

When analyzing a project, apply the following hierarchy:

* **Indentation:** Check `.editorconfig` first. If missing, check `pyproject.toml` (Black/Ruff). Default to **4 spaces** if no config is found.
* **Line Length:**
    - If **Black** is present: Default is **88**.
    - If **Flake8/PEP8** is present: Default is **79**.
    - Otherwise, look for explicit `line-length` or `max-line-length` values.
* **Quotes:**
    - Black defaults to **double quotes** (`"`).
    - If not using Black, observe existing code for single vs. double quote preference.
* **Imports:** Check for `isort` or Ruff’s `I` (isort) rules to determine grouping and alphabetization logic.

## 5. Quick Scan Prompt Example

> "Scan the root directory for `pyproject.toml`, `.editorconfig`, and `.flake8`. Identify the indentation style, max line length, and preferred linter/formatter settings so I can match this project's coding style."
