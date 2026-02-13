# Comments and Documentation Strings

## General Comments Rules

### Keep Comments Up-to-Date
**Comments that contradict code are worse than no comments.** Always update comments when code changes.

### Complete Sentences
* Capitalize the first word (unless it's an identifier starting with lowercase)
* Use periods to end sentences
* Use one or two spaces after sentence-ending period (except after the final sentence)

### English Comments
Unless you're 120% sure code will never be read by non-speakers of your language, write comments in English.

## Block Comments

### When to Use
Apply to code that follows them.

### Style Rules
* Indented to the same level as the code
* Each line starts with `#` and a single space
* Paragraphs separated by a line containing just `#`

```python
# This is a block comment that explains
# the following section of code.
#
# This is a second paragraph in the block
# comment, separated by a blank comment line.
def complex_function():
    pass
```

## Inline Comments

### When to Use
Use **sparingly**. Unnecessary inline comments are distracting.

### Style Rules
* At least **two spaces** from the statement
* Start with `#` and a single space

```python
x = x + 1  # Compensate for border
```

### Don't State the Obvious
```python
# Wrong - states the obvious:
x = x + 1                 # Increment x

# Correct - explains why:
x = x + 1                 # Compensate for border
```

## Documentation Strings (Docstrings)

Full conventions in **PEP 257**. Key points:

### When to Write Docstrings
* All **public** modules, functions, classes, and methods
* Non-public methods: Use a comment after the `def` line instead

### Multiline Docstrings
Closing `"""` on its own line:

```python
def complex_function(arg1, arg2):
    """Return a foobang.
    
    Optional plotz says to frobnicate the bizbaz first.
    This function does many complex things that require
    multiple lines of explanation.
    """
    pass
```

### One-Line Docstrings
Keep closing `"""` on the same line:

```python
def simple_function():
    """Return an ex-parrot."""
    return ExParrot()
```

### Triple-Quote Style
Always use **double quotes** for docstrings: `"""Like this."""`

## Comments vs Docstrings

| Use Case | Solution |
|:---------|:---------|
| Explain what a public function does | Docstring |
| Explain what a private method does | Comment after `def` line |
| Explain why code works a certain way | Block or inline comment |
| Document API contracts, parameters, returns | Docstring (see PEP 257 and docstring style guides) |

## Example: Comprehensive Comment Usage

```python
"""
This module handles user authentication and session management.

It provides functions for logging in, logging out, and maintaining
user sessions with proper security measures.
"""

# Standard library imports
import hashlib
import secrets

# Configuration constants
MAX_LOGIN_ATTEMPTS = 3
SESSION_TIMEOUT = 3600  # seconds


def authenticate_user(username, password):
    """Authenticate a user with username and password.
    
    Args:
        username: The user's username
        password: The user's password (plaintext)
    
    Returns:
        User object if authentication succeeds, None otherwise.
    
    Raises:
        TooManyAttemptsError: If user has exceeded login attempts.
    """
    # Check if account is locked due to too many failed attempts
    if _is_account_locked(username):
        raise TooManyAttemptsError(username)
    
    # Hash password for comparison with stored hash
    password_hash = _hash_password(password)
    
    user = _get_user_by_username(username)
    
    if user and user.password_hash == password_hash:
        _reset_failed_attempts(username)
        return user
    else:
        _increment_failed_attempts(username)
        return None


def _hash_password(password):
    """Hash a password using SHA-256.
    
    Note: This is a simplified example. In production, use
    proper password hashing like bcrypt or Argon2.
    """
    # Add salt to prevent rainbow table attacks
    salt = _get_or_create_salt()
    salted = f"{salt}{password}".encode('utf-8')
    return hashlib.sha256(salted).hexdigest()
```

## Comment Pitfalls to Avoid

### Over-Commenting
```python
# Wrong: Too obvious
x = x + 1  # Add 1 to x
y = x * 2  # Multiply x by 2
z = y - 5  # Subtract 5 from y
```

### Under-Commenting
```python
# Wrong: Complex logic with no explanation
if (a > b and c < d) or (e == f and g != h):
    x = (y * z + w) / (q - r)
```

### Outdated Comments
```python
# Wrong: Comment doesn't match code
# Calculate the average of all values
total = sum(values)  # Comment says average, code does sum!
```

### Right Amount
```python
# Correct: Comments explain why, code shows how
# Use exponential backoff to avoid overwhelming the API
for attempt in range(MAX_RETRIES):
    try:
        response = api_call()
        break
    except RateLimitError:
        sleep_time = 2 ** attempt  # 1s, 2s, 4s, 8s, ...
        time.sleep(sleep_time)
```
