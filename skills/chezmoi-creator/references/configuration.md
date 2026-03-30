# Configuration

Use this reference when creating or reviewing `chezmoi.toml`, `chezmoi.yaml`, `chezmoi.json`, or `chezmoi.jsonc`. The purpose of configuration is to control local behavior and bootstrap context, not to hide the actual source-state design.

## What configuration should do

Good configuration answers questions like:

- where is the source state for this machine or repo?
- which editor and interpreters should chezmoi use?
- how should secrets be decrypted?
- what machine-local data should templates consume?

Bad configuration tries to replace source-state structure or duplicate template logic.

## High-value top-level settings

### `sourceDir`

Use `sourceDir` to tell chezmoi where the source state lives.

In a dedicated per-user setup, the default user source directory may be fine. In a project repository, explicitly setting `sourceDir` is safer.

Recommended repo-local pattern:

```yaml
sourceDir: ./src
workingTree: .
```

Why this is useful:

- repository metadata stays outside the managed source state
- `chezmoi add` and `chezmoi source-path` operate against the intended local repo

### `destDir`

Use `destDir` when the managed destination should not be the default home directory.

This is less common for personal dotfiles, but useful for:

- tests
- sandboxed migrations
- container-specific layouts

### `workingTree`

Use `workingTree` when the repo root and source state root are intentionally different.

This is important in the `src/` layout because repository operations still conceptually happen at the project root.

### `data`

Use `data` for machine-local template values.

Good examples:

- profile names
- email addresses
- host roles
- item IDs or vault names for secret lookups

Bad examples:

- long-lived plaintext secrets
- shared repo data that should be versioned in `.chezmoidata.*`

### `umask`

Use `umask` when default permission behavior must be adjusted consistently across applies.

This matters more in mixed OS or multi-user environments than in simple personal setups.

### `encryption`

Use this to declare the repository's encryption mechanism, typically `age` or GPG-backed workflows.

Set it explicitly when the repo manages encrypted files so bootstrap behavior is predictable.

## Editing behavior

chezmoi chooses an editor in this order:

1. `edit.command`
2. `VISUAL`
3. `EDITOR`
4. platform fallback

### `edit.command` and `edit.args`

Use these when the repo or environment requires a specific editor invocation.

Examples:

- launch `nvim`
- invoke VS Code with wait flags
- use a wrapper script in constrained environments

Example:

```toml
[edit]
    command = "code"
    args = ["--wait"]
```

### `edit.minDuration` and `edit.watch`

Use these when editor integration depends on file watchers or minimum edit windows.

These settings matter in GUI editor workflows more than terminal-only flows.

## Interpreters

Use `interpreters` to map file extensions to execution commands, especially when default OS behavior is inconsistent.

Typical cases:

- `.ps1` -> `pwsh` or `powershell`
- `.py` -> `python3`
- `.rb` -> pinned ruby interpreter

Example:

```toml
[interpreters.ps1]
    command = "pwsh"
```

Why this matters:

script portability often fails because the wrong interpreter is assumed, especially on Windows.

## Git integration

### `git.autoCommit`

Use this only when the source-state repo workflow explicitly wants automatic commits.

It can be useful for tightly controlled personal flows, but it is usually too implicit for shared repositories.

### `git.autoPush`

Use this only when automatic remote pushes are genuinely intended. In most collaborative or audited environments, this is too aggressive.

### `git.commitMessageTemplate`

Use this when automatic or semi-automatic commits need consistent structure.

This is more useful than `autoPush` in most teams because it improves traceability without forcing remote side effects.

## Encryption and merge tooling

### Age and GPG settings

Common keys:

- `age.identity`
- `age.recipient`
- `gpg.recipient`
- `gpg.args`

Use these when the repo manages encrypted source-state files.

Prefer age for new setups unless the environment already standardizes on GPG.

### Diff and merge customization

Common keys:

- `diff.command`
- `merge.command`
- `textconv`

Use these when:

- opaque formats need normalization before diffing
- repo policy requires custom diff behavior
- merge conflicts are easier to resolve through external tooling

Example use of `textconv`:

convert a structured or generated file into a readable text form before comparing changes.

## Practical configuration examples

### Repo-local project layout

```yaml
sourceDir: ./src
workingTree: .
data:
  profile: work
  codespaces: false
```

Use this when the repository contains docs, CI, and helper scripts alongside the source state.

### Windows-friendly script execution

```toml
[interpreters.ps1]
    command = "pwsh"

[edit]
    command = "code"
    args = ["--wait"]
```

Use this when PowerShell scripts and GUI editing are part of the workflow.

## Common mistakes

- storing secrets directly in `data`
- using config to model shared repo structure that belongs in source-state files
- omitting explicit interpreter mappings in mixed-platform repos
- relying on implicit default source directories in project-local workflows
- enabling auto-push without an intentional workflow for it

## Rule of thumb

If a value is:

- shared and safe to commit -> source state or `.chezmoidata.*`
- machine-specific and non-secret -> config `data`
- secret -> password manager or encrypted source-state file

Configuration should clarify machine-local behavior, not conceal design decisions.
