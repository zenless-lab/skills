# NumPy Docstring Reference (numpydoc)

## 1. General Principles

* **Syntax:** Use ReStructuredText (reST) syntax.
* **Quotes:** Always surround docstrings with triple double quotes `"""`.
* **Line Length:** Keep lines to a maximum of 75 characters for terminal readability.

## 2. Structure & Sections

Sections are separated by headings underlined with hyphens. Use the following order:

### 2.1 Summary & Description

* **Short Summary:** A one-line summary of the function's purpose. Do not use variable names or the function name itself.
* **Extended Summary:** Provides a detailed description of functionality. Avoid implementation details (use the **Notes** section for that).

### 2.2 Parameters

* **Format:** `name : type` followed by an indented description.
* **Type Details:** Be precise (e.g., `int`, `str`, `array_like`).
* **Optional:** Use `optional` for keyword arguments with defaults: `x : int, optional`.
* **Choices:** List fixed values in braces: `order : {'C', 'F', 'A'}`.

```python
Parameters
----------
x : int
    Description of parameter `x`.
y : float, optional
    Description of `y` (default is 1.0).

```

### 2.3 Returns & Yields

* **Return Values:** Similar to Parameters, but the name is optional while the type is required.
* **Generators:** Use `Yields` instead of `Returns` for generator functions.

```python
Returns
-------
int
    Description of the return value.
err_code : int
    Description of a named return value.

```

### 2.4 Raises & See Also

* **Raises:** Detail non-obvious errors that might be raised.
* **See Also:** Refer to related routines. Use `name : description` or just a list of function names.

### 2.5 Notes & References

* **Notes:** Use for theoretical background or mathematical algorithms.
* **Math:** Use LaTeX format with the `.. math::` directive or inline `:math:`.
* **References:** List cited works using numbered markers like `[1]_`.

### 2.6 Examples

* **Format:** Use doctest style starting with `>>>`. Separated from text and other examples by blank lines.
* **Context:** Assume `import numpy as np` has been executed.

```python
Examples
--------
>>> np.add(1, 2)
3

```

## 3. Class Documentation

* **Main Docstring:** Document the class and its constructor (`__init__`) parameters in the **Parameters** section.
* **Attributes:** Use an **Attributes** section below Parameters to describe non-method attributes: `name : type`.
* **Methods:** List relevant public methods only if the class has many complex routines.
* **Self:** Never list `self` as a parameter in any method docstring.

## 4. Formatting Conventions

* **Variables:** Enclose parameter, attribute, and method names in single backticks ``var``.
* **Code Blocks:** Use double backticks ```code``` for monospaced text.
* **Bold/Italics:** Use `**bold**` and `*italics*` for emphasis.
* **Lists:** Use standard reST bulleted or numbered lists.
