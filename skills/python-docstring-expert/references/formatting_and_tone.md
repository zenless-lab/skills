# Formatting, Doctests, and Tone

## Formatting Rules

### Single-line Docstrings
- Use for simple, obvious functionality where a docstring is still deemed necessary.
- Keep the `"""` on the same line as the content.
- End with a period `.`.
- *Rule:* If the single-line docstring just repeats the function name, delete it entirely.

### Multi-line Docstrings
- Start with `"""` followed immediately by a concise, single-line summary.
- Leave one blank line.
- Provide detailed content (parameters, returns, exceptions, etc.).
- Close with `"""` on its own line.

## Voice and Tone

- **Priority 1:** Follow explicit user requests or `AGENTS.md`.
- **Priority 2:** Match the existing code base's consistency (e.g., declarative "Returns the user" vs. imperative "Return the user").
- **Priority 3:** Default to PEP 257. PEP 257 mandates the **imperative mood** for summaries (e.g., "Do X", "Return Y"). However, community consensus sometimes diverges, especially with documentation generators. Consistency within the file/project is more important than strict adherence to PEP 257.

## 3. Doctests Philosophy

- The primary goal of doctests in docstrings is **explanation and illustration**, not comprehensive testing.
- Do NOT use doctests for edge-case testing or replacing unit tests. Keep them readable.
- For frequently used public APIs, include typical input/output examples to guide users and serve as simple verification.
