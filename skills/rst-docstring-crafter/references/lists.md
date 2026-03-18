# Lists & Field Lists

## Bullet & Enumerated Lists
Lists must start after a blank line. Body elements must be indented relative to the marker.

- **Bullet Markers:** `*`, `+`, `-`, `•`, `‣`, `⁃`.
- **Enumeration Sequences:** Arabic numerals (`1.`), Alphabet characters (`A.`, `a.`), Roman numerals (`I.`, `i.`).
- **Auto-enumerator:** Use `#.` for automatic numbering.
- **Formatting Types:** Suffix with a period (`1.`), parentheses (`(1)`), or right-parenthesis (`1)`).

## Definition Lists
A term followed by a definition. The definition is indented relative to the term.

- **Term:** A simple one-line phrase.
- **Classifiers:** Optional, following the term after an inline ` : `.

```rst
term 1 : classifier
    Definition of term 1.
```

## Field Lists
Map names to bodies, modeled on RFC822. Used for metadata and directives.

- **Format:** `:Field Name: Field body content.`
- **Indentation:** Field body lines must align with each other.
- **Docstring Fields:** `:param name:`, `:type name:`, `:raises Error:`, `:returns:`, `:rtype:`.
- **Bibliographic Fields:** First element in a document (e.g., `Author`, `Version`).
- **RCS Keywords:** Expanded strings like `$Date$`.

## Option Lists
Map command-line options to descriptions.

- **Syntax:** `-a`, `--long`, `/V`, `-o arg`.
- **Formatting:** Must be at least two spaces between the option and the description.

```rst
-a         All.
--input=F  Set file F.
```
