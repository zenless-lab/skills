# Document Structure & Whitespace

## Whitespace & Indentation
reST is indentation-sensitive. Consistent indentation is required to indicate block levels.

- **Blank Lines:** Required to separate blocks (paragraphs, lists, etc.). Multiple blank lines are treated as one.
- **Indentation:** Used for block quotes, definitions, and local nested content.
- **Tabs:** Converted to spaces (usually 8 columns). Use spaces for consistency.

## Document Structure
- **Document Title/Subtitle:** No specific syntax. A uniquely adorned top-level section title is treated as the title.
- **Sections:** Created by "underlining" title text with punctuation. Overlines are optional but must match underlines.
  - Recommended characters: `= - ` : . ' " ~ ^ _ * + #`
  - Hierarchy is determined by the order encountered.
- **Transitions:** A horizontal line of 4+ repeated punctuation characters. Requires blank lines before and after.

```rst
Chapter 1
=========

Section 1.1
-----------

Para.

----------

Para.
```
