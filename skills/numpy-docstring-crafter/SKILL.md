---
name: numpy-docstring-crafter
description: Use this skill when you need to write or refactor Python docstrings according to the NumPy Docstring Standard (numpydoc). Trigger this even if the user just asks to 'document the code using numpy style', 'add numpy docstrings', or 'format comments for Sphinx using numpydoc'.
license: Apache-2.0
---

# NumPy Style Docstring Crafter

This skill provides expertise in writing Python documentation according to the [NumPy Docstring Standard](https://numpydoc.readthedocs.io/en/latest/format.html). This style is heavily used in the scientific Python ecosystem (NumPy, SciPy, pandas, scikit-learn) and relies on specific reStructuredText (reST) formatting, focusing on readability in text terminals.

## Core Principles

1.  **Readability First:** Human readers of text terminals are given precedence. Avoid contorting docstrings just to make Sphinx produce nice output. Keep line lengths to a maximum of 75 characters.
2.  **Specific Sections:** Information is divided into explicitly named, underlined sections (e.g., `Parameters`, `Returns`, `Examples`).
3.  **Strict Underlining:** Section headers must be underlined with hyphens (`-`) matching the exact length of the header name.
4.  **reST Syntax:** Utilizes basic reStructuredText syntax for formatting. Use single backticks (`` `name` ``) for parameter names and double backticks (`` ``monospaced`` ``) for inline code/literals.

## Audit Checklist

When reviewing or writing NumPy style docstrings, use this checklist:

- [ ] Is the docstring enclosed in triple double quotes `"""`?
- [ ] Is there a concise, one-line short summary?
- [ ] Are section headers (e.g., `Parameters`, `Returns`) correctly spelled and underlined with hyphens (`-`) of the *exact same length*?
- [ ] Are parameters listed as `name : type` with the colon preceded by a space?
- [ ] Do parameter and return value descriptions maintain a hanging indent of 4 spaces?
- [ ] Are parameter names referenced in the text enclosed in single backticks (`` `param` ``)?
- [ ] Are inline code snippets enclosed in double backticks (`` ``code`` ``)?
- [ ] Is the line length kept under 75 characters where possible?

## Simple Example

```python
def add(a, b):
    """
    The sum of two numbers.

    Parameters
    ----------
    a : int or float
        The first number to add.
    b : int or float
        The second number to add.

    Returns
    -------
    int or float
        The sum of `a` and `b`.
    """
    return a + b
```

## Detailed References

Refer to these guides for specific formatting rules:

- [Sections Overview](references/sections.md): The ordered list of all possible sections.
- [Functions & Methods](references/functions.md): Formatting for `Parameters`, `Returns`, `Yields`, etc.
- [Classes & Modules](references/classes_and_modules.md): Formatting for `Attributes`, `Methods`, and module summaries.
- [reST Formatting](references/rest_formatting.md): Rules for backticks, links, math, and notes.

## Templates

### Modules
- [Single Line Module](assets/module_single_line_template.py)
- [Private Module](assets/module_private_template.py)
- [Public Module](assets/module_public_template.py)

### Classes
- [Single Line Class](assets/class_single_line_template.py)
- [Private Class](assets/class_private_template.py)
- [Public Class](assets/class_public_template.py)

### Functions & Methods
- [Single Line Function](assets/function_single_line_template.py)
- [Private Function](assets/function_private_template.py)
- [Public Function](assets/function_public_template.py)
