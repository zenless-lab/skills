---
name: ruff-python-guide
description: Use this skill to introduce, configure, edit, integrate, or troubleshoot Ruff in Python projects. It helps with installation choices, config design, lint and format workflows, rule selection, suppressions, CI and pre-commit integration, and migration from Black, Flake8, or related tools.
---
# Ruff Python Guide

Use this skill when the task involves creating, editing, or operationalizing Ruff configuration for a Python project.

## Skill Overview

This skill helps you:

1. Choose an appropriate Ruff installation and execution model.
2. Design or update Ruff configuration without breaking an existing toolchain.
3. Separate linting, fixing, and formatting workflows clearly.
4. Enable rules incrementally and keep suppressions narrow.
5. Integrate Ruff into local development, pre-commit, and CI.
6. Troubleshoot migration issues and formatter-linter conflicts.

## Core Principles

Always apply these principles in order:

1. **Inspect Before Enforcing**: Check the repository's current formatter, linter, pre-commit hooks, and CI before proposing Ruff changes.
2. **Separate Responsibilities**: Treat `ruff check`, `ruff check --fix`, and `ruff format` as distinct operations with different rollout risks.
3. **Prefer Incremental Adoption**: Start with a narrow rule set and expand deliberately.
4. **Minimize Suppressions**: Prefer targeted `per-file-ignores` or `noqa` annotations over broad global ignores.
5. **Protect Existing Workflows**: Keep Ruff aligned with Black, type checkers, notebooks, and existing automation where they remain in use.

## Local References (Load On-Demand)

Load only the references needed for the task.

* [Installation and Bootstrap](references/installation_and_bootstrap.md) - Choose how Ruff is installed and establish a safe first-run workflow.
* [Configuration Patterns](references/configuration_patterns.md) - Build or edit `pyproject.toml`, `ruff.toml`, or inherited Ruff configurations.
* [Configuration Presets](references/config_presets.md) - Compare the provided general, machine-learning, and data-science TOML templates, then load the matching asset.
* [Lint vs Format Workflows](references/lint_vs_format_workflows.md) - Decide when to lint, fix, format, or run check-only flows.
* [Rule Selection and Suppression](references/rule_selection_and_suppression.md) - Add rules gradually, manage ignores, and document exceptions.
* [Settings API Reference](references/settings.md) - Single-file complete Ruff settings reference covering top-level, analyze, format, lint core, and plugin-specific configuration.
* [Formatter-Linter Compatibility](references/compatibility.md) - Avoid conflicts between Ruff's formatter and selected lint rules.
* [Integrations: pre-commit and CI](references/integrations.md) - Wire Ruff into automation and editor-driven workflows.
* [Troubleshooting and Migration](references/migration.md) - Resolve common adoption failures and migration friction.

## Rule Discovery via Ruff CLI

Use Ruff itself as the primary source of truth for rule lookup.

* Get the complete rule documentation set: `ruff rule --all`
* List all rules by filtering Markdown H1 headings from the full output: `ruff rule --all | grep '^# '`
* Get the explanation for a specific rule: `ruff rule <code>`

Examples:

* `ruff rule F401`
* `ruff rule TID252`
* `ruff rule --all | grep '^# ' | head`

## Local Assets (Templates)

Load these when the user needs a copy-paste-ready starting point.

* [General Ruff Template](assets/pyproject.toml) - Baseline `pyproject.toml` preset.
* [Machine Learning Ruff Template](assets/pyproject.ai.toml) - Narrower ML-oriented preset.
* [Data Science Ruff Template](assets/pyproject.datascience.toml) - NumPy and pandas oriented preset.
* [GitHub Actions CI Template](assets/github_actions_ci.yml) - Direct CLI workflow for `ruff check`.
* [GitHub Actions ruff-action Template](assets/github_actions_ruff_action.yml) - Managed installation workflow.
* [GitLab CI Template](assets/gitlab-ci.yml) - `ruff check` plus `ruff format --diff` pipeline.
* [pre-commit Basic Template](assets/pre-commit-basic.yml) - Minimal `ruff check` hook setup.
* [pre-commit Fix Template](assets/pre-commit-fix.yml) - Auto-fix oriented pre-commit hook setup.
* [pre-commit No-Notebooks Template](assets/pre-commit-no-notebooks.yml) - pre-commit setup that excludes notebook processing.

## Workflow

### Step 1: Discover the Existing Toolchain

Before making changes, inspect:

* `pyproject.toml`
* `ruff.toml` or `.ruff.toml`
* `.pre-commit-config.yaml`
* CI workflow files
* nearby Python files for quote, import, and docstring patterns

Identify:

* whether Ruff is already installed
* whether Black, Flake8, isort, or Pylint are still active
* whether Ruff is used for linting, formatting, or both
* line length, target Python version, and rule-selection strategy

### Step 2: Route to the Right Reference

Choose references based on the user's goal:

* New Ruff adoption or install choice -> [Installation and Bootstrap](references/installation_and_bootstrap.md)
* Editing settings or choosing config layout -> [Configuration Patterns](references/configuration_patterns.md)
* Starting from a known config template -> [Configuration Presets](references/config_presets.md), then one of [General Ruff Template](assets/pyproject.toml), [Machine Learning Ruff Template](assets/pyproject.ai.toml), or [Data Science Ruff Template](assets/pyproject.datascience.toml)
* Defining local or CI commands -> [Lint vs Format Workflows](references/lint_vs_format_workflows.md)
* Adding rules or silencing false positives -> [Rule Selection and Suppression](references/rule_selection_and_suppression.md)
* Looking up exact settings semantics -> [Settings API Reference](references/settings.md)
* Looking up exact rule codes, rule names, or full rule documentation -> use `ruff rule --all`; if you only need the rule list, use `ruff rule --all | grep '^# '`; if you need one rule, use `ruff rule <code>`
* Mixing formatter and linter behavior -> [Formatter-Linter Compatibility](references/compatibility.md)
* Pre-commit or CI setup -> [Integrations: pre-commit and CI](references/integrations.md), then one of [pre-commit Basic Template](assets/pre-commit-basic.yml), [pre-commit Fix Template](assets/pre-commit-fix.yml), [pre-commit No-Notebooks Template](assets/pre-commit-no-notebooks.yml), [GitHub Actions CI Template](assets/github_actions_ci.yml), [GitHub Actions ruff-action Template](assets/github_actions_ruff_action.yml), or [GitLab CI Template](assets/gitlab-ci.yml)
* Adoption failures, noisy diffs, or migration questions -> [Troubleshooting and Migration](references/migration.md)

### Step 3: Plan Before Editing

When proposing a change, produce a concise plan that states:

1. which config file(s) will change
2. whether Ruff will lint, format, or both
3. which rule families will be enabled or adjusted
4. how existing hooks or CI jobs will be updated
5. how the change will be validated

### Step 4: Implement Conservatively

When writing or editing configuration:

* keep the rule set explicit
* keep suppressions local and documented by context
* prefer project-local installation for repository automation
* avoid enabling formatter-conflicting lint rules unless intentionally managed

### Step 5: Validate the Outcome

When possible, validate with commands appropriate to the task:

* `ruff check`
* `ruff check --fix`
* `ruff format --check`
* `ruff format`

In automation, ensure the chosen commands match the intended policy: fail-only, fix-before-format, or diff-only.

## Quick Decision Rules

1. If the repository already uses Black, decide explicitly whether Ruff formatter is replacing it or coexisting with it.
2. If the repository is new to linting, start near Ruff defaults before enabling broad rule families.
3. If rule churn is high, use incremental migration patterns instead of global strictness.
4. If a suppression is needed, use the narrowest mechanism that solves the problem.
5. If CI and local behavior differ, document why and keep the difference intentional.

## Response Template

When reporting Ruff guidance or changes, summarize in this order:

1. Current toolchain signals found in the repository.
2. Recommended Ruff role: lint only, format only, or both.
3. Proposed config or workflow changes.
4. Validation commands or automation updates.
5. Any migration risk, suppression rationale, or follow-up references.
