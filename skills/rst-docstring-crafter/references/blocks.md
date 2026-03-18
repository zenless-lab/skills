# Blocks & Paragraphs

## Paragraphs
A block of left-aligned text with no other markup. Blank lines are required separators.

## Literal Blocks
Finished with a double-colon `::` in the preceding paragraph. Contents are preformatted and monospaced. Markup processing is disabled.

- **Indented:** Block must be indented relative to the preceding paragraph.
- **Quoted:** Unindented, but each line starts with the same non-alphanumeric character.
- **Minimization:** `::` preceded by whitespace is removed from output. `::` at the end of text is replaced by a single `:`.

```rst
This is a paragraph::

    Indented literal block (code, ASCII art).
```

## Line Blocks
Groups of lines starting with a vertical bar `|`. Line breaks and initial indentation are preserved. Continuation lines (wrapped) begin with a space instead of a bar.

```rst
| Verse line 1
| Verse line 2
  continuation of line 2
|   Nested line
```

## Block Quotes
A block of text indented relative to the preceding text. No special marker is needed.

- **Attributions:** A paragraph starting with `--`, `---`, or an em-dash at the bottom of the quote.
- **Termination:** An empty comment `..` can be used to separate a block quote from a preceding list or to separate two quotes.

```rst
    "It is my business to know things."

    -- Sherlock Holmes
```

## Doctest Blocks
Interactive Python sessions starting with the interpreter prompt `>>> `. Indentation is not required.

```rst
>>> print('Hello Doctest')
Hello Doctest
```
