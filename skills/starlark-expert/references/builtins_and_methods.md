# Starlark Built-in Functions and Methods

## Table of Contents

* [Built-in Constants and Functions](#built-in-constants-and-functions) (Lines 15 - 234)
* [Built-in Methods](#built-in-methods) (Lines 235 - 500)
  * [Bytes Methods](#bytes-methods) (Lines 239 - 249)
  * [Dictionary Methods](#dictionary-methods) (Lines 249 - 301)
  * [List Methods](#list-methods) (Lines 302 - 336)
  * [Set Methods](#set-methods) (Lines 337 - 406)
  * [String Methods](#string-methods) (Lines 407 - 500)

---

## Built-in Constants and Functions

### None

`None` is the distinguished value of the type `NoneType`.

### True and False

`True` and `False` are the two values of type `bool`.

### abs

`abs(x)` takes either an integer or a float, and returns the absolute value of that number.

### any

`any(x)` returns `True` if any element of the collection `x` is true. If the collection is empty, it returns `False`.

### all

`all(x)` returns `False` if any element of the collection `x` is false. If the collection is empty, it returns `True`.

### bool

`bool(x)` interprets `x` as a Boolean value---`True` or `False`. With no argument, `bool()` returns `False`.

### bytes

`bytes(x)` converts its argument to a `bytes`.

* If x is a `bytes`, the result is x.
* If x is a string, the result is a `bytes` whose elements are the UTF-8 encoding of the string.
* If x is an iterable of int values, the result is a `bytes` whose elements are those integers.

```python
bytes("hello 😃")  # b"hello 😃"
bytes(b"hello 😃")  # b"hello 😃"
bytes("hello 😃"[:-1])          # b"hello ���"
bytes([65, 66, 67])  # b"ABC"
bytes(65)   # error: got int, want string, bytes, or iterable of int
```

### dict

`dict` creates a dictionary. It accepts up to one positional argument (an iterable of key/value pairs) and any number of keyword arguments.

```python
dict()                          # {}, empty dictionary
dict([(1, 2), (3, 4)])          # {1: 2, 3: 4}
dict(one=1, two=2)              # {"one": 1, "two": 2}
```

### dir

`dir(x)` returns a new sorted list of the names of the attributes (fields and methods) of its operand.

```python
dir("hello")                    # ['capitalize', 'count', ...], the methods of a string
```

### enumerate

`enumerate(x)` returns a list consisting of pairs `(i, v)`, where each successive `v` is the next item of collection `x`, and where `i` starts at 0.

```python
enumerate(["zero", "one", "two"])    # [(0, "zero"), (1, "one"), (2, "two")]
enumerate(["one", "two"], 1)         # [(1, "one"), (2, "two")]
```

### fail

The `fail(*args)` function causes execution to fail with an error message that includes the string forms of the argument values.

```python
fail("oops")                    # "fail: oops"
fail("oops", 1, False)          # "fail: oops 1 False"
```

### float

`float(x)` interprets its argument as a floating-point number.
Accepts `int`, `float`, `bool`, or `string` (including "Inf", "NaN"). With no argument, `float()` returns `0.0`.

### getattr

`getattr(x, name[, default])` returns the value of the attribute (field or method) of x named `name`.

```python
getattr("banana", "split")("a")         # ["b", "n", "n", ""], equivalent to "banana".split("a")
getattr("banana", "myattr", "mydefault")# "mydefault"
```

### hasattr

`hasattr(x, name)` reports whether x has an attribute (field or method) named `name`.

### hash

`hash(x)` returns an integer hash of a string or bytes x such that two equal values have the same hash.

### int

`int(x[, base])` interprets its argument as an integer.

```python
int("21")          # 21
int("1234", 16)    # 4660
int("0x1234", 0)   # 4660
```

### len

`len(x)` returns the number of elements in its argument. It is a dynamic error if its argument is not a collection, string, or bytes.

### list

`list(x)` returns a new list containing the elements of the iterable `x`. With no argument, `list()` returns a new empty list.

### max

`max(x)` returns the greatest element in the collection `x`.

```python
max([3, 1, 4, 1, 5, 9])                         # 9
max("two", "three", "four", key=len)            # "three", the longest
```

### min

`min(x)` returns the least element in the collection `x`.

```python
min([3, 1, 4, 1, 5, 9])                         # 1
min("two", "three", "four", key=len)            # "two", the shortest
```

### print

`print(*args, sep=" ")` prints its arguments, followed by a newline.

```python
print(1, "hi", x=3)                             # "1 hi x=3\n"
print("hello", "world", sep=", ")               # "hello, world\n"
```

### range

`range` returns an immutable sequence of integers defined by the specified interval and stride.

```python
list(range(10))                                 # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
list(range(3, 10, 2))                           # [3, 5, 7, 9]
```

### repr

`repr(x)` formats its argument as a string. All strings in the result are double-quoted.

```python
repr(1)                 # '1'
repr("x")               # '"x"'
repr([1, "x"])          # '[1, "x"]'
```

### reversed

`reversed(x)` returns a new list containing the elements of the collection `x` in reverse order.

```python
reversed(range(5))                              # [4, 3, 2, 1, 0]
```

### set

`set(x)` returns a new set containing the unique elements of the iterable `x` in iteration order.

```python
set([3, 1, 1, 2])              # set([3, 1, 2]), a set of three elements
```

### sorted

`sorted(x)` returns a new list containing the elements of the collection x, in sorted order.

```python
sorted([3, 1, 4, 1, 5, 9], reverse=True)                   # [9, 5, 4, 3, 1, 1]
sorted(["two", "three", "four"], key=len)                  # ["two", "four", "three"]
```

### str

`str(x)` formats its argument as a string.

```python
str("x")                        # 'x'
str([1, "x"])                   # '[1, "x"]'
str(0.0)                        # '0.0'
```

### tuple

`tuple(x)` returns a tuple containing the elements of the iterable `x`. With no arguments, `tuple()` returns the empty tuple.

### type

`type(x)` returns a string describing the type of its operand.

```python
type(None)              # "NoneType"
type(0)                 # "int"
```

### zip

`zip()` returns a new list of n-tuples formed from corresponding elements of each of the n collections provided as arguments.

```python
zip(range(10), ["a", "b", "c"])         # [(0, "a"), (1, "b"), (2, "c")]
```

---

## Built-in Methods

Methods are selected using dot expressions (e.g., `"banana".count("a")`).

### Bytes Methods

#### bytes·elems

`b.elems()` returns an opaque iterable value containing successive int elements of b.

```python
list(b"ABC".elems())  # [65, 66, 67]
```

### Dictionary Methods

#### dict·clear

`D.clear()` removes all the entries of dictionary D and returns `None`.

#### dict·get

`D.get(key[, default])` returns the dictionary value corresponding to the given key.

#### dict·items

`D.items()` returns a new list of key/value pairs, one per element in dictionary D.

```python
{"one": 1, "two": 2}.items()            # [("one", 1), ("two", 2)]
```

#### dict·keys

`D.keys()` returns a new list containing the keys of dictionary D.

#### dict·pop

`D.pop(key[, default])` returns the value corresponding to the specified key, and removes it from the dictionary.

#### dict·popitem

`D.popitem()` returns the first key/value pair, removing it from the dictionary.

#### dict·setdefault

`D.setdefault(key[, default])` returns the dictionary value corresponding to the given key. If not found, it inserts the new key/value entry.

```python
x = {"one": 1, "two": 2}
x.setdefault("three", 3)                # 3
# x is now {"one": 1, "two": 2, "three": 3}
```

#### dict·update

`D.update([pairs][, name=value[, ...]])` makes a series of key/value insertions into dictionary D, then returns `None`.

```python
x = {}
x.update([("a", 1), ("b", 2)], c=3)     # x becomes {"a": 1, "b": "2", "c": 3}
```

#### dict·values

`D.values()` returns a new list containing the dictionary's values.

### List Methods

#### list·append

`L.append(x)` appends `x` to the list L, and returns `None`.

#### list·clear

`L.clear()` removes all the elements of the list L and returns `None`.

#### list·extend

`L.extend(x)` appends the elements of `x`, which must be iterable, to the list L, and returns `None`.

#### list·index

`L.index(x[, start[, end]])` finds `x` within the list L and returns its index.

```python
x = ["b", "a", "n", "a", "n", "a"]
x.index("a", 2)                         # 3 (banAna)
```

#### list·insert

`L.insert(i, x)` inserts the value `x` in the list L at index `i`, moving higher-numbered elements along by one.

#### list·pop

`L.pop([index])` removes and returns the last element of the list L, or, if the optional index is provided, at that index.

#### list·remove

`L.remove(x)` removes the first occurrence of the value `x` from the list L, and returns `None`.

### Set Methods

#### set·add

`S.add(x)` adds the value `x` to the set `S`. Returns `None`.

#### set·clear

`S.clear()` removes all elements from the set `S`. Returns `None`.

#### set·difference

`S.difference(*others)` returns a new set containing elements found in `S` but not found in any of `*others`.

```python
set([1, 2, 3]).difference([2])          # set([1, 3])
```

#### set·difference_update

`S.difference_update(*others)` removes from the set `S` any elements found in any of the collections `*others`. Returns `None`.

#### set·discard

`S.discard(x)` removes the value `x` from the set `S` if present. Returns `None`.

#### set·intersection

`S.intersection(*others)` returns a new set containing those elements that `S` and all of `*others` have in common.

#### set·intersection_update

`S.intersection_update(*others)` removes from `S` any elements not found in at least one of `*others`. Returns `None`.

#### set·isdisjoint

`S.isdisjoint(x)` returns `True` if `S` and `x` do not have any values in common.

#### set·issubset

`S.issubset(x)` returns `True` if every element of `S` is present in `x`.

#### set·issuperset

`S.issuperset(x)` returns `True` if every element of `x` is present in `S`.

#### set·pop

`S.pop()` removes and returns the first element (in iteration order) from the set `S`.

#### set·remove

`S.remove(x)` removes the value `x` from the set `S`. Fails if `x` is not present.

#### set·symmetric_difference

`S.symmetric_difference(x)` returns a new set containing elements found only in `S` or in `x` but not those found in both.

#### set·symmetric_difference_update

`S.symmetric_difference_update(x)` removes from `S` any elements found in both `S` and `x`, and adds to `S` any elements found in `x` but not in `S`.

#### set·union

`S.union(*others)` returns a new set containing elements found in `S` or in any of `*others`.

#### set·update

`S.update(*others)` adds to `S` any elements found in any of `*others`.

### String Methods

#### string·capitalize

`S.capitalize()` returns a copy of string S, where the first character (if any) is converted to uppercase.

#### string·count

`S.count(sub[, start[, end]])` returns the number of occurrences of `sub` within the string S.

#### string·elems

`S.elems()` returns an opaque iterable value containing successive 1-element substrings of S.

#### string·endswith

`S.endswith(suffix[, start[, end]])` reports whether the string `S[start:end]` has the specified suffix.

#### string·find

`S.find(sub[, start[, end]])` returns the index of the first occurrence of the substring `sub` within S, or -1 if not found.

#### string·format

`S.format(*args, **kwargs)` returns a version of the format string S in which bracketed portions `{...}` are replaced by arguments.

```python
"a{x}b{y}c{}".format(1, x=2, y=3)               # "a2b3c1"
```

#### string·index

`S.index(sub[, start[, end]])` is like `S.find`, except that if the substring is not found, the operation fails.

#### string·isalnum, isalpha, isdigit, islower, isspace, istitle, isupper

Reports whether the string meets the respective character class condition.

#### string·join

`S.join(iterable)` returns the string formed by concatenating each element of its argument, with a copy of S between elements.

```python
", ".join(["one", "two", "three"])      # "one, two, three"
```

#### string·lower

`S.lower()` returns a copy of the string S with letters converted to lowercase.

#### string·lstrip, rstrip, strip

Returns a copy of the string S with leading, trailing, or both whitespace (or specified cutset) removed.

```python
"  hello  ".strip()                     # "hello"
```

#### string·partition, rpartition

`S.partition(x)` splits string S into three parts: the portion before the first occurrence of `x`, `x` itself, and the portion following it. `rpartition` splits at the last occurrence.

#### string·removeprefix, removesuffix

`S.removeprefix(x)` removes the prefix `x` from the string S at most once. `removesuffix` does the same for the suffix.

#### string·replace

`S.replace(old, new[, count])` returns a copy of string S with all occurrences of substring `old` replaced by `new`.

#### string·rfind, rindex

Like `find` and `index`, but searches for the *last* occurrence of the substring.

#### string·split, rsplit

`S.split([sep [, maxsplit]])` returns the list of substrings of S, splitting at occurrences of the delimiter string `sep`. `rsplit` chooses rightmost splits when `maxsplit` is provided.

#### string·splitlines

`S.splitlines([keepends])` returns a list whose elements are the successive lines of S.

#### string·startswith

`S.startswith(prefix[, start[, end]])` reports whether the string `S[start:end]` has the specified prefix.

#### string·title

`S.title()` returns a copy of the string S with letters converted to titlecase.

#### string·upper

`S.upper()` returns a copy of the string S with letters converted to uppercase.
