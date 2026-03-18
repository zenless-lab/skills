# reST Mechanics & Measures

## Escaping Mechanism
A backslash `\` escapes the following character.

- **Escaped non-white characters:** Represent themselves.
- **Escaped whitespace:** Removed from the output. In URI context, represents a single space.
- **Literal Context:** Backslashes are literal in literal blocks, inline literals, code/math/raw directives.

## Reference Names
Reference names identify elements for cross-referencing.

- **Simple Reference Name:** Single word consisting of alphanumerics plus isolated internal hyphens, underscores, periods, colons, and plus signs.
- **Phrase References:** Enclosed in backquotes ``` `phrase` ```.
- **Normalization:** Whitespace is normalized to a single space. Case is normalized to lowercase.
- **Namespace:** Hyperlinks, footnotes, and citations share a namespace. Substitutions have a separate case-sensitive (forgiving) namespace.

## Measures and Units
Measures consist of a positive floating-point number and an optional unit (e.g., `1.5em`, `20 mm`).

- **Length Units:** `em`, `ex`, `ch`, `rem`, `vw`, `vh`, `vmin`, `vmax`, `cm`, `mm`, `Q`, `in`, `pc`, `pt`, `px`.
- **Percentage Unit:** Signified by `%`. Relative to context.

## Error Handling
System messages and problematic tokens are generated for markup errors.
- **Problematic elements:** Inline fragments identified as having errors.
- **System messages:** Levels range from INFO (0) to FATAL (4).
- **PEP 258:** Error handling follows the Docutils specification.
