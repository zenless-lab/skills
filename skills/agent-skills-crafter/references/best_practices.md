# Best Practices for Skill Creators

## Writing Effective Descriptions (Discovery & Triggering)
Because agents use progressive disclosure, the `description` field in the frontmatter carries the entire burden of triggering. If it's poorly written, the skill will never be used.
- **Imperative phrasing:** Frame it as an instruction to the agent. "Use this skill when..." rather than "This skill does..."
- **Focus on user intent, not implementation:** Describe what the user is trying to achieve (e.g., "when the user wants to explore tabular data"), not the internal mechanics.
- **Be pushy:** Explicitly list contexts where the skill applies, including cases where the user doesn't name the domain directly (e.g., "even if they don't explicitly mention 'CSV' or 'analysis'").

## Ground in Real Expertise
- **No Role-Playing or Task Prompts:** A skill is a reference guide, not a persona assignment. Avoid phrases like "You are an expert developer..." or treating the skill as a direct task prompt. Focus entirely on providing the necessary domain knowledge, context, and structural rules.
- Extract skills from real hands-on tasks, execution traces, or project artifacts (internal docs, runbooks, code review comments).
- **Focus on what the agent lacks:** Add specific API usage, project conventions, and edge cases. Omit what the agent already knows (e.g., don't explain what a PDF is or how HTTP works).

## Provide Domain Knowledge, Not Just Manuals
- A skill serves to provide critical domain knowledge, not just a step-by-step procedure.
- **Explain the "why":** Giving reasons for an instruction allows the agent to make context-dependent decisions.
- **Favor generalized procedures:** Teach the agent how to approach a class of problems rather than what to produce for one specific instance.

## Instruction Patterns & Control
- **Provide defaults, not menus:** If multiple tools work, pick a default and provide an escape hatch.
- **Templates:** Use templates for exact output formats. Store large templates in `assets/`.
- **Checklists:** For multi-step tasks, provide an explicit progress checklist.
- **Validation Loops:** Instruct the agent to run a validator (a script or self-check) and fix issues before proceeding.
- **Plan-Validate-Execute:** For batch or destructive operations, tell the agent to create a structured plan, validate it against a source of truth, and execute once validated.

## Using Scripts
When the agent frequently rewrites the same helper logic, bundle a script in `scripts/`.
- **Avoid Interactive Prompts:** Agents run in non-interactive shells. Accept input via stdin or CLI flags.
- **Write Helpful Errors:** Output meaningful error messages to `stderr`.
- **Use Structured Output:** Prefer JSON, CSV, or TSV for `stdout`.
- **Python Scripts:** Use `uv run` and the PEP 723 specification (see `assets/script_template.py`) for zero-setup inline dependencies.
