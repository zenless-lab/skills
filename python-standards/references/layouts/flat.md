# The "Flat" Layout (Pragmatic/Script)

## Overview
The package directory resides directly in the project root. It is simpler for beginners, scripts, and internal tools where distribution to PyPI is not the primary goal.

## Directory Tree
```text
project_root/
├── my_package/           # Code lives in root
│   ├── __init__.py
│   └── main.py
├── tests/                # Tests alongside package
│   └── test_main.py
├── requirements.txt      # Dependencies
└── main.py               # Entry point script
```

## Pros & Cons

* **Pros**: Zero configuration. `python main.py` works immediately without `pip install`.
* **Cons**: Easy to accidentally import files that won't be included in the final package distribution.
