# PEP 8 Core Standards (Quick Reference)

This is a quick reference summary of the most commonly used PEP 8 rules. For detailed information on specific topics, see the specialized reference files linked throughout this document.

## Layout & Whitespace
* **Indentation**: Strictly **4 spaces**. No tabs.
* **Line Length**: Max **79 chars** (code), **72 chars** (comments/docstrings).
    * *Modern Exception*: 88 chars (Black formatter default) or 100/120 is acceptable if configured in `pyproject.toml`.
* **Blank Lines**:
    * Top-level functions/classes: **2 blank lines** surrounding.
    * Methods inside classes: **1 blank line** surrounding.

**→ For detailed whitespace rules (operators, expressions, statements, trailing commas):**  
See [whitespace guide](references/style/whitespace.md)

## Import Organization
* **Order**:
    1.  Standard Library (`os`, `sys`)
    2.  Third Party (`numpy`, `requests`)
    3.  Local Application (`from . import models`)
* **Location**: Top of file, after module docstring
* **Style**: Separate lines preferred

**→ For complete import conventions (absolute vs relative, grouping, wildcards, module dunders):**  
See [import guide](references/style/imports.md)

## Naming Conventions
| Type | Convention | Example |
| :--- | :--- | :--- |
| **Function/Variable** | `snake_case` | `calculate_total`, `user_id` |
| **Class** | `CapWords` (PascalCase) | `DataProcessor`, `UserAccount` |
| **Constant** | `ALL_CAPS` | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| **Protected Member** | `_leading_underscore` | `_internal_cache` |
| **Private Member** | `__double_underscore` | `__mangle_this` |

**→ For complete naming rules (all styles, special forms, prescriptive conventions, inheritance design):**  
See [naming guide](references/style/naming.md)

## Comments and Docstrings
* **Block comments**: Same indentation as code, `# ` prefix
* **Inline comments**: At least 2 spaces from statement
* **Docstrings**: Use `"""triple double quotes"""`
* **Docstring placement**: Closing `"""` on separate line for multi-line

**→ For complete comment conventions (when to use, formatting, docstring vs comments):**  
See [comment guide](references/style/comments.md)

## Programming Recommendations
* Use `is` for `None` checks: `if x is not None:` (not `if x != None:`).
* Use `"".startswith()` and `"".endswith()` instead of string slicing.
* Context Managers: Always use `with open(...)` for file handling.
* Use `isinstance()` for type checks, not `type()` comparisons.
* Don't compare boolean values to `True` or `False` using `==`.

**→ For complete programming recommendations (comparisons, exceptions, returns, lambda, etc.):**  
See [programming recommendations](references/style/programming_recommendations.md)

## Type Annotations
* Space after colon in variable annotations: `x: int = 5`
* Spaces around `->` in function annotations: `def func() -> int:`
* Spaces around `=` when combining annotation with default: `def func(x: int = 0):`

**→ For complete type annotation guidelines (PEP 484, PEP 526, stub files, tools):**  
See [annotations guidelines](references/style/annotations.md)

---

## When to Load Additional References

* **Uncertain about whitespace around operators?** → Load [whitespace](references/style/whitespace.md)
* **Need detailed naming rules (underscore forms, inheritance)?** → Load [naming](references/style/naming.md)
* **Import organization questions?** → Load [imports](references/style/imports.md)
* **Comment or docstring formatting?** → Load [comments](references/style/comments.md)
* **Best practices for exceptions, comparisons, returns?** → Load [programming_recommendations](references/style/programming_recommendations.md)
* **Type hints and annotations?** → Load [annotations](references/style/annotations.md)
