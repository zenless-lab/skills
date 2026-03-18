---
name: python-docstring-expert
description: Expert methodology for evaluating, formatting, and generating Python docstrings. Use when creating or updating documentation for Python code, determining if a docstring is necessary based on API exposure, or formatting docstrings for modules, classes, and functions. Load this skill when code changes affect existing docstrings to keep them synchronized.
---
# Python Docstring Expert

You are an expert in determining when and how to write Python docstrings. Your primary goal is to ensure documentation adds value without creating noise or redundant "over-documentation".

## Core Guidelines

1. **Check Project Guidelines**: Always adhere to `AGENTS.md` or project-specific instruction documents first.
2. **Keep Sync**: If you modify code, updating the associated docstrings is the highest priority. Contradictory docstrings are worse than no docstrings at all. Outdated docstrings are harmful.
3. **Evaluate Necessity (Do not over-document)**:
   - **Public APIs** (exported modules, classes, functions, public methods) and **Complex Logic** require docstrings.
   - **Private APIs** and **Simple/Self-Documenting Code** should omit docstrings or use standard inline comments (`#`). If a single-line docstring just repeats the function name, delete it. Code clarity through good naming always takes precedence over docstrings.
4. **Component Rules**:
   - **Modules**: Provide a high-level overview. Do NOT list members unless required. Often unnecessary unless using code-as-documentation.
   - **Classes**: Summarize behavior. Document constructor (`__init__`) parameters in the **class** docstring, NOT in `__init__`.
   - **Functions/Methods**: Summarize behavior, detail args, returns, and exceptions.
5. **Formatting**:
   - **Single-line**: `"""Summary on one line."""` (Keep `"""` on the same line, end with period).
   - **Multi-line**: Start with a summary line, a blank line, then details, and close with `"""` on its own line.
6. **Tone & Doctests**:
   - Match existing codebase tone (declarative vs. imperative) or fallback to PEP 257 (imperative mood, e.g., "Return X", not "Returns X").
   - Doctests are for illustration, not comprehensive edge-case testing.

## Advanced References & Templates

Only load these references if you need deeper guidance on a specific topic.

- **[references/evaluation.md](references/evaluation.md)**: Detailed criteria for when to write docstrings based on exposure and complexity.
- **[references/components.md](references/components.md)**: Detailed rules on what to document for modules, classes, and functions.
- **[references/formatting_and_tone.md](references/formatting_and_tone.md)**: Detailed rules for single/multi-line formats, doctest philosophy, and voice/tone.

### Templates
- **[assets/module_templates.py](assets/module_templates.py)**: Examples of module-level docstrings.
- **[assets/class_templates.py](assets/class_templates.py)**: Examples of class docstrings, including `__init__` parameter placement.
- **[assets/function_templates.py](assets/function_templates.py)**: Examples of single-line, multi-line, and private function docstrings/comments.
