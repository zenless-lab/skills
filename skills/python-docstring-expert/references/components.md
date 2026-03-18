# What to Document by Component

## Modules
- Provide a high-level overview and purpose.
- Do NOT list members (classes/functions) unless required, as documentation frameworks usually do this automatically.
- *Note:* Module docstrings are often unnecessary unless the project uses a "code-as-documentation" framework. If a module is just a collection of unrelated utilities, a brief summary is sufficient.

## Classes
- Summarize the class's behavior and the entity it represents.
- List public methods and properties if they aren't immediately obvious.
- **Crucial:** Document the constructor (`__init__`) parameters in the *class* docstring, not in the `__init__` method docstring. The `__init__` method itself should typically lack a docstring unless there are specific initialization side effects to detail.

## Functions and Methods
- Summarize specific behavior.
- Detail parameters (including types if not type-hinted, though type hints are preferred).
- Detail return values and types.
- Detail side effects and known exceptions (`Raises`).
