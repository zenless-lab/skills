# Troubleshooting and Migration

This reference helps an agent diagnose common Ruff adoption failures and plan migrations from other Python tooling.

## 1. Symptom: Too Many Violations at First Run

Likely causes:

* too many rule families enabled immediately
* repository never had a linter baseline
* notebooks, generated files, or vendored code were included unintentionally

Recommended response:

1. narrow the rule set
2. exclude non-source paths deliberately
3. migrate by directory or rule family
4. use targeted suppressions only after classifying the remaining issues

## 2. Symptom: Formatter and Linter Disagree

Likely causes:

* line-length linting is stricter than formatter output
* quote or docstring rules overlap with formatter decisions
* multiple tools still own formatting behavior

Recommended response:

1. identify the formatter of record
2. align line length and quote expectations
3. disable or adjust overlapping style rules
4. simplify hook and CI ownership

## 3. Symptom: CI and Local Results Differ

Likely causes:

* different Ruff versions
* different working directories or config resolution
* local editor uses a different executable path
* CI runs verification only while local development uses fixes

Recommended response:

1. standardize installation source
2. make config file location explicit
3. align command sequences across environments
4. document intentional differences

## 4. Symptom: Imports or Modernization Changes Feel Risky

Likely causes:

* fix behavior was enabled without reviewing safety
* modernization rules touched compatibility-sensitive code
* import rewrites interact with package initialization or side effects

Recommended response:

* keep risky rule families review-only at first
* use `unfixable` or scoped suppressions where behavior matters
* validate package initialization and import side effects after rewrites

## 5. Migrating from Flake8

Migration pattern:

1. identify active Flake8 plugins and their purpose
2. map only the needed rule families into Ruff
3. avoid copying a large historic ignore list blindly
4. re-evaluate old suppressions because Ruff may classify issues differently

Good default posture:

* begin with correctness and bug-prone rules
* add style-oriented or framework-specific rules later

Ruff can replace Flake8 effectively when the project uses Flake8 with no plugins or a modest plugin set, especially when paired with Black or Ruff formatter on Python 3 code. Do not claim that every historical Flake8 plugin maps perfectly without verification.

## 6. Migrating from Black

Before replacing Black with Ruff formatter, confirm:

* the team accepts a near-compatible rather than identical formatter
* save hooks and CI can be updated together
* line length and quote policy stay coherent

Rollout advice:

* run formatter diffs on a branch first
* review noisy edge cases such as comments and docstring examples
* remove redundant formatter steps only after the new flow is stable

Describe the migration target as near-compatible, not identical. That wording matches Ruff's own compatibility posture.

## 7. Ruff Alongside Pylint or Type Checkers

Ruff is not a full substitute for a type checker, and it does not mirror every Pylint behavior.

Use this split:

* Ruff for fast structural, stylistic, and modernization feedback
* type checkers for semantic type analysis
* Pylint only where its project-specific checks still justify the overlap

Useful boundary statements:

* Ruff is a linter, not a type checker.
* Ruff and Pylint overlap, but they do not enforce the same rule set.
* Ruff does not support custom third-party lint plugins today.

## 8. Other Migration Questions

### Replacing isort

Ruff's import sorting is generally close to isort with `profile = "black"`, but there are edge-case differences. Validate import-heavy modules before removing isort from automation.

### Replacing Black and isort together

If Ruff takes over both formatting and import sorting, remove overlapping hook and CI steps in the same change set or document the temporary mixed state explicitly.

### Python version support

Ruff lints Python `3.7+` code and is installable on Python `3.7+`. If the repository targets older syntax or runtime compatibility shims, validate modernization rules carefully.

## 9. Migration Review Checklist

Before calling the migration complete, confirm:

1. the chosen rule set is documented
2. formatter ownership is unambiguous
3. pre-commit and CI reflect the same policy
4. suppressions are understandable and minimal
5. local developers can reproduce CI outcomes
