# Source State Naming Rules

Use this reference whenever you need to derive the correct source-state filename from a target path and intended behavior. The filename is not decoration. It is part of the configuration language.

## Why naming rules matter

In chezmoi, filenames encode semantics.

These two entries target different behavior even if they look similar:

- `dot_gitconfig`
- `dot_gitconfig.tmpl`

The second file is rendered as a template, so it can branch on OS, hostname, or config data. The first is copied as static content.

Likewise:

- `private_dot_ssh/config`
- `dot_ssh/config`

Both target `~/.ssh/config`, but only the first requests private permissions.

If the filename is wrong, chezmoi may:

- render nothing as a template when it should
- create the wrong target type
- skip required permission changes
- apply scripts in an unexpected phase

## Read a source-state filename from left to right

The encoded name typically answers these questions in order:

1. Is this a special target type such as script, symlink, or remove rule?
2. Does it have behavior attributes such as `private_` or `executable_`?
3. Does the target name begin with a dot?
4. Does the content have suffix attributes such as `.tmpl`, `.age`, or `.literal`?

Example:

- `private_executable_dot_local/bin/bootstrap.tmpl`

Interpretation:

- `private_`: restrict permissions
- `executable_`: make target executable
- `dot_`: target path segment starts with `.`
- `.tmpl`: render as template

## Prefix rules by target type

### Regular files

Common prefixes:

- `private_`: write with restricted permissions
- `readonly_`: mark read-only in the target
- `executable_`: make executable
- `empty_`: create an empty file
- `encrypted_`: source content is encrypted
- `dot_`: the target name starts with `.`

Use these when the target is an ordinary file in the destination tree.

Examples:

- `dot_zshrc`
- `private_dot_ssh/config.tmpl`
- `encrypted_private_dot_ssh/id_ed25519.age`

### Directories

Common prefixes:

- `exact_`: destination directory should exactly match managed contents
- `private_`: restrict directory permissions
- `readonly_`: set read-only attributes where supported
- `remove_`: remove the target directory
- `external_`: populate from external source
- `dot_`: target directory name starts with `.`

Example:

- `exact_dot_config/nvim`

Meaning: `~/.config/nvim` should not accumulate unmanaged extra files.

### Scripts

Scripts use a different naming grammar because phase and repetition policy matter more than a target path.

Core elements:

- `run_`: this is a script entry
- `once_` or `onchange_`: repetition policy
- `before_` or `after_`: phase relative to normal target updates

Examples:

- `run_once_before_10-bootstrap.sh`
- `run_onchange_after_20-refresh-font-cache.sh`

Meaning:

- `once_`: run only once per machine unless the state is reset
- `onchange_`: run when script content changes
- `before_`: run before normal file updates
- `after_`: run after normal file updates

### Symlinks

Use `symlink_` when the target should be a symbolic link rather than a file copy.

Example:

- `symlink_dot_config/nvim`

Do this only when the destination should intentionally remain a symlink. Do not use symlinks just because they resemble a manual dotfiles workflow.

## Prefix order is semantic, not stylistic

The order of prefixes matters. It is not just a naming convention for humans.

For example, if a file should be both private and executable, encode both attributes in the expected order. When in doubt, prefer `chezmoi add` and `chezmoi chattr` instead of manual renaming.

Practical rule:

- let chezmoi derive the initial path with `add`
- change behavior with `chattr`
- hand-edit names only when you fully understand the attribute grammar

## Suffix rules

### `.tmpl`

Use `.tmpl` when the file should be rendered as a Go template.

Use it for:

- host-specific branches
- inserting machine-local config values
- conditional includes
- secret lookups at render time

Do not use it for a file that is completely static across machines.

### Encryption suffixes

Encrypted files also use an encryption suffix such as:

- `.age`
- `.asc`

Example:

- `encrypted_private_dot_ssh/id_ed25519.age`

This says the source-state content is encrypted, and the destination target should be private.

### `.literal`

Use `.literal` when suffix parsing should stop.

This is useful when the real filename ends with something that would otherwise be interpreted as a chezmoi attribute.

## Literal escape behavior

### `literal_`

Use `literal_` in the filename when a path segment would otherwise collide with a recognized prefix.

### `.literal`

Use this when the basename or extension would otherwise be parsed as suffix behavior.

Both mechanisms exist so you can represent real filenames without fighting chezmoi's attribute grammar.

## Common mappings and why they are correct

### Dotfile target

- target: `~/.zshrc`
- source state: `dot_zshrc`

Why: `dot_` encodes the leading dot.

### Templated dotfile

- target: `~/.gitconfig`
- source state: `dot_gitconfig.tmpl`

Why: the file has a leading dot and should be rendered.

### Private templated SSH config

- target: `~/.ssh/config`
- source state: `private_dot_ssh/config.tmpl`

Why: SSH config often contains sensitive hostnames or usernames and should have restricted permissions.

### Executable local utility

- target: `~/.local/bin/bootstrap`
- source state: `private_executable_dot_local/bin/bootstrap`

Why: the target is under a dot directory, should be executable, and may reasonably be private if it contains machine-specific logic.

### One-time bootstrap script

- source state: `run_once_before_10-bootstrap.sh`

Why: this is a lifecycle script, not a target file. Its sequencing is explicit.

## Design guidance

Prefer encoding the real behavior in the filename rather than explaining hidden conventions in comments.

Good approach:

- the filename shows that a file is templated, private, or executable
- `source-path` and `target-path` can explain the mapping directly

Bad approach:

- plain filenames plus informal knowledge that a later step "will fix permissions"

## Debugging naming mistakes

When naming looks wrong, use these commands:

1. `chezmoi source-path <target>` to see the active source-state path
2. `chezmoi target-path <source-path>` to verify the reverse mapping
3. `chezmoi diff` to catch permission or content mismatches caused by wrong attributes
4. `chezmoi chattr` to change behavior without manual rename errors

If you are unsure whether the filename is valid, do not guess. Let chezmoi encode it for you and then inspect the result.
