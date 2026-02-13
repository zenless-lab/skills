# Google Docstring Style

**Official Reference**: https://google.github.io/styleguide/pyguide.html

## Philosophy
Prioritizes human readability. Uses indentation and headers rather than excessive punctuation.

## Format Rules
* **Summary**: Imperative mood ("Fetch the user", not "Fetches the user").
* **Sections**: `Args:`, `Returns:`, `Raises:`, `Yields:`, `Examples:`.
* **Type Hinting**: Prefer PEP 484 type hints in the signature (`func(a: int)`), but types can be included in docs if necessary.

## Example
```python
def fetch_data(url: str, retries: int = 3) -> dict:
    """Fetches data from the API endpoint.

    Args:
        url: The URL to fetch from.
        retries: Number of times to retry on failure.

    Returns:
        A dictionary containing the parsed JSON response.

    Raises:
        ConnectionError: If the server is unreachable.
    """
    pass
```
