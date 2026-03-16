# Guide: Creating Scripts for Skills

When a skill requires executing complex tool chains, parsing difficult formats, or reusing logic, it is highly recommended to bundle self-contained scripts in the `scripts/` directory.

## Core Design Principles for Agentic Scripts
Agents are not human users. They run commands in non-interactive shells and rely entirely on `stdout` and `stderr` to understand what happened.
- **No Interactive Prompts:** An agent will hang indefinitely if a script blocks for interactive input (e.g., `input("Enter name: ")`). All inputs must be passed via CLI arguments, environment variables, or `stdin`.
- **Write Helpful Errors (`stderr`):** If a script fails, a generic "Error" wastes the agent's turn. Output specific error messages to `stderr` detailing what failed, why, and what the valid options are.
- **Output Structured Data (`stdout`):** Prefer outputting JSON, CSV, or TSV. Structured data is unambiguous and easy for the agent to parse programmatically.
- **Document Usage (`--help`):** Include a clear description, flag options, and examples in the script's `--help` output so the agent can learn its interface on the fly.

## Self-Contained Dependencies
Scripts should not require complex environment setup. Use tools that auto-resolve dependencies.

### Python (Preferred)
Use `uv run` and the **PEP 723** specification to declare dependencies inline. The agent can run it with a single command without creating virtual environments manually.
```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
```
*Note: You can copy the boilerplate from `assets/script_template.py`.*

### Other Languages
- **Node.js:** Use `npx <package>` or `npx tsx script.ts` for zero-install execution.
- **Bash:** Keep scripts standard and avoid requiring globally installed non-standard binaries unless explicitly declared in the skill's `compatibility` frontmatter.

## Referencing Scripts in SKILL.md
Always use relative paths from the root of the skill directory when instructing the agent to run a script.
```markdown
Run the data processor:
`uv run scripts/process_data.py --input data.json`
```
