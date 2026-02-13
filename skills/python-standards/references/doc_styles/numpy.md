# NumPy / SciPy Docstring Style

**Official Reference**: https://numpydoc.readthedocs.io/en/latest/format.html

## Philosophy
Verbose and highly structured. Optimized for complex scientific functions with mathematical descriptions and array dimensions.

## Format Rules
* **Headers**: Underlined with dashes `-----`.
* **Type Spec**: Placed on the same line as the parameter name, often with optional shape info.

## Example
```python
def dot_product(a, b):
    """
    Calculate the dot product of two arrays.

    Parameters
    ----------
    a : array_like
        First input array.
    b : array_like
        Second input array.

    Returns
    -------
    output : float
        The dot product of a and b.
    """
    pass
```
