# Cookiecutter Data Science Layout

## Overview
Designed for reproducibility and the "Data Acyclic Graph" (DAG) workflow. It clearly separates raw data (immutable) from processed data and analysis logic.

## Directory Tree
```text
project_root/
├── data/
│   ├── raw/              # Original, immutable data dump
│   ├── interim/          # Transformed data
│   └── processed/        # Final sets for modeling
├── notebooks/            # Jupyter Notebooks
│   ├── 1.0-exploratory.ipynb
│   └── 2.0-modeling.ipynb
├── src/                  # Reusable Python code (not scripts)
│   ├── __init__.py
│   ├── data/             # Scripts to generate data
│   ├── features/         # Feature engineering code
│   └── models/           # Training code
├── models/               # Serialized models (.pkl, .h5)
└── reports/              # Generated HTML/PDF analysis
```

## Key Rules

1. **Never edit `data/raw` manually.**
2. Move complex logic out of Notebooks and into `src/` functions to make them testable.
