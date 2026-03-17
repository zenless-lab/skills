---
name: agents-md-crafter
description: Use this skill when you need to create, update, or improve AI agent instruction files like AGENTS.md, GEMINI.md, or copilot-instructions.md. Trigger this anytime the user wants to set up standard AI rules, document project context for LLMs, or add repository-wide guidelines for AI agents.
---

# AGENTS.md Expert

This skill guides you through creating, modifying, updating, and improving `AGENTS.md` (or similar) files for a repository. These files act as a "README for AI agents," providing the specific, detailed context agents need to work effectively.

By default, if no specific framework is requested, you should create a highly compatible `AGENTS.md` file based on the provided template and the official https://agents.md/ specification.

## Workflow / Instructions

When asked to create or modify an `AGENTS.md` file, strictly follow these steps:

1. **Check for Existing Files:** List the root project directory to check if an agent guidance file (like `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursorrules`, etc.) already exists.
2. **Analyze File Structure:** Print the tree structure of the repository at an appropriate depth (e.g., using `tree -L 2` or equivalent python script/command) to gain a comprehensive understanding of the project's content, tech stack, and module organization. **Crucially:** Because a git repository is constantly changing, do not analyze the file structure too deeply. Focus on the modular structure.
3. **Scan for Instruction Drift:** Analyze existing instruction files for redundant, outdated, or conflicting rules ("mudballs"). Recommend a refactoring step if files are overly cluttered or contradictory.
4. **Formulate a Plan:** Based on your findings, formulate a plan to create or update the agent instruction file.
    - **Single Root File (Default):** By default, maintain a single, comprehensive `AGENTS.md` file in the root directory. Keep the root file minimal (preferably <100 lines) following the Progressive Disclosure principle.
    - **Conditional Progressive Disclosure:** If the file exceeds 500 lines or the project is exceptionally complex, split the file (e.g., using nested `AGENTS.md` or linking to sub-docs like `docs/DATABASE.md`).
    - **Multi-Framework Support:** If the user specifies multiple frameworks (e.g., Copilot, Claude Code, Cursor), implement the **Symlink Strategy** to use `AGENTS.md` as the Single Source of Truth (SSOT).
5. **Execution:** Create or modify the file based on your plan and the project context.

## Content Requirements for AGENTS.md

Ensure the generated `AGENTS.md` file contains the following key components based on the https://agents.md/ specification:
- **Project Context:** A brief summary of the project's purpose and tech stack.
- **Setup & Dev Environment:** Explicit commands for installing dependencies and building the project. Keep in mind that **agents may or may not have internet access**; rely on local context and installed dependencies where possible.
- **Code Style & Conventions:** Architectural patterns, stylistic preferences, and specific language settings.
- **Testing Instructions:** Commands to run tests, and explicit expectations that tests must pass before completing a task.
- **Language Preference:** Unless explicitly overridden by the user, state: **"Prioritize using English for code and comments."**
- **Git & PR Guidelines:** Unless the user specifies otherwise, enforce **Conventional Commits** (https://www.conventionalcommits.org/en/v1.0.0/) for git commit messages.

## Bundled Resources

- **[AGENTS.md Template](assets/agents_template.md):** The default, highly compatible template for `AGENTS.md`.
- **[Framework Locations](references/framework_locations.md):** A reference guide on where various agent frameworks expect their instruction files.
- **[Priority Rules](references/priority_rules.md):** Details on how different frameworks handle conflicting instructions and nested files.
- **[Progressive Disclosure Strategy](references/progressive_disclosure.md):** Guidelines for maintaining lean, hierarchical instruction sets.
