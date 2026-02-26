---
name: skill-expert
description: Comprehensive master guide for designing, creating, editing, updating, and refactoring Agent Skills according to the official agentskills.io specification. Use this when you need to build or modify capabilities for an AI agent.
---
# Agent Skill Manager & Creator

Welcome to the Agent Skill Manager. This skill outlines the core philosophy and comprehensive guiding principles for building, editing, and maintaining high-quality, efficient, and modular Agent Skills.

## 🧠 Core Philosophy: Progressive Disclosure

The most critical principle of an Agent Skill is **Progressive Disclosure**. You must manage the agent's context window efficiently:

1. **Discovery**: Only `name` and `description` (YAML frontmatter) are loaded at startup. Keep them keyword-rich and highly descriptive.
2. **Activation**: This `SKILL.md` file is read upon task activation. It must remain under 500 lines and focus on *what* to do and *general rules*.
3. **Execution**: Detailed step-by-step guides, complex templates, and executable code MUST be offloaded to subdirectories and loaded *only on demand*.
   * **`references/`**: Detailed technical docs, step-by-step workflows, API references, or long-form domain instructions. Read only when specific guidance is needed.
   * **`assets/`**: Static resources like document templates, config templates, or data schemas.
   * **`scripts/`**: Executable code (e.g., Python or Bash). Scripts must be self-contained, provide clear error messages, and handle edge cases gracefully.

## 🏗️ Structural Principles

Every Agent Skill you create or refactor must adhere to these architectural standards:

* **Self-Contained Folder**: The skill lives in a directory matching the `name` in the frontmatter.
* **Mandatory SKILL.md**: This is the heart of the skill. It MUST contain compliant YAML frontmatter (`name`, `description`), followed by Markdown instructions.
* **Relative Referencing**: All internal links to auxiliary files (references/assets/scripts) MUST use relative paths from the skill root (e.g., `[Format Guide](references/format-guide.md)`).

## 📜 Formatting and Syntax Rules

* **Naming Constraints**: `name` must be 1-64 characters, restricted to lowercase alphanumeric and hyphens (`a-z`, `0-9`, `-`). Cannot start/end with a hyphen, nor contain consecutive hyphens.
* **Description Constraints**: `description` (1-1024 characters) must explicitly state what the skill does and *when* the agent should trigger it.
* **Script Standards & Execution Preference**:
  * Any Python scripts placed in the `scripts/` directory MUST follow the PEP 723 inline script metadata standard.
  * **CRITICAL**: If you generate a new skill that contains executable scripts, you MUST explicitly state in the generated `SKILL.md` that the agent should prefer using `uvx scripts/your_script.py` to ensure dependencies are automatically handled.

## 🌐 Official Specifications (On-Demand)

If you need to consult the raw official definitions and specs during creation or validation, access the following links:
* [Home](https://agentskills.io/home.md)
* [What are skills?](https://agentskills.io/what-are-skills.md)
* [Specification](https://agentskills.io/specification.md)
* [Integrate skills](https://agentskills.io/integrate-skills.md)

## 📚 Detailed Workflows & Guidelines (Load on Demand)

For specific execution steps and constraint checks, read the following files *only when performing a specific task*:

* [For the Standard Operating Procedure on creating/editing skills](references/step-by-step-workflow.md)
* [For YAML specifications](references/frontmatter-spec.md)
* For coding and documentation rules: 
  * [Script best practices](references/script-best-practices.md)
  * [Reference file best practices](references/reference-best-practices.md)
