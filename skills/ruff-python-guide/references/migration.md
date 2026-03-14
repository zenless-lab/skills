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

## 6. Migrating from Black

Before replacing Black with Ruff formatter, confirm:

* the team accepts a near-compatible rather than identical formatter
* save hooks and CI can be updated together
* line length and quote policy stay coherent

Rollout advice:

* run formatter diffs on a branch first
* review noisy edge cases such as comments and docstring examples
* remove redundant formatter steps only after the new flow is stable

## 7. Ruff Alongside Pylint or Type Checkers

Ruff is not a full substitute for a type checker, and it does not mirror every Pylint behavior.

Use this split:

* Ruff for fast structural, stylistic, and modernization feedback
* type checkers for semantic type analysis
* Pylint only where its project-specific checks still justify the overlap

## 8. Migration Review Checklist

Before calling the migration complete, confirm:

1. the chosen rule set is documented
2. formatter ownership is unambiguous
3. pre-commit and CI reflect the same policy
4. suppressions are understandable and minimal
5. local developers can reproduce CI outcomes
