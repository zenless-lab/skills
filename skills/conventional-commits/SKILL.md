---
name: conventional-commits
description: Standardize git commit messages using Conventional Commits 1.0.0, project-specific conventions, and 50/72 rules. Use when drafting messages for staged changes, formatting existing commits, creating commit message templates, or when requested to "commit", "write a message", or "fix commit style".
---

# Conventional Commits Workflow

Follow these steps to generate a project-aligned git commit message.

## Core Mandates

*   **Respect Local Context First:** Before drafting anything, inspect explicit user instructions, `.gitmessage`, `commitlint.config.*`, `.commitlintrc*`, `package.json` commitlint settings, `CONTRIBUTING.md`, `AGENTS.md`, and similar repository guidance. Treat hard validation and explicit user direction as higher priority than generic defaults.
*   **Match Repository History:** Review recent commit history before drafting so the message matches the repository's existing type casing, scope usage, footer conventions, and scope granularity.
*   **50/72 Rule:** Title must be ≤ 50 characters. Separate body with a blank line. Wrap body lines at 72 characters.
*   **Grammar:** Use imperative mood and present tense for the title (e.g., "fix bug", "add feature"). Do not capitalize the first letter and do not use a period at the end.
*   **Explain Why, Not How:** The diff already shows implementation details. If a body is needed, use it to explain why the change exists, what problem it solves, and any notable consequences, tradeoffs, or side effects.
*   **Prefer Determinism:** When multiple labels seem plausible, apply the priority rules below and stop at the first matching rule. If the staged changes truly represent multiple unrelated intentions, recommend splitting the commit instead of inventing a hybrid label.

## Implementation Steps

### 1. Collect Project Context
Inspect local rules before classifying the change.
*   Read explicit user instructions first.
*   Inspect `.gitmessage`, `commitlint.config.*`, `.commitlintrc*`, `package.json`, `CONTRIBUTING.md`, `AGENTS.md`, and adjacent commit-message guidance if they exist.
*   Review recent commit history, and prefer recent commits in the same subsystem when possible.
*   Infer whether scope is customary, forbidden, or required, and what granularity the repository uses when scope appears.

If local rules conflict, use this precedence order:
1. Explicit user instruction.
2. Hard project validation or enforced configuration.
3. Repository documentation and agent instructions.
4. Recent repository history.
5. This skill's defaults.

### 2. Analyze Changes & Decide Format
Read staged changes to determine the nature of the modification.
*   **Short Format:** Use when one line is enough to preserve the intent of the change. This is the default. Reference `assets/short_template.txt`.
*   **Long Format:** Use only when the rationale, constraints, or consequences would be unclear or lost in a single line, or when the user explicitly requests it. Reference `assets/long_template.txt`.

Use this checklist before moving from Short Format to Long Format:

- [ ] The title alone would leave the reason for the change unclear.
- [ ] The diff does not show important background, a tradeoff, a risk, or a consequence.
- [ ] A future reader should not miss a warning, limitation, or migration note.

Check these questions in order:
1. Would the title alone leave the reason for the change unclear?
2. Is there non-obvious background, a tradeoff, a risk, or a consequence that the diff does not show?
3. Is there a warning, limitation, or migration note a future reader should not miss?

If all answers are No, use Short Format. If any answer is Yes, use Long Format.

### 3. Determine Type Using Priority Order
Classify the commit by answering these questions from top to bottom. The first `Yes` decides the type. Do not keep scanning once a rule matches.

1. **Does the commit add a new capability, endpoint, command, option, UI flow, or other behavior that did not exist before?**
	*   **Yes:** use `feat`.
	*   Use `feat` ONLY when the primary effect is adding capability.
	*   Do not downgrade to `refactor` or `chore` when new behavior is introduced.
2. **Does the commit correct wrong behavior, a regression, a defect, a crash, incorrect output, a broken integration, or another bug?**
	*   **Yes:** use `fix`.
	*   Use `fix` ONLY when behavior was incorrect before the change and is corrected after the change.
	*   Do not use `refactor` when the commit fixes externally observable incorrect behavior.
3. **Does the commit primarily improve performance WITHOUT intentionally changing behavior or adding features?**
	*   **Yes:** use `perf`.
	*   Use `perf` ONLY when performance is the reason for the change.
	*   Do not use `refactor` when performance improvement is the primary intent.
4. **Does the commit change documentation ONLY, WITHOUT changing runtime code, tests, build files, or generated behavior?**
	*   **Yes:** use `docs`.
5. **Does the commit change formatting, whitespace, naming style, or lint-driven presentation ONLY, WITHOUT changing behavior, documentation meaning, tests, or build configuration?**
	*   **Yes:** use `style`.
6. **Does the commit restructure existing code WITHOUT changing externally observable behavior and WITHOUT performance as the primary goal?**
	*   **Yes:** use `refactor`.
	*   Use `refactor` ONLY for internal restructuring.
	*   Do not use `refactor` if `fix`, `feat`, or `perf` already matched.
7. **Does the commit add, remove, or rewrite tests ONLY, WITHOUT changing production behavior, build tooling, or CI workflows?**
	*   **Yes:** use `test`.
8. **Does the commit change build, packaging, dependency resolution, release tooling, compiler configuration, bundler configuration, or artifact generation?**
	*   **Yes:** use `build`.
	*   Use `build` ONLY for mechanics required to build, package, or release the project.
	*   Do not use `chore` when `build` applies.
9. **Does the commit change CI/CD workflows, hosted automation, pipeline definitions, or status-check orchestration?**
	*   **Yes:** use `ci`.
	*   Use `ci` ONLY for automation executed by CI/CD systems.
10. **If none of the rules above match, use `chore`.**
	*   Use `chore` ONLY as the fallback bucket.
	*   Do not use `chore` for changes that fit `build`, `ci`, `docs`, `test`, `style`, `refactor`, `perf`, `fix`, or `feat`.

### 4. Determine Scope Using Priority Order
Decide whether to include a scope by applying these rules in order.

1. **Obey explicit requirements first.**
	*   If the user explicitly requires a scope, use one.
	*   If the user explicitly forbids a scope, omit it unless a hard project rule would reject the commit.
	*   If project configuration or validation requires a scope, use the exact style that configuration expects.
2. **Match repository history second.**
	*   If recent history consistently uses scopes, keep using them.
	*   Match the repository's historical granularity. If history uses package names, keep package names. If history uses top-level areas like `api` or `docs`, do not invent finer scopes.
	*   If recent history consistently omits scopes, omit the scope unless rule 1 or rule 3 applies.
3. **Default to scope in a clear monorepo.**
	*   If the repository is a mono-repo or multi-package workspace and higher-priority rules do not decide otherwise, use a scope by default.
	*   Treat the repository as a clear monorepo when workspace manifests, multi-package tooling, or stable top-level package directories make package boundaries explicit.
	*   Prefer stable units such as package, app, service, crate, module, or workspace names over transient file names.
4. **Default to no scope when evidence is weak.**
	*   If no explicit rule exists, history is mixed or unavailable, or the correct granularity cannot be determined confidently, omit the scope.

### 5. Identify Breaking Changes
Check for public API changes or major refactors.
*   Append `!` after the type/scope (e.g., `feat!: ...`).
*   If using Long Format, add `BREAKING CHANGE: <description>` to the footer.

### 6. Compose the Message
*   **Title:** `<type>[optional scope][!]: <description>`. Ensure it is ≤ 50 chars and lowercase.
*   **Body:** Only include one when it adds context the diff cannot. When present, separate it from the title with a blank line and wrap each line at 72 characters. Focus on why the change was necessary, what problem it resolves, and any meaningful side effects, limitations, or migration notes. Do not narrate the implementation unless the implementation choice itself is the important reason.
*   **Footers:** Include mandatory tags (e.g., `Refs: #123`) or breaking change notes if applicable.

When writing a body, prefer answering these prompts:
*   Why was this change needed now?
*   What bug, risk, limitation, or maintenance problem does it address?
*   Are there side effects, compatibility implications, or follow-up expectations?

Avoid body lines that merely restate the patch, list edited files, or describe step-by-step how the code was changed.

## Self-Check

Before finalizing, verify the message passes this review:

- [ ] **Background is clear:** A reader six months later can still understand why the code was added, changed, or removed.
- [ ] **Intent is explained when needed:** Architectural, dependency, product, or operational reasons are captured only when they are not already obvious from the code and title.
- [ ] **Consequences are noted when relevant:** Breaking changes, risks, side effects, or rollout concerns are called out when they exist.
- [ ] **Format is justified:** The message stays one line unless extra context materially improves understanding.
- [ ] **The diff is not paraphrased:** The message adds intent and context instead of repeating how the implementation works.

## Message Template
When the user asks for a reusable message template, create it from the bundled assets and then adapt it to local conventions.
*   Use `assets/gitmessage_template.txt` as a base `.gitmessage`-style template and editor-integrated commit template.
*   Apply explicit user requirements first, then `AGENTS.md` and repository guidance, then recent history and established formatting habits.
*   Preserve the repository's preferred type casing, scope style, footer names, and expected section order.

## Resources

*   **Templates:** See `assets/short_template.txt`, `assets/long_template.txt`, and `assets/gitmessage_template.txt`.
*   **Full Spec:** Refer to `references/specification.md` for complete Conventional Commits 1.0.0 rules.
