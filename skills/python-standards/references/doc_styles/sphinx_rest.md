# Sphinx / reStructuredText (reST) Style

## Philosophy
Prioritizes tooling and rich linking. The native format for Python's official documentation.

## Format Rules
* **Directives**: Uses `:field name:` syntax.
* **Types**: Can be separate (`:type param:`) or inline.
* **Formatting**: Supports bold, italics, and code blocks using reST syntax (`**bold**`, ``` ``code`` ```).

## Example
```python
def fetch_data(url, retries=3):
    """Fetches data from the API endpoint.

    :param url: The URL to fetch from.
    :type url: str
    :param retries: Number of times to retry on failure.
    :type retries: int
    :return: The parsed JSON response.
    :rtype: dict
    :raises ConnectionError: If the server is unreachable.
    """
    pass
```
