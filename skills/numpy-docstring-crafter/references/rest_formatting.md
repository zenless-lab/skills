# reST Formatting in NumPy Docstrings

NumPy docstrings use a subset of reStructuredText (reST) designed to be readable in text terminals while still allowing rich rendering via Sphinx.

## Backticks

Use of backticks is a common point of confusion because it differs from Markdown.

- **Single Backticks (`` `name` ``):** Use for variable names, parameter names, and object names (modules, classes, functions, attributes). Depending on project settings, these may automatically render as hyperlinks (e.g., `` `numpy` `` -> :any:`numpy`).
- **Double Backticks (`` ``code`` ``):** Use for inline code snippets, mathematical literals, or anything that must render in a `monospaced` font but *should not* be a hyperlink.

## Equations

Mathematical equations can be included but should be used sparingly, as LaTeX is hard to read in plain text.

```python
Notes
-----
The FFT is a fast implementation of the discrete Fourier transform:

.. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

The value of :math:`\omega` is larger than 5.
```

Often, it is better to show equations as Python pseudo-code using double backticks (`` ``y = np.sin(x)`` ``).

## Links

If you need to include hyperlinks, use the inline hyperlink form to avoid confusing the numpydoc parser:

```rst
`Example <http://www.example.com>`_
```

Do not use the detached target form (`.. _Example: http://www.example.com`).

## Examples Section

The `Examples` section uses the `doctest` format. It is meant to illustrate usage, not to replace the testing framework.

```python
Examples
--------
>>> np.add(1, 2)
3

Comment explaining the second example.

>>> np.add([1, 2], [3, 4])
array([4, 6])
```

- Separate multiple examples with blank lines.
- Split code across multiple lines using `... `.

### Why
Using a constrained subset of reST ensures that the docstring remains lightweight and perfectly legible when a user types `help(function)` in a Python REPL.
