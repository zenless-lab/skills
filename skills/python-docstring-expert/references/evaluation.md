# Evaluating Docstring Necessity

Avoid over-documenting. Documentation is for humans. Only write docstrings if they provide value beyond the code itself. Code clarity and self-documentation through good structuring and naming must ALWAYS take priority over adding docstrings.

## When to Write Docstrings

- **Public APIs**: Exported modules, classes, functions, and public methods *should* have docstrings. They serve as a contract with external users.
- **Complex Logic**: Code with non-intuitive or complex logic that cannot be fully explained by its name requires a docstring for IDE integration and user understanding.
- **Large Code Blocks**: Lengthy components that cannot be understood at a glance benefit from a summarizing docstring.

## When NOT to Write Docstrings

- **Private APIs**: Simplify or omit docstrings for private members (`_prefix`).
- **Simple/Self-Documenting Code**: Do NOT write a docstring if it simply repeats the function/class name. If the name isn't enough but the logic is simple, prefer standard inline comments (`#`) or a single-line docstring over a verbose multi-line one.
