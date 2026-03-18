# Inline Markup Reference

Inline markup applies within a text block. It cannot be nested.

- **Emphasis:** `*emphasis*` (italics)
- **Strong Emphasis:** `**strong**` (bold)
- **Interpreted Text:** `` `interpreted text` `` (role inferred or explicit like `:role:\`text\``).
- **Inline Literals:** ```` ``inline literals`` ```` (monospaced, no markup interpretation).
- **Substitution References:** `|substitution|`.
- **Inline Internal Targets:** `_`target``.
- **Footnote References:** `[1]_`, `[#]_`, `[*]_`.
- **Hyperlink References:** ``` `phrase`_ ``` (named), ``` `phrase`__ ``` (anonymous), `word_`.

## Recognition Rules
Markup delimiters are only recognized if:
1. Start-string followed by non-whitespace.
2. End-string preceded by non-whitespace.
3. Separated by at least one character.
4. Not preceded by an unescaped backslash.
5. Punctuation around the markup must not match corresponding delimiters (e.g., `('*')` is fine, but `(*)` is not).

## Character-Level Inline Markup
Use backslash-escaped whitespace or escapes to immediately precede or follow markup.
```rst
re\ ``Structured``\ Text
```

## Hyperlink Reference Features
- **Embedded URIs/Aliases:** ``` `Link Text <https://url.com>`_ ```
- **Standalone Hyperlinks:** `https://python.org`, `user@example.com`.
- **Order of Recognition:** Strong emphasis > Emphasis > Inline literals > Inline internal targets > Phrase hyperlink references > Interpreted text > Footnote references > Standalone hyperlinks.
