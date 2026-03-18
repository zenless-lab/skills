# Sections Overview

The docstring consists of a number of sections separated by headings. Each heading should be underlined in hyphens (`-`), matching the exact length of the heading name.

The section ordering should be consistent with the description below.

1.  **Short summary**: A one-line summary that does not use variable names or the function name.
2.  **Deprecation warning**: (Use if applicable) Warns users that the object is deprecated. Uses the `.. deprecated::` Sphinx directive instead of an underlined header.
3.  **Extended Summary**: A few sentences giving an extended description. Clarify *functionality*, not implementation detail or theory.
4.  **Parameters**: Description of the function arguments, keywords and their respective types.
5.  **Returns**: Explanation of the returned values and their types.
6.  **Yields**: Explanation of the yielded values and their types (for generators).
7.  **Receives**: Explanation of parameters passed to a generator's `.send()` method.
8.  **Other Parameters**: An optional section used to describe infrequently used parameters.
9.  **Raises**: An optional section detailing which errors get raised and under what conditions.
10. **Warns**: An optional section detailing which warnings get raised and under what conditions.
11. **Warnings**: An optional section with cautions to the user in free text/reST.
12. **See Also**: An optional section used to refer to related code.
13. **Notes**: An optional section that provides additional information about the code, possibly including a discussion of the algorithm or mathematical equations.
14. **References**: References cited in the Notes section.
15. **Examples**: An optional section for examples, using the doctest format.

### Why
Using explicitly named and underlined sections ensures that the docstrings are easily parsable by automated tools like Sphinx (via numpydoc) and are highly readable as plain text. Adhering to the specific order ensures a predictable structure across large codebases.
