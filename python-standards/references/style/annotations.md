# Type Annotations (PEP 484 and PEP 526)

## Function Annotations (PEP 484)

### Basic Style Rules
* Use PEP 484 syntax for type hints
* Normal colon rules apply
* Always have spaces around the `->` arrow

```python
# Correct:
def munge(input: AnyStr) -> AnyStr: ...
def munge(sep: AnyStr = None) -> None: ...

# Wrong:
def munge(input:AnyStr)->AnyStr: ...
def munge(sep:AnyStr=None)->None: ...
```

### Type Hints with Default Values
When combining annotations with defaults, use spaces around `=`:

```python
# Correct:
def munge(sep: AnyStr = None) -> None: ...
def process(data: List[str], limit: int = 1000) -> Dict[str, Any]: ...

# Wrong:
def munge(sep: AnyStr=None) -> None: ...
def process(data: List[str], limit=1000) -> Dict[str, Any]: ...
```

Note: Unannotated parameters with defaults don't need spaces:
```python
def process(data: List[str], limit=1000): ...  # OK for backward compat
```

## Variable Annotations (PEP 526)

### Module, Class, and Instance Variables
* Single space after the colon
* No space before the colon
* One space on both sides of `=` when assigning

```python
# Correct:
code: int

class Point:
    coords: Tuple[int, int]
    label: str = '<unknown>'
    
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

# Wrong:
code:int  # No space after colon
code : int  # Space before colon

class Test:
    result: int=0  # No spaces around =
```

### Local Variables
Same rules apply:

```python
def calculate_total(items: List[Item]) -> int:
    total: int = 0
    count: int = len(items)
    return total
```

## Type Annotation Best Practices

### When to Use Type Hints
* **New code**: Use type hints from the start
* **Big refactorings**: Good time to add them
* **Standard library**: Conservative adoption

### Opting Out of Type Checking
For code that uses annotations differently, add this comment near the top:

```python
# type: ignore
```

For finer-grained control, see PEP 484.

### Type Checkers are Optional Tools
* Python interpreters don't enforce types by default
* Users who don't want type checkers can ignore them
* Type checkers (mypy, pyright, etc.) are separate tools

### Stub Files for Distribution
For library packages:
* Create `.pyi` stub files for type information
* Distribute them with the library or separately via typeshed
* Type checkers read `.pyi` files in preference to `.py` files

```python
# mymodule.pyi (stub file)
from typing import List, Optional

def process_data(items: List[str], flag: bool = False) -> Optional[str]: ...

class DataProcessor:
    def __init__(self, config: dict) -> None: ...
    def process(self) -> List[str]: ...
```

## Common Type Hint Patterns

### Optional Values
```python
from typing import Optional

def get_user(user_id: int) -> Optional[User]:
    """Return User or None if not found."""
    pass
```

### Union Types
```python
from typing import Union

def process(data: Union[str, bytes]) -> str:
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data
```

### Collection Types
```python
from typing import List, Dict, Set, Tuple

def process_names(names: List[str]) -> Dict[str, int]:
    return {name: len(name) for name in names}

def get_coords() -> Tuple[int, int]:
    return (0, 0)

def unique_items(items: List[str]) -> Set[str]:
    return set(items)
```

### Callable Types
```python
from typing import Callable

def apply_operation(func: Callable[[int, int], int], x: int, y: int) -> int:
    return func(x, y)
```

### Generic Types
```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()
```

### Any Type (Escape Hatch)
```python
from typing import Any

def process_unknown(data: Any) -> Any:
    """Process data of unknown type."""
    return data
```

## Gradual Typing

### Start Simple
You don't need to annotate everything at once:

```python
# Start with public API
def public_function(x: int) -> str:
    result = _internal_helper(x)  # No annotations yet
    return str(result)

def _internal_helper(x):  # Add annotations later
    return x * 2
```

### Progressive Enhancement
1. Annotate function signatures first
2. Add variable annotations where clarity helps
3. Use `Any` temporarily for complex types
4. Refine to precise types over time

## Type Checking Tools

### Popular Type Checkers
* **mypy**: The original, most mature
* **pyright**: Fast, integrated with VS Code (Pylance)
* **pyre**: Facebook's type checker
* **pytype**: Google's type checker with inference

### Running Type Checkers
```bash
# mypy
mypy mypackage/

# pyright
pyright mypackage/

# With specific Python version
mypy --python-version 3.9 mypackage/
```

### Configuration
Use `pyproject.toml` or dedicated config files:

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

## Python Version Compatibility

### Annotations in Python 3.7+
Use from `__future__` import for forward references:

```python
from __future__ import annotations

class Node:
    def add_child(self, child: Node) -> None:  # Can reference Node before it's defined
        pass
```

### Supporting Older Python Versions
Use string literals for forward references:

```python
class Node:
    def add_child(self, child: 'Node') -> None:
        pass
```

Or use stub files (`.pyi`) for all versions.
