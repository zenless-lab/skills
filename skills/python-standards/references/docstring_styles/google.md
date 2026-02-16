# Google Python Docstring Reference

## 1. General Principles

* **Format**: Always use triple double-quotes `"""` for docstrings.
* **Summary Line**: Provide a single-line summary (max 80 characters) ending with a period, question mark, or exclamation point.
* **Spacing**: Insert one blank line after the summary line before adding more detail.
* **Indentation**: Detailed descriptions must be indented to align with the opening quote.

## 2. Module-Level Docstrings

* **Placement**: Position at the top of the file, following the license boilerplate.
* **Contents**: Describe the module’s purpose, exported classes/functions, and provide typical usage examples.
* **Test Modules**: Docstrings are not required for tests unless they involve unusual setup or external dependencies.

## 3. Functions and Methods

* **Mandatory**: Required for public APIs, functions of non-trivial size, or non-obvious logic.
* **Style**: Use either descriptive style (`"""Fetches rows..."""`) or imperative style (`"""Fetch rows..."""`), but maintain consistency within the file.
* **Args Section**: List parameters by name, followed by a colon and description. Include types only if type annotations are missing.
* **Returns Section**: (Use **Yields:** for generators) Describe return value semantics. This may be omitted if the function returns `None`.
* **Raises Section**: List exceptions relevant to the interface and their trigger conditions.
* **Overriding**: Methods decorated with `@override` do not require a docstring unless the contract is significantly refined.

### Function Example

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table row.

    Returns:
        A dict mapping keys to the corresponding table row data.

    Raises:
        IOError: An error occurred accessing the smalltable.
    """

```

## 4. Classes

* **Summary**: The first line should describe what the class instance represents.
* **Attributes Section**: Document public attributes here (excluding properties) using the same formatting as `Args`.
* **Initialization**: Document constructor parameters within the `__init__` method docstring.

## 5. Specific Formatting & Scenarios

* **Properties**: Use noun-phrase descriptions (e.g., `"""The Bigtable path."""`) rather than verb phrases.
* **TODO Comments**: Use the format `# TODO: bug_link - explanation` (e.g., `# TODO: crbug.com/123 - fix this`).
