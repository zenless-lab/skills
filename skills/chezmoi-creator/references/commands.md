# Commands

Use this reference when the user asks how to initialize, inspect, test, migrate, or debug a chezmoi repository. The point is not to memorize command names. The point is to know which command answers which question.

## The core workflow in practice

Most real work falls into this loop:

1. Import or edit the source state.
2. Inspect the rendered result.
3. Diff before apply.
4. Apply narrowly or broadly.
5. Verify the result.

The commands below are grouped by the problem they solve.

## Start or connect a source state

### `chezmoi init [repo]`

Use `init` when you are starting a new source directory or cloning an existing dotfiles repo.

Common use cases:

- first-time bootstrap on a new machine
- initialize from a remote git repo
- initialize from an explicit local source directory during Codespaces bootstrap

Example:

```sh
chezmoi init --apply --source "$PWD/src"
```

Why this matters:

- `init` decides which source directory chezmoi will treat as canonical
- when working inside a project repo, passing an explicit `--source` avoids accidentally using the default user source directory

## Bring an existing file under management

### `chezmoi add [target]...`

Use `add` when the file already exists in the working tree and you want chezmoi to derive the correct source-state representation for you.

Example:

```sh
chezmoi add ~/.zshrc
chezmoi add --template ~/.gitconfig
chezmoi add --encrypt ~/.ssh/id_ed25519
```

Why this is usually better than hand-creating source-state files:

- chezmoi chooses the initial mapping correctly
- it reduces filename-encoding mistakes
- it preserves the current target content as the starting point

Use `--template` when the file should immediately become a template. Use `--encrypt` when the managed unit is a secret file.

## Edit what chezmoi manages

### `chezmoi edit [target]...`

Use `edit` when you want to change the source-state version of a target without manually locating its encoded filename.

Example:

```sh
chezmoi edit ~/.config/starship.toml
```

This is especially useful once filenames become encoded with `dot_`, `private_`, `encrypted_`, or `.tmpl`.

### `chezmoi chattr`

Use `chattr` when the behavior of the source-state entry should change but the logical target stays the same.

Common cases:

- convert a plain file into a template
- mark a file private
- mark a script executable

Example:

```sh
chezmoi chattr +template ~/.gitconfig
chezmoi chattr +private ~/.ssh/config
```

Why use it:

- avoids manual rename mistakes
- keeps attribute changes explicit and reversible

## Inspect what chezmoi thinks

### `chezmoi source-path [target]...`

Use this when you know the destination path and want to know which source-state entry backs it.

Example:

```sh
chezmoi source-path ~/.gitconfig
```

This is the fastest way to debug naming confusion.

### `chezmoi target-path [source-path]...`

Use this when you have a source-state file and want to verify what destination path it will produce.

Example:

```sh
chezmoi target-path dot_config/nvim/init.lua.tmpl
```

### `chezmoi cat [target]...`

Use `cat` when you want to inspect the fully rendered content of a target file.

Example:

```sh
chezmoi cat ~/.gitconfig
```

This is the right command when the file exists but contains the wrong rendered values.

### `chezmoi dump [target]...`

Use `dump` when you want structured inspection rather than plain text content.

This is more useful for tooling, diagnostics, and understanding metadata than for everyday file editing.

### `chezmoi data`

Use this when a template rendered with the wrong OS branch, hostname branch, or machine-specific value.

It answers: "What data did the template actually see?"

### `chezmoi cat-config` and `chezmoi dump-config`

Use these when a config setting seems ignored.

- `cat-config` shows the active config text
- `dump-config` shows parsed config values

The parsed view is often the faster way to catch type or merge mistakes.

## Preview changes safely

### `chezmoi diff [target]...`

Use `diff` before `apply`, especially after editing templates, scripts, externals, or secret flows.

Example:

```sh
chezmoi diff
chezmoi diff ~/.ssh/config
```

This is the main safety valve in everyday use.

### `chezmoi status`

Use `status` for a quick high-level answer to: "What managed files differ right now?"

It is less detailed than `diff`, but faster to scan.

### `chezmoi verify [target]...`

Use `verify` after apply when you want an explicit integrity check.

This is useful in scripts, CI-like checks, or after a large migration.

## Apply changes

### `chezmoi apply [target]...`

Use `apply` to write the computed target state to the destination tree.

Prefer narrow applies while iterating:

```sh
chezmoi apply ~/.gitconfig
```

Prefer full applies once the design is stable:

```sh
chezmoi apply
```

Narrow applies reduce blast radius while debugging.

### `chezmoi update`

Use `update` when the source state lives in a git repo and you want the standard pull-and-apply workflow.

It is the operational command for "sync this machine with the latest dotfiles repo".

## Work with config and init-time prompts

### `chezmoi edit-config`

Use this to edit machine-local config safely.

This is where per-host values belong, not inside shared source-state files.

### `chezmoi edit-config-template`

Use this when the bootstrap-time config template itself needs to change.

This is not for day-to-day dotfile edits. It is for changing what happens during `chezmoi init`.

### `chezmoi execute-template`

Use this to test template expressions in isolation.

Example:

```sh
printf '{{ .chezmoi.os }}\n' | chezmoi execute-template
```

This is useful when the question is "does the template expression work at all?" before it is embedded into a larger file.

## Diagnose environment and scope problems

### `chezmoi doctor`

Use `doctor` when behavior varies by machine and you suspect environment, interpreter, or dependency issues.

Typical reasons:

- password-manager CLI missing
- wrong shell or editor resolution
- interpreter mismatch on Windows

### `chezmoi managed` and `chezmoi unmanaged`

Use these to inspect scope boundaries.

They answer:

- what is currently managed by chezmoi
- what nearby files are still outside management

This is helpful during migration from a manual dotfiles setup.

## Secret and encryption operations

### `chezmoi edit-encrypted`

Use this when you need to modify an encrypted source-state file directly.

### `chezmoi encrypt` and `chezmoi decrypt`

Use these for direct transformations or diagnostics around encrypted content.

### `chezmoi age` and `chezmoi age-keygen`

Use these when the repository standardizes on age and you need local identities or low-level age operations.

### `chezmoi secret`

Use this when the configured `secret.command` backend should be invoked directly for testing or inspection.

## Recommended command selection by question

If the question is:

- "How do I bring this existing file under management?" -> `add`
- "Which source file backs this target?" -> `source-path`
- "What will the rendered file look like?" -> `cat`
- "Why is the template using the wrong branch?" -> `data`
- "What changes will apply?" -> `diff`
- "How do I change behavior without hand-renaming?" -> `chattr`
- "Why is this machine behaving strangely?" -> `doctor`

The right command is the one that answers the current uncertainty with the smallest amount of side effect.
