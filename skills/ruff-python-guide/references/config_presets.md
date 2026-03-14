# Ruff Configuration Presets

This file explains when to choose each configuration preset.

The copy-paste-ready templates themselves live in `assets/` so they can be used directly without extracting code blocks from a reference document.

Template assets:

* `assets/pyproject.toml`
* `assets/pyproject.ai.toml`
* `assets/pyproject.datascience.toml`

## General Project

Best for standard Python applications and libraries that want a broad lint profile with modernization, import hygiene, and Ruff-specific checks.

Template: `assets/pyproject.toml`

## Machine Learning Project

Best for model training or experimentation repositories that want practical correctness and import hygiene without the full Pylint-style breadth.

Template: `assets/pyproject.ai.toml`

## Data Science Project

Best for notebooks, NumPy, and pandas heavy projects that need array/dataframe-aware linting.

Template: `assets/pyproject.datascience.toml`

## Selection Guide

* Choose the general template for libraries and services with a broader static-analysis posture.
* Choose the machine-learning template when experimentation speed matters more than broad Pylint-style coverage.
* Choose the data-science template when NumPy and pandas specific linting should be first-class.
