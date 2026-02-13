# Unittest (Standard Library) Patterns

## Core Philosophy
xUnit style (Java JUnit derivative). Tests are classes inheriting from `unittest.TestCase`.

## Key Concepts
* **Discovery**: `python -m unittest discover`.
* **Assertions**: Use methods like `self.assertEqual`, `self.assertTrue`.
* **Lifecycle**: `setUp()` and `tearDown()` methods run before/after every test method.

## Structure Example
```python
# tests/test_math.py
import unittest
from my_app import add

class TestMath(unittest.TestCase):
    def setUp(self):
        self.base_val = 10

    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_error(self):
        with self.assertRaises(ValueError):
            add("a", 1)

if __name__ == '__main__':
    unittest.main()
```
