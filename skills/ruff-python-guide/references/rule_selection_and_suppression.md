# Rule Selection and Suppression

This reference covers how to expand Ruff's rule set without making the project noisy or opaque.

## 1. Start Narrow, Then Expand

Ruff can enforce many rule families, but broad enablement is rarely the right first move.

Recommended progression:

1. Start from defaults or near-defaults.
2. Add one category at a time.
3. Review error volume and false positives.
4. Decide whether each category should be fixable, suppressible, or deferred.

## 2. Prefer Explicit Rule Policy

Use `select` when the repository wants a clear baseline. Use `extend-select` when building on a known base intentionally.

Common families:

* `F` for Pyflakes-style correctness
* `E` for pycodestyle error classes
* `B` for bug-prone patterns
* `I` for import ordering
* `UP` for Python modernization
* `D` for docstring enforcement
* `Q` for quote-style linting

Be careful with style-oriented families when Ruff formatter or Black already governs the same space.

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
2. block range suppressions for a specific rule set
3. file-level `# ruff: noqa: CODE`
4. `per-file-ignores` in config
5. global `ignore`

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

## 8. Migration Pattern for Existing Codebases

When adding a new rule family to a mature repository:

1. enable the rule in a branch
2. inspect the error distribution
3. fix obviously safe issues
4. decide whether remaining exceptions belong in config or source
5. only then consider `--add-noqa` for residual legacy cases

## 9. Review Checklist

Before approving a rule-policy change, confirm:

1. why this rule family is being added
2. whether formatting tools overlap with it
3. whether auto-fix is acceptable
4. whether suppressions are local and understandable
5. whether CI behavior stays predictable after the change
