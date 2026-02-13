# Programming Recommendations

## General Philosophy

### Python Implementation Compatibility
Write code that doesn't disadvantage other implementations (PyPy, Jython, IronPython, Cython).

**Example**: Don't rely on CPython's in-place string concatenation optimization:
```python
# Wrong: Slow in non-CPython implementations
a += b
a = a + b

# Correct: Fast in all implementations
''.join([a, b, c])  # For performance-sensitive code
```

## Comparisons

### None Comparisons
Always use `is` or `is not`, never equality operators:

```python
# Correct:
if x is not None:
    pass

# Wrong:
if x != None:
    pass
```

### Beware of Truthy/Falsy Context
```python
# Wrong: Will fail if x is an empty container
if x:
    do_something()

# Correct: Explicit None check
if x is not None:
    do_something()
```

### Preferred Operator Form
Use `is not` rather than `not ... is`:

```python
# Correct:
if foo is not None:

# Wrong:
if not foo is None:
```

### Type Comparisons
Use `isinstance()` instead of comparing types directly:

```python
# Correct:
if isinstance(obj, int):

# Wrong:
if type(obj) is type(1):
if type(obj) == int:  # Also wrong
```

### Boolean Comparisons
Don't compare booleans with `==` or `is`:

```python
# Correct:
if greeting:
if not greeting:

# Wrong:
if greeting == True:
if greeting is True:  # Even worse!
```

### Sequence Empty Checks
Use the fact that empty sequences are falsy:

```python
# Correct:
if not seq:
if seq:

# Wrong:
if len(seq):
if not len(seq):
if len(seq) == 0:
```

### String Prefix/Suffix Checks
Use `.startswith()` and `.endswith()`:

```python
# Correct:
if foo.startswith('bar'):
if foo.endswith('.txt'):

# Wrong:
if foo[:3] == 'bar':
if foo[-4:] == '.txt':
```

## Rich Comparisons
Implement all six operations for consistency:

```python
from functools import total_ordering

@total_ordering
class MyClass:
    def __eq__(self, other):
        ...
    
    def __lt__(self, other):
        ...
    
    # total_ordering generates: __le__, __gt__, __ge__, __ne__
```

Or implement all six manually: `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`.

## Functions and Lambda

### Use `def`, Not Lambda Assignment
```python
# Correct:
def f(x):
    return 2*x

# Wrong:
f = lambda x: 2*x
```

**Reason**: `def` gives the function a proper name for tracebacks. Lambda should only be used when embedded in larger expressions.

## Exceptions

### Derive from `Exception`
```python
# Correct:
class CustomError(Exception):
    pass

# Wrong:
class CustomError(BaseException):  # Reserved for system exceptions
    pass
```

### Design Exception Hierarchies for Catching
Base hierarchy on what catchers need to distinguish, not where exceptions are raised:

```python
class APIError(Exception):
    """Base for all API errors."""
    pass

class AuthenticationError(APIError):
    """Failed to authenticate."""
    pass

class RateLimitError(APIError):
    """API rate limit exceeded."""
    pass
```

### Exception Chaining
Use `raise X from Y` to preserve tracebacks:

```python
# Correct:
try:
    do_something()
except KeyError as e:
    raise AttributeError(f"Missing attribute: {e}") from e

# Explicit replacement (use sparingly):
raise AttributeError("Custom message") from None
```

### Catch Specific Exceptions
```python
# Correct:
try:
    import platform_specific_module
except ImportError:
    platform_specific_module = None

# Wrong:
try:
    import platform_specific_module
except:  # Catches SystemExit and KeyboardInterrupt!
    platform_specific_module = None
```

### Bare `except` Guidelines
Use only for:
1. Logging/printing traceback before re-raising
2. Cleanup before re-raising with `try...finally`

```python
# Acceptable:
try:
    risky_operation()
except:
    logger.exception("Operation failed")
    raise
```

### Minimize `try` Clause Scope
```python
# Correct:
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)

# Wrong: Too broad
try:
    return handle_value(collection[key])  # Will catch KeyError from handle_value!
except KeyError:
    return key_not_found(key)
```

### OS Error Handling
Use Python 3.3+ exception hierarchy:

```python
# Correct (Python 3.3+):
try:
    f = open('file.txt')
except FileNotFoundError:
    pass

# Old style (avoid):
import errno
try:
    f = open('file.txt')
except OSError as e:
    if e.errno == errno.ENOENT:
        pass
```

## Context Managers

### Use `with` for Resources
```python
# Correct:
with open('file.txt') as f:
    data = f.read()

# Wrong:
f = open('file.txt')
data = f.read()
f.close()  # Might not happen if exception occurs
```

### Be Explicit About Context Manager Behavior
```python
# Correct: Clear that this is starting a transaction
with conn.begin_transaction():
    do_stuff_in_transaction(conn)

# Wrong: Unclear what __enter__/__exit__ do
with conn:
    do_stuff_in_transaction(conn)
```

## Return Statements

### Be Consistent
Either all returns have expressions, or none do:

```python
# Correct:
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return None

# Correct:
def bar(x):
    if x < 0:
        return None
    return math.sqrt(x)

# Wrong: Inconsistent
def baz(x):
    if x >= 0:
        return math.sqrt(x)
    # Implicitly returns None
```

## Flow Control in `finally`

### Avoid `return`/`break`/`continue` in `finally`
They implicitly cancel propagating exceptions:

```python
# Wrong: Swallows the exception!
def foo():
    try:
        1 / 0
    finally:
        return 42  # Exception is lost

# Correct:
def foo():
    try:
        result = 1 / 0
    except ZeroDivisionError:
        return None
    else:
        return result
```

## Trailing Whitespace
Don't write string literals that rely on significant trailing whitespace. It's visually indistinguishable and some editors/tools strip it.
