# Agent Instructions

This file provides the necessary context, conventions, and instructions for AI agents operating in this repository. It follows the [AGENTS.md](https://agents.md/) standard.

## Project Context
- **Description:** A repository containing domain-specific skills, scripts, and documentation for AI Agents to use in various contexts (e.g., Python standards, LLM training, Secret Scanning, etc.).
- **Language/Tech Stack:** Markdown, Python, Shell, AI Agent configurations.
- **Environment Notes:** Agents should heavily rely on reading the provided `SKILL.md` files and reference documentation within each skill's directory when performing tasks related to those domains.

## Setup & Development Environment
- Most content consists of Markdown documentation, prompt templates, and Python utility scripts.
- Ensure any Python scripts are compatible with Python 3.

## Code Style & Conventions
- **Language Preference:** Prioritize using English for all documentation, skill configurations, code, variable names, and comments.
- **Skill Structure:** Each skill should follow the established directory structure containing `SKILL.md`, `assets/`, `references/`, and `scripts/`.
- **Skill Naming Conventions:**
  - **Action-Oriented (Default):** Typically, skill names should represent a concrete action (e.g., `secret-scan`) guiding how to execute or achieve a specific goal.
  - **Context-Providing Exceptions (`-crafter` & `-expert`):** Used for skills that primarily provide domain-specific context:
    - **`*-crafter`:** Provides concrete, practical help for specific tasks within a domain (e.g., how to craft and format a reST reference document).
    - **`*-expert`:** Provides higher-level, methodological context (e.g., determining the appropriate granularity for docstring comments or architectural patterns).
  - **Framework/Local Context (`*-knowledge` & `*-info`):** Used to provide localized context specific to a framework, application, or library. These are usually distributed alongside the codebase or library to offer plug-and-play context for users.
- **Markdown:** Maintain clean and consistent Markdown formatting. Use clear headings, bullet points, and code blocks where appropriate.
- **Code Quality:** Ensure all new Python scripts are properly formatted, include appropriate type hints, and follow general Python best practices (e.g., as guided by `python-standards` and `ruff-python-guide` within this repo).

## Git & PR Guidelines
- **Commit Messages:** Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard (e.g., `feat: add new agent skill`, `docs: update LLM training guide`).
- **Review:** Treat all `SKILL.md` updates critically, as they dictate the behavior of AI agents working across projects.

## Framework Specific Notes
- **VS Code Copilot Agents:** Agents operating in this repository should be aware that they are modifying instructions for other agents. Extreme care should be taken to ensure clarity, lack of ambiguity, and precise instructional prompt design.
