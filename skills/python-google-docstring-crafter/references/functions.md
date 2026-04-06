# Function and Method Docstrings

A docstring is mandatory for functions that are part of the public API, are of nontrivial size, or have non-obvious logic.

### Core Guidelines

- **Inform the Caller:** Provide enough information to use the function without reading its implementation.
- **Describe Semantics:** Document what the function does and what its arguments mean, including side effects.
- **Style Consistency:** Use either descriptive style (`"""Fetches rows from Bigtable."""`) or imperative style (`"""Fetch rows from Bigtable."""`) consistently within a file.

### Section Formatting

Each section begins with a heading line followed by a colon. Maintain a consistent hanging indent of two or four spaces for the body of each section.

#### Args:
List each parameter by name. Follow the name with a colon and a description. If the description is long, use a hanging indent (2 or 4 spaces more than the parameter name). Include types only if type annotations are missing.

#### Returns: (or Yields: for generators)
Describe the semantics of the return value. If the function returns `None`, omit this section. For generators, document the object returned by `next()`.

#### Raises:
List all relevant exceptions followed by a description. Do not document exceptions that would only occur if the API is misused.

#### Examples:
Provide usage examples where appropriate. These are often formatted as a code block. For module-level docstrings, the heading "Typical usage example:" is preferred.

### Overridden Methods

Do not provide a docstring for a method that overrides a base class method if it is explicitly decorated with `@override`, unless the behavior refinement is significant.

### Why

Proper function docstrings make the API discoverable and easier to use, while structured sections ensure consistency across the codebase.
