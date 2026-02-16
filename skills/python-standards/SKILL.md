---
name: python-standards
description: Use this skill to apply Python coding standards in an existing or new project, infer project style from configuration, and load the right style, docstring, and layout references with PEP 8 as the primary baseline.
---

# Python Standards Skill

Use this skill when you need to write or review Python code with consistent,
practical standards.

## Skill Overview

This skill helps you:

1. Detect a project's actual Python style before making changes.
2. Apply PEP 8 and Google Python Style Guide conventions.
3. Keep changes consistent with existing code.
4. Use progressive loading: load only the references required for the current task.

When PEP 8 and Google style differ, prefer **PEP 8 first**, then use Google
style as complementary guidance.

Only if you are uncertain about what PEP 8 or Google Python Style Guide means,
load [references/style.md](references/style.md) as a brief summary.

## Core Principles

Always apply these principles in order:

1. **Existing Code First**: Match the surrounding repository style when maintaining existing code.
2. **Readability Above All**: Optimize for clarity and maintainability.
3. **Break Rules When Necessary**: If a strict rule hurts readability, prioritize a clearer implementation.

These principles still operate within a PEP 8-first baseline unless the project
already established a different convention.

## Workflow

### Step 1: Discover Project Style

Before changing code, inspect project configuration using
[references/discovery.md](references/discovery.md).

At minimum, check for:

- `.editorconfig`
- `pyproject.toml`
- `ruff.toml` / `.ruff.toml`
- `.flake8`
- `.pylintrc` / `pylintrc`
- `setup.cfg` / `tox.ini`

Infer and follow:

- indentation
- line length
- formatter/linter stack
- import ordering rules
- quote preferences (if not formatter-enforced)

If uncertain about project style, use discovery guidance to
confirm settings first.

### Step 2: Apply Style Priority

Apply style in this order:

1. Project config and surrounding code style.
2. PEP 8 as the primary baseline.
3. Google Python Style Guide as complementary guidance.

Load [references/style.md](references/style.md) **only if** the agent is
uncertain about PEP 8 or Google style definitions. Treat it as a brief summary,
not a mandatory full reference.

### Step 3: Load Docstring Style Reference

Identify existing docstring conventions in the codebase, then load only the
matching reference:

- **Google style** → [references/docstring_styles/google.md](references/docstring_styles/google.md)
- **NumPy style (numpydoc)** → [references/docstring_styles/numpy.md](references/docstring_styles/numpy.md)
- **Sphinx/reST field-list style** → [references/docstring_styles/sphinx_rest.md](references/docstring_styles/sphinx_rest.md)

Selection heuristics:

- Prefer the style already used in nearby modules.
- If docs tooling clearly requires one style, follow that tooling.
- For new projects without constraints, default to Google style unless the team specifies otherwise.

### Step 4: Load Project Layout Reference

Pick the layout guidance that matches repository structure and project type:

- `src/` package layout → [references/layouts/src.md](references/layouts/src.md)
- flat package at root → [references/layouts/flat.md](references/layouts/flat.md)
- FastAPI backend modular layout → [references/layouts/fastapi_modular.md](references/layouts/fastapi_modular.md)
- notebook/data workflow → [references/layouts/data_science.md](references/layouts/data_science.md)

Only load one primary layout reference unless the repository is intentionally
multi-structure.

### Step 5: Implement and Validate

When producing code changes:

- keep edits minimal and focused
- preserve local style patterns
- avoid unnecessary refactors
- verify formatting/lint expectations when possible

## Quick Decision Rules

1. Existing style and config beat generic defaults.
2. PEP 8 is the primary standard.
3. Google style guidance is secondary and complementary.
4. If uncertain, re-run discovery and inspect neighboring files before editing.

## Response Template

When reporting what you applied, summarize in this order:

1. Detected project style signals (from config files).
2. Selected docstring reference and why.
3. Selected layout reference and why.
4. Key style decisions (especially where readability required exceptions).
