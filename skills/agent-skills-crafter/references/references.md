# Guide: Creating Reference Documents

Skills use **progressive disclosure**. This means `SKILL.md` should remain a high-level orchestration file (< 5000 tokens), while detailed, domain-specific knowledge should be offloaded to separate files in the `references/` directory.

## When to Create a Reference File
- **Large Contexts:** If the information takes up more than 100-200 lines, move it out of `SKILL.md`.
- **Conditional Knowledge:** If the information is only needed in specific edge cases (e.g., `api_errors.md`, `legacy_system_auth.md`), move it. The agent will only load it if it encounters that edge case.
- **Structured Data:** Large JSON schemas, YAML templates, or extensive CSV lookup tables should be stored as references or assets.

## Best Practices for Reference Content
- **Focus and Isolate:** A single reference file should cover a single, coherent topic. Don't create a massive `EVERYTHING.md` file. Split it up logically (e.g., `schema.md`, `error_codes.md`, `style_guide.md`).
- **Clear Headings:** Use clear, hierarchical Markdown headings (`##`, `###`). Agents use headings to quickly navigate and find the exact piece of information they need when scanning files.
- **Provide "Why" and "How":** Don't just dump an API schema. Include snippets showing *how* to use the API and *why* certain parameters are required. Context is just as important as the facts.

## Linking References in SKILL.md
The agent must know the reference exists and when to read it. Link them clearly using Markdown syntax with relative paths from the skill directory root.

**Example in `SKILL.md`:**
```markdown
## Handling Errors
If the API returns a validation error, read **[API Errors](references/api_errors.md)** to find the exact resolution steps before retrying.

## Bundled Resources
- **[Database Schema](references/db_schema.yaml):** The source of truth for all database tables.
- **[Coding Style](references/style_guide.md):** Project-specific formatting rules.
```

*By explicitly stating "read [API Errors]", you provide a direct instruction for the agent to use its file-reading tool exactly when the condition is met, saving context window space during normal operations.*
