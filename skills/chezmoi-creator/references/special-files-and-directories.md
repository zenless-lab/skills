# Special Files And Directories

chezmoi ignores ordinary dotfiles in the source directory by default. The `.chezmoi*` namespace exists so the source repository can contain control files, reusable template material, and metadata without colliding with managed targets.

Use this reference when deciding whether a concern belongs in a normal source-state entry or in one of chezmoi's control files and directories.

## Why special files exist

The source state needs more than just files that map to destinations. It also needs places for:

- machine-local bootstrap config
- static data for templates
- ignore and remove rules
- external dependency definitions
- scripts that are not themselves target files

Special files are how chezmoi models those concerns explicitly.

## Broad evaluation order

chezmoi processes special items in this broad order:

1. `.chezmoiroot`
2. `.chezmoi.$FORMAT.tmpl`
3. `.chezmoidata.$FORMAT` and `.chezmoidata/`
4. `.chezmoitemplates/`
5. `.chezmoiignore`
6. `.chezmoiremove`
7. `.chezmoiexternal.$FORMAT` and `.chezmoiexternals/`
8. `.chezmoiversion`
9. `.chezmoiscripts/`

You do not need to memorize this exact list, but you do need to understand the consequences:

- root selection happens early
- config template and template data are available before normal rendering
- externals and scripts are separate control mechanisms, not just unusual files

## Special files

### `.chezmoiroot`

Use `.chezmoiroot` when the actual source state lives below the repository root.

This is useful when the repository also contains:

- CI configuration
- documentation
- helper scripts
- issue templates or other project metadata

Example use:

- repo root contains `README.md`, `.github/`, `install.sh`, and `src/`
- `.chezmoiroot` points chezmoi at `src/`

Why this matters:

it prevents repository housekeeping files from being misinterpreted as source-state entries.

### `.chezmoi.$FORMAT.tmpl`

This file is the init-time config template used during `chezmoi init`.

Use it for:

- prompting for machine-local values
- writing initial local config
- defining bootstrap-time defaults

Do not use it as a general-purpose template for ordinary target files. It is specifically about generating local config at init time.

Example use cases:

- prompt for email address on first setup
- prompt whether the machine is work or personal
- store password-manager vault or item identifiers locally

### `.chezmoidata.$FORMAT`

Use this for static, shared structured data that should be available to templates.

Good examples:

- a map of Git identities by profile
- common package lists by platform
- host groups or role names that are safe to keep in the repo

Bad examples:

- live secrets
- per-machine values that should stay local
- data that should be fetched from a password manager at apply time

### `.chezmoiignore`

Use this when some target paths should be managed conditionally or skipped on certain machines.

Important point:

ignore rules match target paths, not source-state filenames.

That means the rule should talk about paths like `~/.config/nvim` behaviorally, not about strings like `dot_config/nvim`.

Typical uses:

- skip Linux-only files on Windows
- skip GUI application config in headless environments
- avoid applying a file when a local package is absent

### `.chezmoiremove`

Use this when the apply should delete legacy paths that are no longer represented as managed targets.

This is useful during migration from an old layout to a new one.

Example:

- remove an obsolete `~/.vimrc` after migrating to `~/.config/nvim`

Use it for intentional cleanup, not as a substitute for understanding why a target is still being created.

### `.chezmoiversion`

Use this to declare a minimum required chezmoi version when the source state relies on features not available in older releases.

This prevents hard-to-debug failures on machines with outdated binaries.

Typical reasons:

- newer template functions
- newer config keys
- updated external definitions or script behavior

### `.chezmoiexternal.$FORMAT`

Use this to declare third-party content that should be fetched into the managed tree.

Good uses:

- plugin repos
- archives
- shared snippets
- external tools distributed as assets

Do not use externals when a normal source-state file or a script would be clearer.

Externals fetch content. They do not encode arbitrary imperative logic.

## Special directories

### `.chezmoidata/`

Use this when static template data is large enough or structured enough that a single data file becomes awkward.

Reason to choose the directory form:

- split data by domain
- keep package lists separate from profile maps
- reduce merge conflicts in collaborative repos

### `.chezmoitemplates/`

Use this for reusable template partials.

Good uses:

- shared shell fragments
- reusable git config sections
- common header/footer content

This keeps repeated template logic out of large top-level files.

### `.chezmoiexternals/`

Use this directory form when external definitions are better split by concern.

Examples:

- one file for shell plugins
- one file for fonts
- one file for editor ecosystem dependencies

### `.chezmoiscripts/`

Use this when the action should run as a script but does not correspond to a normal target file in the destination tree.

Examples:

- refresh a cache
- install a package or plugin
- perform one-time machine bootstrap

This is usually clearer than trying to hide scripts among normal source-state files.

## Practical selection rules

Use:

- normal source-state file when you are managing a file or directory in the destination tree
- `.chezmoidata` when templates need shared static data
- `.chezmoitemplates` when multiple templates repeat the same content fragment
- `.chezmoiignore` when application should be conditional by target path
- `.chezmoiremove` when old paths need explicit cleanup
- `.chezmoiexternal` when third-party content should be fetched
- `.chezmoiscripts` when side effects belong to the managed machine state

## Common mistakes

- putting secrets in `.chezmoidata.*`
- writing ignore rules against source-state filenames instead of target paths
- using `.chezmoi.$FORMAT.tmpl` as if it were a normal file template
- using externals for content that should simply live in the repository
- burying important bootstrap logic in undocumented scripts instead of using the dedicated control locations

## Example layout

```text
.
├── .chezmoiroot
├── .chezmoi.yaml.tmpl
├── .chezmoidata.yaml
├── .chezmoitemplates/
│   └── git/
│       └── aliases.tmpl
├── .chezmoiexternal.toml
├── .chezmoiscripts/
│   └── run_once_after_20-font-cache.sh
└── src/
    ├── dot_gitconfig.tmpl
    └── private_dot_ssh/
        └── config.tmpl
```

This layout separates bootstrap config, reusable data, externals, and scripts from the actual managed files.
