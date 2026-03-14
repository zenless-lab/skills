# Formatter-Linter Compatibility

This reference helps an agent avoid policy conflicts when Ruff is used as both linter and formatter, or when it coexists with Black.

## 1. Keep Formatting and Style Linting Aligned

The safest Ruff setup is one in which formatting choices do not create new lint failures.

That usually means:

* avoiding style rules that fight the formatter
* keeping line length and quote policy consistent across the toolchain
* deciding clearly whether Ruff formatter replaces Black or complements a different formatter

## 2. Common Conflict Areas

### Line length

Formatters make a best effort to wrap code, but lint rules like `E501` still flag long lines that remain, such as comments, URLs, or some string-heavy constructs.

If Black or Ruff formatter already governs wrapping, decide explicitly whether `E501` is still desirable.

### Quote policy

If Ruff formatter enforces a quote style, quote-oriented lint rules can become redundant or conflicting unless configured carefully.

### Indentation and trailing commas

Indentation, trailing-comma, and multiline string rules can overlap with formatter output. Avoid enabling these rules casually in formatter-owned projects.

### Docstring formatting

If docstring example formatting is enabled, verify that docstring-related lint rules and documentation expectations still agree.

## 3. Import Sorting and Formatting

Ruff can also cover import organization through lint rules.

Before enabling import-sorting behavior, confirm:

* whether isort is still active
* whether CI already checks import order separately
* whether import grouping rules are defined by existing config

Do not let multiple tools rewrite imports without a clear ownership decision.

## 4. Recommended Compatibility Profiles

### Ruff formatter replaces Black

Use this when the repository wants one tool for both formatting and linting.

Checklist:

* match line length to team expectations
* avoid formatter-conflicting style rules
* ensure pre-commit and CI no longer invoke Black

### Ruff linting with Black retained

Use this when the repository trusts Black as formatter of record.

Checklist:

* align `line-length`
* avoid overlapping style lint categories unless intentionally enforced
* keep command order predictable in hooks and CI

## 5. Notebook and Documentation Compatibility

Notebook and documentation formatting can widen Ruff's reach beyond standard `.py` files. Only enable these paths if the repository wants them reviewed with the same discipline as source code.

When in doubt, exclude them explicitly and revisit later.

## 6. Agent Decision Rules

When evaluating formatter-linter compatibility, answer these questions:

1. Which tool owns formatting today?
2. Which tool owns import sorting today?
3. Is line length supposed to be advisory or enforced?
4. Are docstring examples or notebooks in scope?
5. Will this configuration make formatting produce fresh lint failures?

If the answer to the last question is yes, adjust the lint policy before rollout.
