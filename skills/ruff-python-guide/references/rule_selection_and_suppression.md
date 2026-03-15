# Rule Selection and Suppression

This reference covers how to expand Ruff's rule set without making the project noisy or opaque.

## 1. Start Narrow, Then Expand

Ruff can enforce many rule families, but broad enablement is rarely the right first move.

Ruff's default rule set is intentionally narrow: it enables Pyflakes `F` plus a subset of pycodestyle `E` rules, while omitting warning classes like `W` and complexity checks like `C901` by default.

Recommended progression:

1. Start from defaults or near-defaults.
2. Add one category at a time.
3. Review error volume and false positives.
4. Decide whether each category should be fixable, suppressible, or deferred.

## 2. Prefer Explicit Rule Policy

Use `select` when the repository wants a clear baseline. Use `extend-select` when building on a known base intentionally.

Common families:

* `A` for flake8-builtins shadowing checks
* `B` for flake8-bugbear bug-prone patterns
* `C4` for flake8-comprehensions cleanup and simplification
* `DTZ` for naive datetime safety checks
* `F` for Pyflakes-style correctness
* `E` for pycodestyle error classes
* `EM` for exception message construction rules
* `I` for import ordering
* `ICN` for import alias conventions
* `INP` for implicit namespace package checks
* `ISC` for implicit string concatenation checks
* `N` for PEP 8 naming checks
* `NPY` for NumPy-specific linting
* `PD` for pandas-vet data-frame usage checks
* `PL` for the Pylint rule families
* `Q` for quote-style linting
* `RUF` for Ruff-specific lint rules
* `S` for security-oriented flake8-bandit checks
* `T10` for debugger statement checks
* `T20` for print and pprint statement checks
* `TID` for tidy-import rules such as relative import restrictions
* `UP` for Python modernization
* `D` for docstring enforcement
* `W` for pycodestyle warning classes
* `YTT` for version-check and year-2020 compatibility rules

Be careful with style-oriented families when Ruff formatter or Black already governs the same space.

If the repository is new to linting, the default rule set is the best initial baseline more often than a broad custom selection.

## 3. Treat `ALL` as a Governance Choice

`ALL` is useful only when the team is ready to adopt new rules on future Ruff upgrades.

Use it only if:

* change management is deliberate
* CI noise from new releases is acceptable
* the repository is maintained closely enough to react to new diagnostics

Otherwise, keep selection explicit.

## 4. Fix Policy Matters

Ruff can fix many rules automatically.

Use these controls intentionally:

* `fixable`
* `unfixable`
* `extend-safe-fixes`
* `extend-unsafe-fixes`

This is especially important during migration, where some rule families are safe to auto-clean while others should remain review-only.

## 5. Suppression Ladder

Prefer suppressions in this order, from narrowest to broadest:

1. inline `# noqa: CODE`
2. file-level `# ruff: noqa: CODE`
3. `per-file-ignores` in config
4. global `ignore`

Use the smallest scope that solves the problem.

## 6. When to Use `per-file-ignores`

Use `per-file-ignores` when the exception is structural rather than accidental.

Examples:

* `__init__.py` files that intentionally re-export names
* notebooks with exploratory print statements
* generated files or compatibility shims

Prefer this over repeated inline `noqa` comments when the exception pattern is stable and predictable.

## 7. When to Use Inline `noqa`

Use inline suppression when a single line is intentionally exceptional and the rationale is local to that statement.

Good examples:

* deliberate import side effects
* compatibility aliases
* exact string literals or patterns required by an API

Avoid blanket `# noqa` unless a coded suppression would be unreasonably noisy.

Prefer code-specific suppressions such as `# noqa: UP035` over a bare `# noqa`.

## 8. Migration Pattern for Existing Codebases

When adding a new rule family to a mature repository:

1. enable the rule in a branch
2. inspect the error distribution
3. fix obviously safe issues
4. decide whether remaining exceptions belong in config or source
5. only then consider `--add-noqa` for residual legacy cases

`--add-noqa` is a migration tool, not the default steady-state suppression strategy.

## 9. Review Checklist

Before approving a rule-policy change, confirm:

1. why this rule family is being added
2. whether formatting tools overlap with it
3. whether auto-fix is acceptable
4. whether suppressions are local and understandable
5. whether CI behavior stays predictable after the change
