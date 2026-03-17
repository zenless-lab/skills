# Priority Rules and Scanning Paths

When managing AI instructions in modern, complex codebases (e.g., monorepos), multiple instruction files often exist. Different frameworks handle conflicting instructions and nested files using specific priority models.

## Hierarchical Scanning Logic (The "Proximity Principle")
Most frameworks apply a geographic proximity principle: instructions closer to the file being edited take precedence over global ones.
- **Root Directory (`AGENTS.md`)**: Act as global rules, usually always active for every session.
- **Subdirectories (e.g., `frontend/AGENTS.md`)**: Act as localized rules, applying only to files within that directory. This prevents context pollution (e.g., backend coding standards don't apply to frontend code).

## GitHub Copilot's Priority Model
GitHub Copilot employs a strict 3-tier weighting system:
1. **Personal Instructions (Highest Priority)**: Stored in user account settings or global config files. Applies across all projects.
2. **Repository Instructions**:
    - **Path-Specific Files**: e.g., `.github/instructions/api.instructions.md`. Targeted via glob matching, higher priority than generic repo files.
    - **General Repo Files**: `.github/copilot-instructions.md` or `AGENTS.md`.
3. **Organizational Instructions (Lowest Priority)**: Set by admins for the entire GitHub Org. Though lowest in priority, often enforced via mandatory CI/CD "Critic Agents".

## Cursor & Windsurf Priority Logic
- **Cursor**:
    - `.mdc` files inside `.cursor/rules/` are the highest priority, especially those flagged as "Always" or matched via specific globs to the active file.
    - Root `.cursorrules` provides baseline rules but is overwritten by matched `.mdc` rules.
    - Nested `AGENTS.md` files apply on a depth-first basis.
- **Windsurf (Cascade Engine)**:
    - Feeds all found `AGENTS.md` files into its rule engine.
    - Path proximity takes priority during conflicts. Merges rules for cross-directory tasks up to the context window limit.

## Gemini CLI's Hierarchical Memory
Gemini CLI processes rules in the following hierarchy:
1. **Explicit User Prompt (Highest)**: Real-time context overrides stored rules.
2. **Local `GEMINI.md`**: Found in the active working directory.
3. **Root `GEMINI.md`**: Provides the baseline mandates.
*(Note: If both `GEMINI.md` and `AGENTS.md` exist, `GEMINI.md` takes precedence).*
- **Memory Reload**: Can be updated on-the-fly using the `/memory refresh` command.

## Instruction Drift & Resolution
As instruction files grow, they can become a "Mudball" of contradictory rules. Use AI to resolve these issues.
- **Best Practice**: Periodically prompt the agent: *"Refactor my instruction file, identify and delete outdated, vague, or conflicting rules."*
