# Functions & Methods Formatting

This reference details how to format the core parameter and return sections for functions and methods in the NumPy style.

## Parameters

List the parameters, their expected types, and a description.

```python
Parameters
----------
x : type
    Description of parameter `x`.
y
    Description of parameter `y` (with type not specified).
copy : bool, optional
    Optional parameters can be marked.
order : {'C', 'F', 'A'}, default: 'C'
    When a parameter assumes a fixed set of values.
*args
    Additional arguments should be passed as keyword arguments.
```

- **Colon Formatting:** The colon `:` must be preceded by a space, or omitted if the type is absent.
- **Indentation:** The description must be indented by exactly 4 spaces.
- **Combining:** When two or more parameters have the exact same type and description, they can be combined (e.g., `x1, x2 : array_like`).
- **References:** Enclose parameter names within the docstring in single backticks (`` `param` ``).

## Returns & Yields

Explanation of the returned (or yielded) values and their types. Similar to `Parameters`, except the name of each return value is optional.

```python
Returns
-------
int
    Description of anonymous integer return value.
err_code : int
    Non-zero value indicates error code, or zero on success.
```

- **Generators:** Use `Yields` instead of `Returns` for generators.
- **Multiple Values:** If multiple values are returned, list them sequentially.

## Raises & Warns

Detail which errors or warnings get raised and under what conditions.

```python
Raises
------
LinAlgException
    If the matrix is not numerically invertible.
```

### Why
Standardizing the structure of parameters and return values allows Sphinx and IDEs to automatically parse and render rich tooltips, while keeping the source code perfectly legible.
