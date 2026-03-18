---
name: rst-docstring-crafter
description: Expert guidance for writing, editing, and formatting reStructuredText (reST), Python docstrings, and Sphinx projects.
---

# reStructuredText (reST) Crafter

reStructuredText is the standard markup for technical documentation and Python docstrings. It is highly sensitive to indentation and blank lines.

## Quick Syntax Reference
- **Inline:** Use `*italic*`, `**bold**`, ` ``literal`` `, and `links_`.
- **Lists:** Bulleted (`-`), Enumerated (`1.`), or Field lists (`:key: value`).
- **Blocks:** Indented literal blocks follow a `::` suffix on the previous paragraph.
- **Sections:** Title text followed by a symbol underline (`=`, `-`, `~`, `^`, `*`).
- **Explicit Markup:** Blocks starting with `.. ` (directives, targets, comments).

### Basic Example
```rst
Title
=====
A paragraph with **bold** text and a `link <https://python.org>`_.

* Bullet list item
* Field list: :param my_arg: Value

::

    # Indented literal block
    print("Hello reST")
```

## Detailed Syntax References
Refer to these files for in-depth rules and complex examples:
- **[Structure](references/structure.md):** Document titles, sections, whitespace, indentation, and transitions.
- **[Blocks & Paragraphs](references/blocks.md):** Literal, line, quote, and doctest syntax.
- **[Lists & Fields](references/lists.md):** Bullet, enumerated, definition, field, and option lists (includes docstring fields).
- **[Tables](references/tables.md):** Grid and Simple table formatting, rules, and spans.
- **[Explicit Markup](references/explicit.md):** Footnotes, citations, targets, directives, and substitutions.
- **[Inline Markup](references/inline.md):** All 9 inline markup types, recognition rules, and order.
- **[Mechanics & Measures](references/mechanics.md):** Escaping, reference normalization, measures/units, and error handling.

## Audit Checklist

When reviewing or writing reStructuredText docstrings, use this checklist:

- [ ] Are blocks properly indented (usually 4 spaces) to match their parent context?
- [ ] Are lists and paragraphs separated by blank lines?
- [ ] Are field lists (e.g., `:param:`, `:returns:`) properly formed and indented?
- [ ] Are inline markups strictly closed (e.g., `*italic*`, `**bold**`, ` ``literal`` `)?
- [ ] Are cross-references and links properly formatted without syntax errors?
- [ ] Do literal blocks (`::`) have a preceding blank line and are they correctly indented?
- [ ] Does the docstring properly declare types (e.g., `:type param: int`) if not using type hints?

## Instructions
1.  **Strict Indentation:** All blocks must be properly indented and separated by blank lines.
2.  **Consult References:** Use the **Detailed Syntax References** list above to identify which file contains the specific rules needed for complex constructs.
3.  **Docstring Fields:** Always use field lists (`:param:`, `:returns:`) for API documentation.
4.  **Use Templates:** Apply standard templates for consistent API docstrings:

## Templates

### Modules
- [Single Line Module](assets/module_single_line_template.py)
- [Private Module](assets/module_private_template.py)
- [Public Module](assets/module_public_template.py)

### Classes
- [Single Line Class](assets/class_single_line_template.py)
- [Private Class](assets/class_private_template.py)
- [Public Class](assets/class_public_template.py)

### Functions & Methods
- [Single Line Function](assets/function_single_line_template.py)
- [Private Function](assets/function_private_template.py)
- [Public Function](assets/function_public_template.py)
