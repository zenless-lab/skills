# Pytest Framework Patterns

## Core Philosophy
Write tests as simple functions. Use `assert` statements. No boilerplate classes required.

## Key Concepts
* **Discovery**: Files must start with `test_` or end with `_test.py`.
* **Fixtures**: Use `@pytest.fixture` in `conftest.py` for setup/teardown logic.
* **Parametrization**: Use `@pytest.mark.parametrize` to run one test with multiple inputs.

## Structure Example
```python
# tests/test_math.py
import pytest
from my_app import add

@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (0, 0, 0)])
def test_add(a, b, expected):
    assert add(a, b) == expected

def test_raises_error():
    with pytest.raises(ValueError):
        add("a", 1)
```
