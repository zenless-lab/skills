# Scripting Best Practices

The `scripts/` directory houses executable code (Python, Bash, Node.js). To ensure seamless agent execution, adhere to the following standards.

## Core Principles

1. **Self-contained**: Scripts must run independently, minimizing reliance on undeclared external environments.
2. **Robust Error Handling**: Handle edge cases gracefully. If an error occurs, output structured, helpful error messages (preferably to stderr) so the Agent can read the context and self-correct.
3. **Relative Pathing**: When reading/writing resources within the skill (e.g., templates in `assets/`), scripts must assume the execution path and safely construct relative paths to the target.

## Python Mandatory Standard: PEP 723

To enable seamless execution and dependency management, ALL Python scripts **MUST** utilize the PEP 723 inline script metadata standard. This allows the agent to use `uvx script.py` to automatically resolve dependencies and run the file.

The top of every Python script must contain a metadata block similar to this:

```python
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "requests",
#     "pandas",
#     "pdfplumber"
# ]
# ///

import requests
import pandas
# ... script body ...
```

## Execution Interaction

* **Non-blocking**: Scripts must NOT contain interactive blocking logic requesting human terminal input (e.g., `input()`), unless explicitly passed via command-line arguments.
* **Clear Exit Codes**: Return `0` on success and non-zero on failure to assist the Agent in determining the execution state.
