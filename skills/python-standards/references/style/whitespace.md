# Whitespace in Expressions and Statements

## Pet Peeves - Avoid These

### No Space Inside Brackets/Parentheses/Braces
```python
# Correct:
spam(ham[1], {eggs: 2})

# Wrong:
spam( ham[ 1 ], { eggs: 2 } )
```

### No Space Before Trailing Comma
```python
# Correct:
foo = (0,)

# Wrong:
bar = (0, )
```

### No Space Before Comma, Semicolon, or Colon
```python
# Correct:
if x == 4: print(x, y); x, y = y, x

# Wrong:
if x == 4 : print(x , y) ; x , y = y , x
```

### Slice Colon Spacing (Special Case)
Treat the colon like a binary operator with equal spacing on both sides:

```python
# Correct:
ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
ham[lower:upper], ham[lower:upper:], ham[lower::step]
ham[lower+offset : upper+offset]
ham[: upper_fn(x) : step_fn(x)], ham[:: step_fn(x)]

# Wrong:
ham[lower + offset:upper + offset]
ham[1: 9], ham[1 :9], ham[1:9 :3]
ham[lower : : step]
ham[ : upper]
```

### No Space Before Function Call Parenthesis
```python
# Correct:
spam(1)

# Wrong:
spam (1)
```

### No Space Before Indexing/Slicing Brackets
```python
# Correct:
dct['key'] = lst[index]

# Wrong:
dct ['key'] = lst [index]
```

### Don't Align Assignments with Extra Spaces
```python
# Correct:
x = 1
y = 2
long_variable = 3

# Wrong:
x             = 1
y             = 2
long_variable = 3
```

## Binary Operator Spacing

### Always Space Around These Operators
Single space on both sides:
* Assignment: `=`
* Augmented assignment: `+=`, `-=`, etc.
* Comparisons: `==`, `<`, `>`, `!=`, `<=`, `>=`, `in`, `not in`, `is`, `is not`
* Booleans: `and`, `or`, `not`

```python
# Correct:
i = i + 1
submitted += 1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)

# Wrong:
i=i+1
submitted +=1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)
```

### Operator Priority Spacing
Add whitespace around lower priority operators:

```python
# Correct:
i = i + 1
submitted += 1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)
```

## Function Annotations and Default Values

### Type Annotations - Always Space Around Arrow
```python
# Correct:
def munge(input: AnyStr): ...
def munge() -> PosInt: ...

# Wrong:
def munge(input:AnyStr): ...
def munge()->PosInt: ...
```

### No Space Around `=` in Keyword Arguments (Unannotated)
```python
# Correct:
def complex(real, imag=0.0):
    return magic(r=real, i=imag)

# Wrong:
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)
```

### But DO Space Around `=` When Combining Annotation with Default
```python
# Correct:
def munge(sep: AnyStr = None): ...
def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...

# Wrong:
def munge(input: AnyStr=None): ...
def munge(input: AnyStr, limit = 1000): ...
```

## Trailing Whitespace
Avoid trailing whitespace anywhere. It's usually invisible and can cause confusion (e.g., a backslash followed by space and newline doesn't count as line continuation).

## Compound Statements
Multiple statements on the same line are discouraged:

```python
# Correct:
if foo == 'blah':
    do_blah_thing()
do_one()
do_two()

# Wrong:
if foo == 'blah': do_blah_thing()
do_one(); do_two(); do_three()

# Definitely Wrong:
if foo == 'blah': do_blah_thing()
else: do_non_blah_thing()

try: something()
finally: cleanup()
```

## Line Breaking Around Binary Operators
Prefer breaking **before** binary operators (Knuth's style):

```python
# Correct: easy to match operators with operands
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)

# Wrong: operators sit far away from operands
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)
```

## Trailing Commas
Useful when using version control - put each item on its own line:

```python
# Correct:
FILES = [
    'setup.cfg',
    'tox.ini',
    ]
initialize(FILES,
           error=True,
           )

# Wrong:
FILES = ['setup.cfg', 'tox.ini',]
initialize(FILES, error=True,)

# Single-element tuples (trailing comma is mandatory):
FILES = ('setup.cfg',)  # Correct: parentheses for clarity
FILES = 'setup.cfg',    # Acceptable but less clear: parentheses recommended
```
