# Classes & Modules Formatting

## Classes

Classes use similar sections as functions, with the addition of `Attributes` and optionally `Methods`. The constructor (`__init__`) can be documented within the class docstring (using a `Parameters` section) or on the `__init__` method itself.

### Attributes

Located below the `Parameters` section (if describing the constructor), the `Attributes` section describes non-method attributes.

```python
Attributes
----------
x : float
    Description of attribute `x`.
y : float
    Description of attribute `y`.
```

Attributes that are properties and have their own docstrings can be simply listed by name.

### Methods

In general, it is not necessary to list class methods. However, if a class has many methods and only a few are relevant, a `Methods` section can be useful.

```python
Methods
-------
colorspace(c='rgb')
    Represent the photo in the given colorspace.
gamma(n=1.0)
    Change the photo's gamma exposure.
```

**Note:** Do not include `self` in the list of parameters for methods. Do not list private methods (starting with `_`) in the `Methods` section.

## Modules

Each module should have a docstring with at least a summary line. Routine listings are encouraged for large modules to provide a good overview of functionality.

```python
"""
Short summary of the module.

Extended summary...

Routine Listings
----------------
func_a
    Description of func_a.
class_b
    Description of class_b.
"""
```

### Why
Documenting class attributes provides a clear picture of the state an object holds, which is essential for object-oriented design. Module docstrings act as the front page for a package, guiding users to the most important exports.
