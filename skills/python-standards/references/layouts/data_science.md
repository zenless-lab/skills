## Data Science Project Layout

### Directory Structure

```
project_root/
├── README.md            # Project overview and reproduction guide
├── pyproject.toml       # Dependency and tool configuration
├── .gitignore           # Git ignore rules
├── data/                # Data storage (git-ignored)
│   ├── raw/             # Original, immutable data dump
│   ├── interim/         # Intermediate transformed data
│   ├── processed/       # Final, canonical data sets for modeling
│   └── external/        # Data from third party sources
├── notebooks/           # Jupyter notebooks
│   ├── 1.0-jdoe-eda.ipynb  # Format: <number>-<author>-<description>
│   └── template.ipynb
├── src/                 # Source code for the project
│   └── __init__.py      # Makes src a Python module
├── models/              # Trained and serialized models, model predictions, or model summaries (optional)
├── references/          # Data dictionaries, manuals, and all other explanatory materials (optional)
├── reports/             # Generated analysis as HTML, PDF, etc. (optional)
│   └── figures/         # Generated graphics and figures to be used in reporting
└── environment.yml      # Conda environment file (optional)

```

### Implementation Rules

1. **Data Immutability**: Treat `data/raw/` as read-only. All transformations must output to `interim/` or `processed/`.
2. **Notebook Refactoring**: Use notebooks for exploration only. Refactor production-ready logic into the `src/` directory for modularity and testing.
3. **Path Independence**: Use project-relative paths (via `pyprojroot` or similar) to ensure code runs across different environments without hardcoded strings.
4. **Version Control Hygiene**: Exclude the contents of `data/` and `models/` from Git via `.gitignore`. Commit only the code, configuration, and documentation.
