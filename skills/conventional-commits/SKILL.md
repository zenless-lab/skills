---
name: conventional-commits
description: Standardize git commit messages using Conventional Commits 1.0.0 and 50/72 rules. Use when drafting messages for staged changes, formatting existing commits, or when requested to "commit", "write a message", or "fix commit style".
---

# Conventional Commits Workflow

Follow these steps to generate a professional git commit message.

## Core Mandates

*   **Respect Context:** If the project contains a `.gitmessage` file or the user provides specific instructions, prioritize them. Use `assets/gitmessage_template.txt` as a reference for formatting.
*   **50/72 Rule:** Title must be ≤ 50 characters. Separate body with a blank line. Wrap body lines at 72 characters.
*   **Grammar:** Use imperative mood and present tense for the title (e.g., "fix bug", "add feature"). Do not capitalize the first letter and do not use a period at the end.

## Implementation Steps

### 1. Analyze Changes & Decide Format
Read staged changes to determine the nature of the modification.
*   **Short Format:** Use for simple, self-explanatory changes. Reference `assets/short_template.txt`.
*   **Long Format:** Use for complex changes or when explicitly requested. Reference `assets/long_template.txt`.

### 2. Determine Type & Optional Scope
Select the correct type from the following: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
*   **Scope:** Do not include a scope unless the user explicitly requests one or the project convention requires it.

### 3. Identify Breaking Changes
Check for public API changes or major refactors.
*   Append `!` after the type/scope (e.g., `feat!: ...`).
*   If using Long Format, add `BREAKING CHANGE: <description>` to the footer.

### 4. Compose the Message
*   **Title:** `<type>[optional scope][!]: <description>`. Ensure it is ≤ 50 chars and lowercase.
*   **Body:** Focus on *what* and *why*. Ensure line length ≤ 72 chars.
*   **Footers:** Include mandatory tags (e.g., `Refs: #123`) or breaking change notes if applicable.

## Resources

*   **Templates:** See `assets/short_template.txt`, `assets/long_template.txt`, and `assets/gitmessage_template.txt`.
*   **Full Spec:** Refer to `references/specification.md` for complete Conventional Commits 1.0.0 rules.
