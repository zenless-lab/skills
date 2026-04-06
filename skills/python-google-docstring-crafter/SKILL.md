---
name: python-google-docstring-crafter
description: Use this skill when you need to write or refactor Python docstrings and comments according to the Google Python Style Guide. Trigger this even if the user just asks to 'document the code', 'add comments', or 'fix docstrings' in a Python project.
license: Apache-2.0
---

# Google Style Python Docstring

This skill provides expertise in writing Python documentation and comments according to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). Proper documentation ensures code is understandable by both humans and automated tools like `pydoc` and `pytype`.

## Core Instructions

1. **Prioritize Intent Over Mechanics:** Focus on *why* a function or class exists and how it should be used. Avoid mechanically repeating the code's logic.
2. **Standard Format:** Use the three-double-quote `"""` format for all docstrings.
3. **Structured Sections:** Use explicit sections for `Args:`, `Returns:`, and `Raises:` to maintain a consistent structure across the project.
4. **Consistency is Key:** Whether you choose imperative or descriptive style, ensure it's consistent within each file.

## Audit Checklist

When reviewing or writing documentation, use the following checklist:

- [ ] Does every module, class, and public function have a docstring?
- [ ] Does the first line consist of a concise, one-line summary terminated by a period?
- [ ] Is there a blank line after the summary if the description continues?
- [ ] Are all parameters listed in the `Args:` section with correct indentation?
- [ ] Is the return value documented in `Returns:` (or `Yields:` for generators)?
- [ ] Are all relevant exceptions listed in the `Raises:` section?
- [ ] For classes, is there an `Attributes:` section for public attributes?
- [ ] Are inline comments positioned at least 2 spaces from the code and descriptive of the *intent*?

## Simple Example

```python
def fetch_data(url: str, timeout: int = 10) -> dict:
    """Fetches data from the given URL.

    Detailed explanation of fetching logic, including timeout behavior.

    Args:
        url: The URL to fetch data from.
        timeout: The maximum time in seconds to wait for a response.

    Returns:
        A dictionary containing the JSON response.

    Raises:
        ConnectionError: If the network request fails.

    Examples:
        >>> fetch_data("https://google.com")
        {'status': 'ok'}
    """
    pass
```

## Detailed References

Refer to these guides for specific formatting rules:

- [Module Docstrings](references/modules.md): Formatting for file headers and test modules.
- [Function & Method Docstrings](references/functions.md): Formatting for `Args`, `Returns`, and `Raises`.
- [Class Docstrings](references/classes.md): Formatting for class summaries and `Attributes`.
- [Block & Inline Comments](references/comments.md): Rules for readability and content.

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
