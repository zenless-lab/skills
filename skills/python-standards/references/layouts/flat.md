## Python Project Layout (flat-layout)

### Directory Structure

```
project_root/
├── pyproject.toml       # Project metadata
├── README.md
├── .gitignore
├── my_package/          # Source code directly in root
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
├── tests/               # Test code
│   └── test_core.py
└── scripts/             # Utility scripts (optional)
    └── run_job.py

```

### Implementation Rules

1. **Direct Access**: Place the package directory (`my_package/`) directly under the `project_root/`.
2. **Path Resolution**: Enable the Python interpreter to recognize the package in the current working directory without requiring an editable install.
3. **Namespace Integrity**: Ensure the top-level package name does not conflict with Python standard library modules or common third-party dependencies.
4. **Test Referencing**: Import the package within the `tests/` directory using standard absolute imports based on the root environment.
5. **Deployment Fit**: Use for standalone scripts, simple microservices, or Docker-based deployments where `src/` isolation is not required.
