## Python Project Layout (src-layout)

### Directory Structure

```
project_root/
├── pyproject.toml       # Project metadata and build configuration
├── README.md            # Project documentation
├── .gitignore           # Git ignore rules
├── src/                 # Source code root
│   └── my_package/      # Actual package directory
│       ├── __init__.py  # Package initialization
│       ├── module.py    # Business logic
│       └── sub_pkg/     # Sub-packages
├── tests/               # Test suite (parallel to src)
│   ├── __init__.py
│   └── test_module.py
├── scripts              # Utility scripts (optional)
└── docs/                # Documentation files
```

### Implementation Rules

1. **Code Isolation**: Place all application source code exclusively within the `src/` directory.
2. **Package Nesting**: Create a unique package directory (e.g., `my_package/`) inside `src/`.
3. **Import Mechanism**: Require editable installation (`pip install -e .`) during development to ensure the package is importable via the `src` path.
4. **Test Separation**: Keep the `tests/` directory at the project root, outside of the `src/` folder.
5. **Centralized Config**: Use `pyproject.toml` as the primary configuration file for build systems and tools (e.g., Ruff, Pytest, MyPy).
6. **No Logic in Root**: Do not place `.py` files in the `project_root/` except for essential configuration scripts.
