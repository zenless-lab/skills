# AI Agent Framework Locations & Configuration

Different AI agent tools expect their system prompts or instruction files to be located in specific paths or configured in specific ways. When a user requests to create instructions for a *specific* framework, use this guide to place the file correctly. If no framework is specified, default to `AGENTS.md` in the project root.

This reference also details whether specific frameworks natively scan for and parse `AGENTS.md` automatically.

## AGENTS.md (Standard / OpenCode / General)
- **Primary Location:** `AGENTS.md` (Root directory)
- **Alternative Locations:** `.github/AGENTS.md`, `docs/AGENTS.md` (less common, but supported by some parsers).
- **Usage:** A growing standard for project-level agent instructions.
- **Scans AGENTS.md Automatically?** Yes (Native).
- **Reference:** https://agents.md/

## GitHub Copilot
- **Primary Location:** `.github/copilot-instructions.md`
- **Alternative Locations:** Workspace-level `.vscode/copilot-instructions.md` (sometimes used in specific VS Code setups, though `.github` is standard).
- **Usage:** Custom instructions for GitHub Copilot Chat.
- **Scans AGENTS.md Automatically?** **No**. Copilot currently only automatically reads `.github/copilot-instructions.md` or settings defined in VS Code workspace settings. `AGENTS.md` would need to be manually referenced in chat.

## Cursor
- **Primary Location:** `.cursorrules` (Root directory)
- **Alternative Locations:** `.cursor/rules/*.mdc` (Cursor's newer format for multi-file rule definitions based on file paths).
- **Usage:** Instructions used by the Cursor IDE agent.
- **Scans AGENTS.md Automatically?** **No**. Cursor relies strictly on `.cursorrules` or `.cursor/rules/` directories. To use `AGENTS.md`, the `.cursorrules` file must explicitly instruct the agent to read `AGENTS.md`.

## Gemini CLI
- **Primary Location:** `GEMINI.md` (Root directory)
- **Alternative Locations:** Global memory (via `save_memory` tool), or specialized skills in `.agents/skills/`.
- **Usage:** Foundational mandates for the Gemini CLI agent. Takes absolute precedence over general workflows.
- **Scans AGENTS.md Automatically?** **Yes/Partial**. Gemini CLI will analyze the workspace and read `AGENTS.md` during its research phase if it exists, but `GEMINI.md` takes absolute priority for foundational behavioral mandates.

## Aider
- **Primary Location:** `.aider.conf.yml`
- **Alternative Locations:** `.aider.model.settings.yml`, or specific markdown files passed via CLI flags (e.g., `AIDER_RULES.md`).
- **Usage:** Settings and system prompts for Aider CLI.
- **Scans AGENTS.md Automatically?** **No**. Aider requires explicit configuration. You must set `message-file: AGENTS.md` in `.aider.conf.yml` or run Aider with `aider --message-file AGENTS.md` for it to read the file.

## Claude (Anthropic) / Claude Code
- **Primary Location:** `CLAUDE.md` (Root directory)
- **Alternative Locations:** Context files passed via CLI (if using Claude Code).
- **Usage:** General system prompt instructions for Claude when interacting with the codebase.
- **Scans AGENTS.md Automatically?** **No**. Claude Code natively looks for `CLAUDE.md`. It will not automatically adopt `AGENTS.md` unless told to do so by the user during the session.

## Cline / Roo Code (VS Code Extensions)
- **Primary Location:** `.clinerules` (for Cline) or `.roomd` (for Roo Code)
- **Alternative Locations:** Roo Code is known to also fall back to reading `.cursorrules` if `.roomd` is not present.
- **Usage:** Specific instructions for Cline or Roo Code agents.
- **Scans AGENTS.md Automatically?** **No**. They look for their specific hidden files.

## Windsurf
- **Primary Location:** `.windsurfrules` (Root directory)
- **Alternative Locations:** N/A.
- **Usage:** Instructions for the Windsurf IDE agent (Cascade).
- **Scans AGENTS.md Automatically?** **No**. Windsurf requires the specific `.windsurfrules` file.

## Best Practice for Cross-Compatibility
If a project wants to support multiple tools without duplicating context, the best practice is to create a comprehensive `AGENTS.md` file and then create symlinks or minimal configuration files for specific frameworks that simply say: *"Read the AGENTS.md file in the root directory for instructions."*
