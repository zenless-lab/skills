# Template Data And Functions

Use this reference when authoring `.tmpl` files or init-time config templates. The goal is not to dump every available helper name. The goal is to understand what kind of data a template should consume, which helpers are appropriate, and when a function is a smell rather than a solution.

## Start with the data model, not the function list

Before picking a function, decide where the template's inputs should come from.

Preferred order:

1. Built-in `.chezmoi` facts for machine identity.
2. Local config for machine-specific values.
3. Shared `.chezmoidata.*` for static repo-owned data.
4. Password-manager or secret helpers for secrets.
5. Shell-out helpers only when the data truly comes from an external command.

This order matters because templates become brittle when they depend on ad hoc command execution instead of explicit data sources.

## Built-in `.chezmoi` data

The `.chezmoi` object exposes machine facts that are safe and stable enough for branching.

Frequently useful fields:

- `.chezmoi.arch`
- `.chezmoi.os`
- `.chezmoi.homeDir`
- `.chezmoi.sourceDir`
- `.chezmoi.destDir`
- `.chezmoi.hostname`
- `.chezmoi.username`
- `.chezmoi.pathSeparator`

### When to use built-in facts

Use them for:

- OS-specific branches
- host or username-specific file paths
- location-aware include decisions
- small compatibility adjustments

Example:

```text
{{- if eq .chezmoi.os "darwin" -}}
set -g default-command /opt/homebrew/bin/fish
{{- else -}}
set -g default-command /usr/bin/fish
{{- end -}}
```

Why this is good:

the branch depends on a stable machine fact, not on parsing command output.

## Local config data

Local config is the right source for values that differ by machine or user but should not be guessed from system facts.

Use it for:

- email addresses
- work vs personal profile selection
- Codespaces flags
- secret item identifiers
- editor or tool paths that vary locally

Example config:

```toml
[data]
profile = "work"
email = "dev@example.com"
```

Template use:

```text
[user]
email = {{ .email | quote }}
```

Why this is better than hardcoding:

the source state stays reusable while the local machine keeps its own identity data.

## Shared static data with `.chezmoidata.*`

Use `.chezmoidata.*` for repo-owned data that is shared across machines and safe to commit.

Good examples:

- Git alias sets
- package lists by platform
- feature flags by profile
- known hosts or service endpoints that are not secret

Example data:

```yaml
gitProfiles:
  work:
    signingKey: ABC123
  personal:
    signingKey: DEF456
```

Template use:

```text
[user]
signingkey = {{ (index .gitProfiles .profile).signingKey | quote }}
```

Why this is useful:

it keeps shared structured data versioned without embedding it into every template.

## Content and composition functions

These functions help break templates into reusable or safer pieces.

### `include`

Use `include` to embed raw file content.

Choose it when the included file should not itself be rendered as a template.

### `includeTemplate`

Use `includeTemplate` when the included file should be rendered with the current template context.

This is the more common choice for reusable config fragments.

Example:

```text
[alias]
{{ includeTemplate ".chezmoitemplates/git/aliases.tmpl" }}
```

Why this is good:

the repeated alias block lives once, but still has access to template data.

### `comment`

Use `comment` when generated content needs a comment prefix applied consistently.

This is helpful for generated headers in formats where comment syntax varies.

### `ensureLinePrefix`

Use this when a multiline value must be prefixed line by line, such as indentation or comment markers.

### `replaceAllRegex`

Use regex replacement when normal string replacement is not expressive enough.

Do not reach for regex first. It is easy to make templates opaque.

### `abortEmpty`

Use this when a target should not be written if the rendered content is empty.

This is safer than creating a blank config file that changes program behavior.

### `warnf`

Use this to emit a warning during rendering when the template can still proceed but the operator should know something is unusual.

Example:

```text
{{- if not .email -}}
{{ warnf "email is not configured; gitconfig will be incomplete" }}
{{- end -}}
```

## Filesystem and path functions

Use these when the template must adapt to actual file locations or tool availability.

### `joinPath`

Prefer `joinPath` over hand-concatenating `/` when the template should remain portable.

Example:

```text
{{ joinPath .chezmoi.homeDir ".local" "bin" }}
```

### `lookPath`, `findExecutable`, `findOneExecutable`

Use these to discover whether a tool is available and which executable name should be used.

Good example:

```text
{{- $editor := findOneExecutable "nvim" "vim" -}}
editor = {{ $editor | quote }}
```

Why this is appropriate:

it avoids hardcoding a single binary name when the environment legitimately varies.

### `isExecutable`, `stat`, `lstat`, `glob`

Use these sparingly. They are useful for conditional rendering based on filesystem state, but they can also make a template depend too heavily on ambient machine state.

Good use:

- render a path only if a tool exists

Risky use:

- build large configuration branches based on many local files that are not themselves managed by chezmoi

## Serialization and parsing helpers

Use these when the template needs to transform structured data rather than manually string-build it.

Common helpers:

- `fromJson`, `toPrettyJson`
- `fromYaml`, `toYaml`
- `fromToml`, `toToml`
- `fromIni`, `toIni`
- `toString`, `toStrings`

### When they are useful

Use them when:

- a template composes nested structured data
- you want stable formatting for generated machine-readable config
- the source data is easier to express in one format and emit in another

Example:

```text
{{ toToml (dict "server" (dict "host" "127.0.0.1" "port" 8080)) }}
```

Why this is better than manual string concatenation:

it avoids formatting drift and quoting mistakes.

## Command execution helpers

Helpers:

- `output`
- `outputList`
- `exec`

These are the most commonly overused template functions.

### When they are justified

Use them when the authoritative source of data is an external command and there is no better static or configured representation.

Examples:

- querying a version manager for an installed path
- reading a CLI that is already the canonical source of a value

### When they are a smell

Avoid them when they merely compensate for missing config or data modeling.

Bad pattern:

- calling `hostname`, `uname`, or `whoami` even though `.chezmoi` already provides the facts

Bad pattern:

- calling shell pipelines to derive data that should live in `.chezmoidata.*`

## Secret and external helpers

Common families:

- `decrypt`, `encrypt`
- `secret`, `secretJSON`
- `onepassword*`
- `bitwarden*`
- `keepassxc*`
- `pass`, `passFields`
- `vault`
- `keyring`
- `gitHubKeys`
- `gitHubLatestRelease`

### How to choose

Use password-manager helpers for runtime secret lookup. Use `decrypt` and `encrypt` for encrypted blobs already stored in the source state. Use GitHub-related helpers for public external metadata such as SSH keys or release assets.

Example secret lookup:

```text
token = {{ onepasswordRead "op://Personal/github-token/password" | quote }}
```

Why this is preferable:

the secret never needs to live in plaintext in the repository.

## Init-only prompt functions

These functions are only valid in `.chezmoi.$FORMAT.tmpl` during `chezmoi init`:

- `promptString`
- `promptBool`
- `promptInt`
- `promptChoice`
- `promptMultichoice`
- `prompt*Once`
- `stdinIsATTY`
- `exit`
- `writeToStdout`

### What they are for

Use prompt functions to collect machine-local bootstrap data once, then persist that data in local config.

Good examples:

- ask which profile this machine should use
- ask for work vs personal email
- ask whether the machine is ephemeral or persistent

Bad examples:

- prompting for values that should come from a password manager
- prompting repeatedly for data that belongs in shared repo state

Example:

```text
[data]
profile = {{ promptChoiceOnce "profile" "Choose profile" (list "work" "personal") | quote }}
```

## Practical design rules

Prefer templates that are mostly declarative:

- branch on `.chezmoi` facts
- read machine-local config for identity
- read shared static data for repo-wide structure
- look up secrets at render time

Avoid templates that act like shell scripts.

If a template needs many command executions, complex regex rewrites, and ambient filesystem probing, the design is usually pushing too much logic into rendering.
