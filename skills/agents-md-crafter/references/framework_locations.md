# AI Agent Framework Locations & Configuration

Different AI agent tools expect their system prompts or instruction files to be located in specific paths or configured in specific ways. When a user requests to create instructions for a *specific* framework, use this guide to place the file correctly. If no framework is specified, default to `AGENTS.md` in the project root.

This reference also details whether specific frameworks natively scan for and parse `AGENTS.md` automatically.

## AGENTS.md (Universal Standard / OpenCode)
- **Primary Location:** `AGENTS.md` (Root directory)
- **Alternative Locations:** `.github/AGENTS.md`, `docs/AGENTS.md` (less common, but supported by some parsers).
- **Usage:** The universal standard for project-level agent instructions, natively supported by OpenCode, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Windsurf, Aider, and Zed.
- **Scans AGENTS.md Automatically?** **Yes** (Native).
- **Reference:** https://agents.md/
- **OpenCode Note:** OpenCode's `/init` command can generate an initial `AGENTS.md` by scanning the project up to the root. In GitHub Actions, it dynamically loads instruction segments based on PR diff paths.

## GitHub Copilot
- **Primary Locations:** `.github/copilot-instructions.md`, `AGENTS.md`, or specific path files like `.github/instructions/*.instructions.md`
- **Usage:** Custom instructions for GitHub Copilot Chat, focusing on organizational and repository-level guidelines.
- **Scans AGENTS.md Automatically?** **Yes**.
- **Environment Extensions:** Supports extra scan paths via `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` environment variable.

## Cursor
- **Primary Locations:** `.cursor/rules/*.mdc` (Directory of Rules) or `.cursorrules` (Root directory)
- **Usage:** Instructions used by the Cursor IDE agent. The modern `.mdc` format supports complex activation modes (Always on, Auto-attach via Glob, Manual trigger).
- **Scans AGENTS.md Automatically?** **Yes**. Cursor scans nested `AGENTS.md` using a depth-first principle.

## Windsurf
- **Primary Location:** `.windsurfrules` (Root directory) or `AGENTS.md`
- **Usage:** Instructions for the Windsurf IDE agent (Cascade engine).
- **Scans AGENTS.md Automatically?** **Yes**. Windsurf's Cascade engine scans the entire workspace: root `AGENTS.md` is always on, and sub-directory `AGENTS.md` files are applied locally via Glob matching.

## Gemini CLI
- **Primary Location:** `GEMINI.md` (Root directory or nested)
- **Usage:** Foundational mandates for the Gemini CLI agent. Gemini CLI uses a hierarchical memory system where local `GEMINI.md` files override root ones, and explicit prompts override all.
- **Scans AGENTS.md Automatically?** **Yes**. Gemini CLI will analyze the workspace and read `AGENTS.md` during its research phase if it exists, but `GEMINI.md` takes absolute priority for foundational behavioral mandates.

## Claude (Anthropic) / Claude Code
- **Primary Location:** `CLAUDE.md` (Root directory)
- **Usage:** System prompt instructions for Claude when interacting with the codebase. Claude Code features an `@imports` system, allowing it to load specific reference docs (e.g., `docs/DATABASE.md`) on-demand.
- **Scans AGENTS.md Automatically?** **Yes**. Claude Code natively looks for `CLAUDE.md` and also supports `AGENTS.md`. Global preferences can be set in `~/.claude/CLAUDE.md`.

## Aider
- **Primary Location:** `.aider.conf.yml`
- **Alternative Locations:** `.aider.model.settings.yml`, or specific markdown files passed via CLI flags (e.g., `AIDER_RULES.md`).
- **Usage:** Settings and system prompts for Aider CLI.
- **Scans AGENTS.md Automatically?** **Yes** (recent versions added support). To be safe, configure explicit support in `.aider.conf.yml` with `message-file: AGENTS.md`.

## Cline / Roo Code (VS Code Extensions)
- **Primary Location:** `.clinerules` (for Cline) or `.roomd` (for Roo Code)
- **Usage:** Specific instructions for Cline or Roo Code agents.
- **Scans AGENTS.md Automatically?** **Yes**.

## Best Practice: The Symlink Hack for Cross-Compatibility
Because the tool ecosystem is fragmented, developers often maintain identical configuration files for different tools. The recommended best practice is:
1. Use `AGENTS.md` as the **Single Source of Truth** (SSOT).
2. Create symlinks for framework-specific files (e.g., `.github/copilot-instructions.md`, `CLAUDE.md`, `.cursorrules`) pointing to the root `AGENTS.md`.
This ensures consistent agent behavior across the entire team, regardless of which tool each developer uses.
