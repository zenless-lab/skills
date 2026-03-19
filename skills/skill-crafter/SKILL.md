---
name: skill-crafter
description: Use this skill when you need to create, edit, evaluate, or improve Agent Skills. Trigger this even if the user just asks to build a new agent workflow, refine an existing AI capability, write support scripts for an agent, or optimize prompt descriptions and outputs.
---

# Skill Crafter

Agent Skills are lightweight, open formats for extending AI agent capabilities with specialized knowledge and workflows. This document serves as a reference for the domain knowledge, architectural standards, and procedural guidelines required to create or modify Agent Skills effectively.

## Core Principles

1. **Discovery is Paramount (The Description):** Agents use progressive disclosure. They only read the `name` and `description` to decide whether to activate a skill. Writing a highly optimized, intent-focused description is the most universally critical step in skill creation.
2. **Progressive Disclosure:** Keep `SKILL.md` concise (< 5000 tokens). Move detailed reference material to `references/` and large templates/assets to `assets/`.
3. **Domain Knowledge:** Skills encapsulate procedural knowledge and rich context (e.g., project conventions, edge cases). Provide the "why" so the agent makes context-dependent decisions.
4. **Eval-driven Iteration:** Systematically test both whether the skill triggers (Trigger Rates) and whether it produces good results (Output Quality).
5. **Scripting:** Bundle reusable scripts in `scripts/`. Python scripts MUST follow PEP 723 inline dependency standards and be designed for non-interactive agent execution via `uv run`.

## Skill Creation Workflow Guidelines

### Defining Scope & Trigger (Frontmatter)
- **Determine the Scope:** Focus on what the agent wouldn't know on its own.
- **Scaffold:** Create the directory (`skill-name/SKILL.md`). The template `assets/skill_template.md` can be used.
- **Optimize the Description:** Because agents use progressive disclosure, the `description` field determines whether a skill is triggered. Follow these key techniques:
  - **Imperative phrasing:** Frame it as an instruction directly to the agent (e.g., "Use this skill when...").
  - **Focus on user intent:** Describe what the user is trying to achieve, not the internal mechanics.
  - **Be pushy:** Explicitly list contexts where the skill applies, including cases where the user doesn't explicitly name the domain.
  - Read [Best Practices](references/best_practices.md) for more details.

### Structuring Skill Instructions
- Consult **[Best Practices](references/best_practices.md)** for guidelines on phrasing, providing defaults, and building workflows.
- **Managing Context:** For large contextual data, conditional edge cases, or schemas, consult **[References](references/references.md)** on how to correctly offload them into the `references/` directory to save token context.
- Use explicit Checklists for multi-step workflows.
- For destructive or batch operations, suggest a Plan-Validate-Execute loop.

### Bundling Scripts
- If a skill requires running complex commands or reusable helper logic, bundle a self-contained script in `scripts/`.
- Consult **[Scripts](references/scripts.md)** for core design principles on making scripts robust and agent-friendly.
- **For Python:** ALWAYS use the PEP 723 script template **[Script Template](assets/script_template.py)**.
- Scripts MUST NOT have interactive prompts. Ensure clear `--help`, helpful stderr messages, and structured `stdout` (JSON, CSV).

### Evaluating & Iterating
- Consult [Evaluation & Iteration](references/evaluation.md) to test **Trigger Rates** (does the description work?) and **Output Quality** (do the instructions/scripts work?).
- Iterate on the `description` or `SKILL.md` instructions based on test results.

## Bundled Resources

- **[Specification](references/specification.md):** Strict formatting rules.
- **[Best Practices](references/best_practices.md):** Writing descriptions, scoping, context, and scripting.
- **[Evaluation & Iteration](references/evaluation.md):** Testing trigger rates and grading output quality.
- **[Scripts](references/scripts.md):** Core principles for writing agent-friendly scripts.
- **[References](references/references.md):** How to structure and link external context.
- **[SKILL.md Template](assets/skill_template.md):** Boilerplate for new skills.
- **[Python Script Template](assets/script_template.py):** Boilerplate for PEP 723 Python scripts.
