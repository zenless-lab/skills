# Concepts And Application Order

Use this reference when deciding how a real file in the working tree should be represented in chezmoi, and when debugging why an apply run behaved differently than expected.

## The four states that matter

### Destination directory

The destination directory is the tree chezmoi manages, usually the current user's home directory. This is where the final files actually live.

When a user says "manage ~/.zshrc with chezmoi", the destination path is `~/.zshrc`.

### Source state

The source state is the representation stored in the chezmoi source directory. It is not a raw mirror of the destination tree. Filenames encode behavior such as:

- whether the target is private
- whether the target is executable
- whether the content is a template
- whether the entry is a script, symlink, or external

Example:

- destination path: `~/.gitconfig`
- source-state path: `dot_gitconfig.tmpl`

The source-state path says more than "this is .gitconfig". It also says "this file starts with a dot" and "render it as a template".

### Target state

The target state is chezmoi's computed result after it combines:

- source-state entries
- template rendering
- machine-local config
- built-in facts like OS, username, and hostname

The target state is what chezmoi intends to write, even if it has not been written yet.

Use `chezmoi cat` or `chezmoi dump` when you need to inspect target state before applying.

### Config file

The config file is machine-local control data, usually under `.config/chezmoi/` or explicitly passed via `--config`. It is where host-specific values belong when they should not be hardcoded in the shared source state.

Good config examples:

- whether the current machine is a Codespace
- email address or username variations
- password-manager item IDs or vault names
- OS-specific tool paths

Bad config examples:

- full reusable dotfile content that should live in the source state
- large static data that should be versioned with the repo

## How chezmoi thinks about a change

When you run `chezmoi apply`, the design question is not "copy file A to file B". The actual flow is:

1. Read the source state.
2. Read local config and machine facts.
3. Render and compute the expected target state.
4. Compare expected target state with the destination tree.
5. Run lifecycle scripts in the appropriate phase.
6. Update the destination tree.

This is why debugging chezmoi usually means asking one of three questions:

1. Is the source-state entry named correctly?
2. Is the template rendering the intended target state?
3. Did a script, external, or hook run at a different phase than expected?

## Deterministic application order

chezmoi applies state in a stable order:

1. Read source state.
2. Read destination state.
3. Compute target state.
4. Run `run_before_` scripts in alphabetical order.
5. Update managed entries in target-name order.
6. Run `run_after_` scripts in alphabetical order.

This order explains several common surprises.

### Why `run_before_` is not a bootstrap catch-all

`run_before_` runs before normal files, directories, and externals are updated. If a script depends on an external repo or a generated config file that will only appear during the update phase, it should not be a `run_before_` script.

Use `run_before_` for work that must happen before any managed targets are written, such as:

- creating a prerequisite directory outside the managed tree
- installing a local interpreter needed by later scripts
- decrypting a machine-local identity needed for later template rendering

### Why `run_after_` is often the safer default

`run_after_` can assume the current apply already created or updated the files it depends on.

Use it for:

- reloading shell completions after files land
- running `fc-cache` after fonts are installed
- invoking `gsettings`, `defaults`, or `dconf` after target files are present

### Why sort order matters for scripts

Script order is alphabetical after the `run_` attributes are interpreted. That means prefixes like `10-`, `20-`, and `90-` are not cosmetic. They are the simplest way to make sequencing explicit.

Example:

- `run_once_before_10-bootstrap.sh`
- `run_once_before_20-install-packages.sh`
- `run_once_after_90-finalize.sh`

## Scripts, hooks, and externals are different tools

These mechanisms are often confused because all three can trigger side effects.

### Source-state scripts

Use source-state scripts when the action is part of the managed machine state.

Examples:

- install a package manager plugin
- create a cache directory that should exist on every machine
- import shell plugins after files are written

The script belongs in the source state because it is part of the desired end state of the machine.

### Hooks

Use hooks when the action is tied to a chezmoi command lifecycle event rather than the target machine state.

Examples:

- lint the source state after `chezmoi add`
- run a repo-specific formatter after `chezmoi apply`
- auto-commit the source repository after an update flow

Hooks are about what happens when a chezmoi command runs, not about what files the machine should contain.

### Externals

Use externals when the source state depends on third-party content that should be fetched, unpacked, or checked out.

Examples:

- clone a shared tmux plugin repo
- download a binary release asset
- vendor a shared snippet archive

Externals are not a substitute for scripts. They fetch content. Scripts perform actions.

## A practical design example

Goal: manage a host-specific `.gitconfig`, clone a shared tmux plugin set, and run a post-apply cache refresh.

Recommended split:

- `dot_gitconfig.tmpl`: holds the config structure and host branches
- `.chezmoiexternal.toml`: fetches tmux plugin repo into the destination tree
- `run_after_20-refresh-tmux.sh`: reloads or refreshes after files and externals exist
- local config: stores per-machine email, signing key, or host role

This split is easier to reason about than trying to do everything in one script.

## Debugging checklist

When the result is wrong, check in this order:

1. `chezmoi source-path <target>`: confirm the source-state file you think is active is actually the one chezmoi uses.
2. `chezmoi cat <target>`: inspect rendered content before touching the destination tree.
3. `chezmoi diff`: verify whether the computed target state differs from the destination tree.
4. `chezmoi data`: inspect machine facts and config-derived data.
5. Review script phase: if a file is missing when a script runs, the phase is probably wrong.

If the failure is about file presence or ordering, think in phases. If the failure is about content, think in rendering and data.
