---
name: agents-md-crafter
description: Use this skill when you need to create, update, or improve AI agent instruction files like AGENTS.md, GEMINI.md, or copilot-instructions.md. Trigger this anytime the user wants to set up standard AI rules, document project context for LLMs, or add repository-wide guidelines for AI agents.
---

# AGENTS.md Expert

This skill guides you through creating, modifying, updating, and improving `AGENTS.md` (or similar) files for a repository. These files act as a "README for AI agents," providing the specific, detailed context agents need to work effectively.

By default, if no specific framework is requested, you should create a highly compatible `AGENTS.md` file based on the provided template and the official https://agents.md/ specification.

## Workflow / Instructions

When asked to create or modify an `AGENTS.md` file, strictly follow these steps:

1. **Check for Existing Files:** List the root project directory to check if an agent guidance file (like `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, etc.) already exists.
2. **Analyze File Structure:** Print the tree structure of the repository at an appropriate depth (e.g., using `tree -L 2` or equivalent python script/command) to gain a comprehensive understanding of the project's content, tech stack, and module organization. **Crucially:** Because a git repository is constantly changing, do not analyze the file structure too deeply. Focus on the modular structure.
3. **Formulate a Plan:** Based on your findings, formulate a plan to create or update the agent instruction file. Consider whether the project is a monorepo (which might benefit from nested `AGENTS.md` files in subdirectories).
4. **Execution:** Create or modify the file based on your plan and the project context.

## Content Requirements for AGENTS.md

Ensure the generated `AGENTS.md` file contains the following key components based on the https://agents.md/ specification:
- **Project Context:** A brief summary of the project's purpose and tech stack.
- **Setup & Dev Environment:** Explicit commands for installing dependencies and building the project. Keep in mind that **agents may or may not have internet access**; ensure core instructions don't strictly rely on external web searches unless necessary, and provide clear local commands and offline guidelines where applicable.
- **Code Style & Conventions:** Architectural patterns, stylistic preferences, and specific language settings.
- **Testing Instructions:** Commands to run tests, and explicit expectations that tests must pass before completing a task.
- **Language Preference:** Unless explicitly overridden by the user, state: **"Prioritize using English for code and comments."**
- **Git & PR Guidelines:** Unless the user specifies otherwise, enforce **Conventional Commits** (https://www.conventionalcommits.org/en/v1.0.0/) for git commit messages.

## Bundled Resources

- **[AGENTS.md Template](assets/agents_template.md):** The default, highly compatible template for `AGENTS.md`.
- **[Framework Locations](references/framework_locations.md):** A reference guide on where various agent frameworks expect their instruction files.
