# Block and Inline Comments

Use comments for tricky parts of the code. If code logic is complex, document it before the operations commence.

### Core Guidelines

- **Focus on Intent:** Explain *why* something is done or what the *intended outcome* is.
- **Do Not Describe Code:** Assume the reader knows Python and focus on the reasoning.
- **Explain Tricky Logic:** If code logic is complex, document it before the operations commence. Non-obvious operations get comments at the end of the line.

### Formatting Rules

1.  **Block Comments:** Use these for explaining multiple lines or complicated logic.
2.  **Inline Comments:** Position inline comments at least 2 spaces from the code. Use a single `#` followed by a space.

```python
if i & (i-1) == 0:  # True if i is 0 or a power of 2.
```

### Why

Comments ensure that complex or non-obvious logic is maintainable by others, while intent-focused comments help developers avoid mistakes when modifying the code later.
