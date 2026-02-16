# Python Code Style Guide

## 1. Core Philosophy

* **Existing Code First**: When maintaining existing code, staying consistent with the surrounding style is often more important than strictly following this guide.
* **Readability Above All**: The primary goal of style guidelines is to improve code readability.
* **Break Rules When Necessary**: Consistency is important, but if following a rule results in less readable code, you should break it.

## 2. Code Layout

* **Indentation**: Use **4 spaces** per indentation level; never use tabs.
* **Line Length**: Limit all code lines to a maximum of **79 characters** (PEP 8 standard) and docstrings/comments to **72 characters**.
    * **Exceptions**: Long import statements, URLs/paths in comments, and Pylint disable comments are allowed to exceed this limit.
* **Line Continuation**: Prefer implicit line joining inside parentheses, brackets, and braces over using backslashes (`\`).
* **Blank Lines**: Separate top-level function and class definitions with **two blank lines**; use **one blank line** between method definitions inside a class.
* **Source File Encoding**: Files must use **UTF-8** encoding.
* **Statements**: Generally, only one statement is allowed per line; never put `try/except` on the same line as code.

## 3. Imports

* **Grouping and Order**: Group imports in the following order, separated by a blank line:
    1. `__future__` import statements.
    2. Python standard library imports.
    3. Third-party module or package imports.
    4. Local application/sub-package imports.
* **Formatting**: Each import should be on its own line (e.g., `import os` and `import sys` on separate lines).
* **Paths**: Use the full package path for all imports; do not use implicit relative imports.

## 4. Whitespace

* **Avoid Whitespace**:
    * Immediately inside parentheses, brackets, or braces.
    * Before commas, semicolons, or colons.
    * Before the open parenthesis that starts an argument list, indexing, or slicing.
* **Use Whitespace**: Surround binary operators (assignment, comparisons, Booleans) with a single space on either side.
* **Argument Defaults**: Do not use spaces around the `=` sign for default parameter values or keyword arguments.
    * **Exception**: Use spaces around the `=` if a **type annotation** is present (e.g., `def func(i: int = 0):`).

## 5. Naming Conventions

* **General**: Names should be descriptive and avoid ambiguous abbreviations.
* **Packages and Modules**: Use `lower_with_under`; do not use dashes.
* **Classes and Exceptions**: Use `CapWords`; exception names must end with `Error`.
* **Functions, Methods, and Variables**: Use `lower_with_under`.
* **Constants**: Use `CAPS_WITH_UNDER`.
* **Internal Members**: Use a leading underscore (e.g., `_protected_member`) for internal module variables or protected class members.

## 6. Programming Practices

* **Conditionals**: Use the fact that empty sequences are false (`if not seq:`); do not compare Booleans to `True` or `False`.
* **Singleton Comparisons**: Use `is` or `is not` when comparing to singletons like `None`.
* **Exception Handling**:
    * Capture specific exceptions (e.g., `except ValueError:`) and avoid catch-all `except:` statements.
    * Minimize the amount of code within `try/except` blocks.
* **Resource Management**: Always use the `with` statement to explicitly close files, sockets, and other stateful resources.
* **Strings**: Do not use `+` or `+=` to accumulate strings in a loop; use `.join()` with a list instead.
* **Logging**: For logging functions, always use a **string literal** with pattern-parameters as subsequent arguments rather than an f-string.
* **Functions**: Keep functions small and focused; consider refactoring if a function exceeds approximately 40 lines.

## 7. Comments and Special Tags

* **Formatting**: Inline comments should be separated from code by at least **2 spaces** and start with `#` followed by **1 space**.
* **Special Tags**:
    * **TODO**: For functionality that needs to be added or modified later.
    * **FIXME**: For code that has a known bug and requires a fix.
    * **HACK**: For suboptimal code that works but requires refactoring.
    * **XXX**: For dangerous code or logic that is unclear despite working.
    * **NOTE**: To document the background or specific reasoning behind an implementation decision.

## 8. Type Annotations

* **Public APIs**: Strongly encouraged to annotate public APIs to improve readability and safety.
* **Self/Cls**: It is generally unnecessary to annotate `self` or `cls`.
* **Formatting**:
    * Use explicit `X | None` for optional types.
    * For long signatures, put one parameter per line and align the closing parenthesis with the `def` keyword.
* **Circular Dependencies**: Use `if TYPE_CHECKING:` blocks and string references to handle types that would otherwise cause circular imports.

## 9. Modern Features

* **Main Block**: Every executable file should contain an `if __name__ == '__main__':` block to prevent execution during imports.
* **Future Annotations**: Use `from __future__ import annotations` to enable forward references within type hints.
