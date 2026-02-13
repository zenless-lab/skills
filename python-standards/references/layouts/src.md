# The "Src" Layout (Production Standard)

## Overview
This layout forces the code to be installed to run tests, preventing "import works on my machine but fails in production" errors. It is the gold standard for modern Python packaging.

## Directory Tree
```text
project_root/
├── src/
│   └── my_package/       # Actual code lives here
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/                # Tests live OUTSIDE the package
│   ├── __init__.py
│   └── test_core.py
├── pyproject.toml        # Build configuration
├── tox.ini               # Test runner config
└── README.md
```

## Import Mechanics

* Code in `tests/` cannot simply `import my_package` via relative path.
* You must install the package in editable mode (`pip install -e .`) to run tests.
* **Benefit**: Guarantees that you are testing the code that will actually be built and distributed.
