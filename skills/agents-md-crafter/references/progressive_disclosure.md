# Progressive Disclosure Strategy

AI context windows, while growing, are not infinite, and providing too much irrelevant information degrades an agent's reasoning capabilities.
The 2026 standard for managing instruction sets is **Progressive Disclosure**: only feed the AI what it needs for the current task.

## The Instruction "Mudball"
As AI instructions are updated over months, they accumulate "mudball" rules—outdated, highly specific, and often conflicting snippets.
- Over-lengthy root instruction files (e.g., >500 lines) cause "context pollution", slowing down the AI and increasing the chance of hallucination.

## Best Practices for Progressive Disclosure

1. **Minimize the Root File**: Keep the root `AGENTS.md` short (ideally under 100 lines). It should contain only:
    - High-level project description.
    - Setup and build commands.
    - Links to other relevant standard documents.
2. **Use Sub-directory Files**: Create scoped `AGENTS.md` files in sub-directories to apply rules only where relevant.
3. **Use the `@imports` System**: Tools like Claude Code support `@imports` in `CLAUDE.md`, allowing the AI to dynamically load documents (e.g., `docs/DATABASE.md`) only when working on related tasks.
4. **Use Standard Markdown Links**: Even if tools don't natively support `@imports`, most modern agents can read external Markdown links if instructed to do so when relevant.
    - *Example*: "For database architecture rules, please refer to [Database Conventions](docs/architecture/database.md)."
5. **Implement Critic Agents**: Use specialized agents or prompts to routinely clean up your instruction files.
    - *"Refactor my instruction file, identify and delete outdated, vague, or conflicting rules."*

By strictly following progressive disclosure, developers ensure high-signal AI interactions, increasing the efficiency and accuracy of multi-agent and autonomous workflows.
