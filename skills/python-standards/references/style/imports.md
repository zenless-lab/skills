# Import Conventions

## Basic Rules

### Imports on Separate Lines
```python
# Correct:
import os
import sys

# Wrong:
import sys, os
```

**Exception** - multiple items from same module are OK:
```python
# Correct:
from subprocess import Popen, PIPE
```

## Import Location
Imports always go at the **top of the file**, after:
1. Module docstring
2. Module-level dunder names (except `from __future__` imports)

But before:
1. Module globals and constants

## Import Grouping
Group imports in this order, with a **blank line** between each group:

1. **Standard library imports**
2. **Related third-party imports**
3. **Local application/library imports**

```python
"""Module docstring."""

from __future__ import annotations  # Future imports first

__version__ = '1.0'
__author__ = 'Your Name'

# Group 1: Standard library
import os
import sys
from pathlib import Path

# Group 2: Third-party
import numpy as np
import requests
from django.conf import settings

# Group 3: Local
from . import models
from .utils import helper_function
```

## Absolute vs Relative Imports

### Absolute Imports (Recommended)
More readable and better error messages:

```python
import mypkg.sibling
from mypkg import sibling
from mypkg.sibling import example
```

### Explicit Relative Imports (Acceptable Alternative)
Useful for complex package layouts where absolute imports would be verbose:

```python
from . import sibling
from .sibling import example
from ..parent import something
```

**Standard library code** should avoid complex layouts and always use absolute imports.

## Importing Classes

### Direct Class Import
Usually OK:

```python
from myclass import MyClass
from foo.bar.yourclass import YourClass
```

### If Name Clashes Occur
Import the module instead:

```python
import myclass
import foo.bar.yourclass

# Use fully qualified names:
obj1 = myclass.MyClass()
obj2 = foo.bar.yourclass.YourClass()
```

## Wildcard Imports

### Avoid `from module import *`
Makes it unclear which names are in the namespace. Confuses readers and automated tools.

```python
# Wrong:
from module import *
```

### Defensible Use Case
Republishing an internal interface as public API:

```python
# api.py - Public API module
from ._internal import *  # Republish accelerated C implementations

# Still follow guidelines on public/internal interfaces
__all__ = ['public_func1', 'public_func2']
```

## Module Level Dunder Names
Place after module docstring but before imports (except `from __future__`):

```python
"""This is the example module.

This module does stuff.
"""

from __future__ import annotations  # Future imports MUST be first

__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Cardinal Biggles'

import os
import sys
```

## Source File Encoding

### Python 3 Default
UTF-8 is the default. **No encoding declaration needed**.

### Non-UTF-8 Encodings
Should only be used for **test purposes**. Use non-ASCII characters sparingly - prefer them only for places and human names.

### ASCII Identifiers Required
All identifiers in standard library **MUST** use ASCII-only identifiers and **SHOULD** use English words where feasible.

## String Quotes

### Single vs Double Quotes
PEP 8 makes no recommendation - pick one and be consistent.

### When String Contains Quotes
Use the opposite quote to avoid backslashes:

```python
# Good:
text = "He said 'hello'"
message = 'Use "quotes" wisely'

# Avoid:
text = 'He said \'hello\''  # Backslashes hurt readability
```

### Triple-Quoted Strings
Always use **double quotes** to match docstring convention (PEP 257):

```python
"""This is a docstring."""

message = """This is a
multi-line string."""
```
