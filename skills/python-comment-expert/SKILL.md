---
name: python-comment-expert
description: Use this skill when writing, reviewing, or modifying Python logic code comments (not docstrings). Trigger this even if the user only broadly asks to clean up or document complex Python logic. Load this skill when code changes affect existing comments to keep them synchronized.
---

# Python Comment Expert

This skill guides logic code comments (not docstrings) in Python.

## Core Rules (Must Follow)

1. **Explain "Why", Not "What"**: Provide context, reasons for decisions, or explain unintuitive behavior. Do not repeat what the code obviously does.
2. **Code Clarity First**: If code is self-explanatory, NO comment is needed. Do not use comments to hide bad code; refactor instead.
3. **Keep Sync**: If you modify code, you MUST update associated comments. Contradictory comments are worse than none.
4. **No Commented-out Code**: Remove commented-out code unless expected to be restored soon (e.g., temporary workarounds).

## Comment Types & Formats

- **Block Comments**: Indented to the same level as code. Start with `# ` (hash + space). Separate paragraphs with a single `#` line.
- **Inline Comments**: Use sparingly. Mainly for linters/scanners or extremely obscure lines (e.g., complex math).
- **Special Markers**: Use `TODO:`, `FIXME:`, `NOTE:`, `XXX:`, `HACK:`, `FAQ:` to communicate with the team.

## Deep Dive & Examples

- **Need detailed reasoning or philosophy?** Read [references/guidelines.md](references/guidelines.md)
- **Need to see concrete good/bad examples?** Read [assets/examples.py](assets/examples.py)
