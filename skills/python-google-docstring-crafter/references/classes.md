# Class Docstrings

Every class should have a docstring below its definition describing its purpose and attributes.

### Core Guidelines

- **Summarize:** Start with a one-line summary describing what the class instance represents.
- **Describe Instance:** For subclasses of `Exception`, describe what the exception represents, not the context in which it occurs.
- **Avoid Redundancy:** Do not include redundant information, like saying the class is a "class".

### Attributes Section

Document public attributes (excluding properties) in an `Attributes` section. Use the same formatting as the `Args` section for functions.

### Example

```python
class SampleClass:
    """Summary of class here.

    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam: bool = False):
        """Initializes the instance with preferences.

        Args:
          likes_spam: Defines if the instance exhibits this preference.
        """
        self.likes_spam = likes_spam
        self.eggs = 0
```

### Why

Class docstrings help developers understand the state and data structures within a system, while documenting attributes provides a clear overview of the instance's properties.
