# Naming Conventions

## Overriding Principle
Names visible to users as public API should reflect **usage** rather than **implementation**.

## Common Naming Styles

| Style | Description | Example |
|:------|:------------|:--------|
| `b` | Single lowercase letter | `x`, `i` |
| `B` | Single uppercase letter | `T`, `N` |
| `lowercase` | All lowercase | `module`, `function` |
| `lower_case_with_underscores` | Snake case | `user_name`, `calculate_total` |
| `UPPERCASE` | All uppercase | `PI`, `MAX` |
| `UPPER_CASE_WITH_UNDERSCORES` | Uppercase snake case | `MAX_OVERFLOW`, `DEFAULT_TIMEOUT` |
| `CapitalizedWords` | PascalCase/CapWords | `DataProcessor`, `UserAccount` |
| `mixedCase` | camelCase (not Pythonic) | `firstName` (avoid) |
| `Capitalized_Words_With_Underscores` | Ugly - avoid! | `Very_Bad_Style` |

**Note on Acronyms in CapWords**: Capitalize all letters. Use `HTTPServerError`, not `HttpServerError`.

## Special Forms with Underscores

### Single Leading Underscore: `_name`
"Internal use" indicator. Not imported by `from module import *`.

```python
class MyClass:
    def _internal_method(self):
        """Not part of public API."""
        pass
```

### Single Trailing Underscore: `name_`
Avoid conflicts with Python keywords:

```python
tkinter.Toplevel(master, class_='ClassName')  # 'class' is a keyword
```

### Double Leading Underscore: `__name`
Triggers name mangling in classes. `__foo` in class `FooBar` becomes `_FooBar__foo`:

```python
class FooBar:
    def __init__(self):
        self.__private = 42  # Becomes _FooBar__private
```

### Double Leading and Trailing: `__name__`
"Magic" objects in user-controlled namespaces. **Never invent these** - only use documented ones like `__init__`, `__import__`, `__file__`.

## Prescriptive Conventions

### Names to Avoid
**Never** use these as single-character variable names:
* `l` (lowercase L) - looks like `1`
* `O` (uppercase O) - looks like `0`
* `I` (uppercase I) - looks like `1` or `l`

When tempted to use `l`, use `L` instead.

### Package and Module Names
* Short, all-lowercase names
* Underscores allowed if it improves readability
* Packages should avoid underscores when possible

```python
# Good module names:
import mymodule
import my_utilities

# C/C++ extension modules with Python wrapper:
import _socket  # C module
import socket   # Python wrapper
```

### Class Names
Use **CapWords** convention:

```python
class DataProcessor:
    pass

class UserAccount:
    pass
```

**Exceptions**: 
* Callable classes can use function naming (lowercase)
* Builtin names are often single words or run together

### Type Variable Names
Use **CapWords**, preferring short names. Add `_co`/`_contra` suffixes for variance:

```python
from typing import TypeVar

T = TypeVar('T')
AnyStr = TypeVar('AnyStr', str, bytes)
VT_co = TypeVar('VT_co', covariant=True)
KT_contra = TypeVar('KT_contra', contravariant=True)
```

### Exception Names
Use **CapWords** with **"Error" suffix** (if it's an error):

```python
class ValidationError(Exception):
    pass

class TimeoutError(Exception):
    pass
```

### Function and Variable Names
Use **lowercase** with **underscores** for readability:

```python
def calculate_total(items):
    user_count = len(items)
    return user_count
```

**Exception**: `mixedCase` is allowed only where it's already the prevailing style (e.g., `threading.py`) for backward compatibility.

### Function and Method Arguments

#### Instance Methods - Always Use `self`
```python
class MyClass:
    def my_method(self, arg):
        pass
```

#### Class Methods - Always Use `cls`
```python
class MyClass:
    @classmethod
    def from_config(cls, config):
        return cls()
```

#### Keyword Clashes
If argument name clashes with keyword, append single underscore rather than abbreviate:

```python
def process_data(class_):  # Better than 'clss' or 'klass'
    pass
```

### Method Names and Instance Variables
* Use function naming rules: **lowercase with underscores**
* Use **one leading underscore** for non-public methods/variables
* Use **two leading underscores** to invoke name mangling (avoid subclass conflicts)

```python
class Example:
    def public_method(self):
        """Anyone can use this."""
        pass
    
    def _protected_method(self):
        """Internal use or subclass API."""
        pass
    
    def __private_method(self):
        """Name mangled to avoid subclass conflicts."""
        pass
```

### Constants
All **UPPERCASE** with **underscores**:

```python
MAX_OVERFLOW = 100
DEFAULT_TIMEOUT = 30
PI = 3.14159
```

## Designing for Inheritance

### Public vs Non-Public Attributes

**Public Attributes**:
* No leading underscores
* You commit to backward compatibility
* Expected to be used by unrelated clients

**Non-Public Attributes**:
* Single leading underscore
* No guarantees - can change or be removed
* Not intended for third-party use

**Subclass API** ("protected"):
* Design explicitly for inheritance
* Document which attributes are public, which are subclass API, and which are truly private

### Guidelines

1. **Public attributes** - no leading underscores
2. **Keyword collision** - use trailing underscore (`class_`)
3. **Simple data attributes** - expose directly, don't add getters/setters until needed (use `@property` later if needed)
4. **Avoid expensive operations** in properties - users expect attributes to be cheap
5. **Subclass attributes** - use double underscore if you don't want subclasses to access them

## Public and Internal Interfaces

* Documented interfaces are **public** (unless explicitly marked provisional/internal)
* Undocumented interfaces are **internal**
* Use `__all__` to declare public API:

```python
# mymodule.py
__all__ = ['public_function', 'PublicClass']

def public_function():
    pass

def _internal_function():  # Not in __all__, and has leading underscore
    pass

class PublicClass:
    pass
```

* Even with `__all__`, prefix internal interfaces with underscore
* Imported names are implementation details unless explicitly documented as part of the API
