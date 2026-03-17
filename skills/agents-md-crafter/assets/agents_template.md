# Agent Instructions

This file provides the necessary context, conventions, and instructions for AI agents operating in this repository. It follows the [AGENTS.md](https://agents.md/) standard.

## Project Context
- **Description:** [Brief summary of what the project does]
- **Language/Tech Stack:** [e.g., Python 3.10 / TypeScript, React, FastAPI]
- **Environment Notes:** Agents may sometimes operate in restricted environments without internet access. Rely on local context, installed dependencies, and provided commands whenever possible.

## Setup & Development Environment
Agents should use these commands to set up the environment and interact with the project:
- **Install Dependencies:**
  ```bash
  # [e.g., npm install / pip install -r requirements.txt]
  ```
- **Build Project:**
  ```bash
  # [e.g., npm run build]
  ```

## Code Style & Conventions
- **Language Preference:** Prioritize using English for all code, variable names, documentation, and comments.
- **Style Guidelines:** [e.g., "Follow PEP 8", "Use Prettier for formatting", "Use single quotes"]
- **Architecture:** [e.g., "Keep components stateless where possible", "Use repository pattern for database access"]
- **Code Quality:** Ensure all new code includes appropriate type hints (if applicable) and passes linting.

## Testing Instructions
All code changes must be verified. Agents must run tests to confirm their work before concluding a task.
- **Run Tests:**
  ```bash
  # [e.g., npm test / pytest]
  ```
- **Lint Code:**
  ```bash
  # [e.g., npm run lint / ruff check .]
  ```
- **Format Code:**
  ```bash
  # [e.g., npm run format / black .]
  ```

## Git & PR Guidelines
- **Commit Messages:** Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard (e.g., `feat: add new feature`, `fix: resolve bug`).
- **Pre-commit:** Always ensure code is formatted and tests pass before committing.

## References / Sub-Domain Instructions (Progressive Disclosure)
To keep context lean, specific architectural guidelines are located in their respective files. Agents should read these when working on relevant features:
- **Database Rules:** [docs/DATABASE.md](docs/DATABASE.md)
- **API Standards:** [docs/API.md](docs/API.md)

## Framework Specific Notes
[Add any specific notes for particular tools or agents used in this project.]
