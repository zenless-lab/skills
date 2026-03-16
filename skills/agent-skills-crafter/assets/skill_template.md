---
name: your-skill-name
description: Use this skill when... (Max 1024 chars. Focus on the user intent and be explicit about when this skill applies. Use imperative phrasing.)
---

# Your Skill Name

Brief overview of what this skill enables the agent to do.

## Context & Domain Knowledge
Provide the non-obvious context, architectural conventions, or domain knowledge the agent needs before acting. Do not explain basic concepts the agent already knows.
- [Project-specific convention 1]
- [Architectural fact 2]

## Workflow / Instructions
Outline the methodology. Use checklists or numbered steps for complex, multi-step procedures.

1. **Step 1:** Analyze the input and verify the state.
2. **Step 2:** Formulate a plan.
3. **Step 3:** Execute the operation using the provided scripts or standard tools.

   *Example: Running a bundled script via `uv run`:*
   ```bash
   uv run scripts/helper.py --input data.json
   ```

   *Example: Adding a dependency via `uv add`:*
   ```bash
   uv add requests bs4
   ```

## Troubleshooting & Edge Cases
- If the API returns a 400 status, check the schema in `references/schema.yaml`.
- Do not attempt to use `library-x`; always prefer `library-y`.

## Bundled Resources
List the available bundled files or external resources here so the agent can load them on demand.

- **[Data Schema](references/schema.yaml):** The source of truth for the data schema.
- **[Markdown Template](assets/template.md):** The markdown template to use for the final report.
- **[Helper Script](scripts/helper.py):** Validates and processes the data format.
- **[External API Docs](https://api.example.com/docs):** Remote documentation for the external service.
