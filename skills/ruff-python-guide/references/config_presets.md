# Ruff Configuration Presets

This file explains when to choose each configuration preset.

The copy-paste-ready templates themselves live in `assets/` so they can be used directly without extracting code blocks from a reference document.

Template assets:

* `assets/pyproject.toml`
* `assets/pyproject.strict.toml`
* `assets/pyproject.ai.toml`
* `assets/pyproject.datascience.toml`

## General Project

Best for standard Python applications and libraries that want a small, guidance-aligned extension over Ruff defaults.

Template: `assets/pyproject.toml`

## Strict Project

Best when the repository wants the previous broader lint policy with additional rule families, per-file ignores, and stricter operational defaults.

Template: `assets/pyproject.strict.toml`

## Machine Learning Project

Best for model training or experimentation repositories that want practical correctness and import hygiene without the full Pylint-style breadth.

Template: `assets/pyproject.ai.toml`

## Data Science Project

Best for notebooks, NumPy, and pandas heavy projects that need array/dataframe-aware linting.

Template: `assets/pyproject.datascience.toml`

## Selection Guide

* Choose the general template for a simpler baseline that extends Ruff defaults conservatively.
* Choose the strict template when broader lint coverage and explicit exceptions are intentional.
* Choose the machine-learning template when experimentation speed matters more than broad Pylint-style coverage.
* Choose the data-science template when NumPy and pandas specific linting should be first-class.
