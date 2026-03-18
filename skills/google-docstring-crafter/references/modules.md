# Module Docstrings

Start every file with a docstring describing its contents and usage.

### Formatting Rules

1.  **Summarize:** Begin with a one-line summary terminated by a period.
2.  **Separate:** Leave a blank line after the summary if more description is needed.
3.  **Elaborate:** Provide an overall description, and optionally include lists of exported classes/functions and usage examples.

### Example

```python
"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.

Typical usage example:

  foo = ClassFoo()
  bar = foo.function_bar()
"""
```

### Test Modules

Do not include module-level docstrings for test files unless they provide unique information (e.g., how to run a specific test, unusual setup patterns, or external dependencies).

- **Omit** docstrings like `"""Tests for foo.bar."""`.
- **Include** docstrings explaining complex setup or environment requirements.

### Why

Module docstrings provide high-level context that helps developers understand the purpose of a file without reading the entire code. They are also extracted by `pydoc` to generate documentation summaries.
