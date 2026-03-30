# Platform Patterns

Use this reference when a request spans Linux, macOS, Windows, containers, or Codespaces. The goal is not to multiply files per platform by default. The goal is to keep one coherent source state while isolating the places where platform differences are real.

## General strategy

Prefer this order:

1. One shared template or file when syntax is the same across platforms.
2. Small template branches when only a few values differ.
3. Separate files only when the target syntax or operational model truly diverges.

This keeps the repo readable. Platform support becomes hard to maintain when every OS gets its own near-duplicate file.

## Linux and macOS

Linux and macOS often share enough shell and dotfile conventions that the same file can serve both with minor branching.

### Preferred patterns

- manage normal dotfiles and `.config/` entries directly
- use small `if eq .chezmoi.os ...` branches for path differences
- use shell scripts for bootstrap actions that are truly imperative

Example:

```text
{{- if eq .chezmoi.os "darwin" -}}
export PATH="/opt/homebrew/bin:$PATH"
{{- else -}}
export PATH="$HOME/.local/bin:$PATH"
{{- end -}}
```

### When to split Linux and macOS files

Split only when:

- application config syntax diverges materially
- the macOS version must use `defaults` or plist-specific content
- one platform needs a file the other never consumes

## Windows

Windows usually differs in both scripting model and some config expectations, so explicit handling is often necessary.

### Preferred patterns

- use PowerShell for imperative setup
- define `interpreters.ps1.command` explicitly
- be careful with path separators and quoting
- set line endings only when the target consumer actually requires them

Example interpreter config:

```toml
[interpreters.ps1]
    command = "pwsh"
```

### Good Windows-specific uses of templates

- choose between `pwsh` and Unix shell snippets
- render Windows-specific paths into application configs
- emit host-specific settings for WSL vs native Windows

### Common mistake

Blindly forcing CRLF on every Windows-managed file. Many tools on modern Windows handle LF correctly. Choose CRLF only when a concrete consumer requires it.

## Containers, VMs, and ephemeral hosts

Ephemeral environments need different operational assumptions.

### Preferred patterns

- keep bootstrap idempotent
- avoid interactive prompts during unattended setup
- separate secret-dependent steps from base environment provisioning
- encode ephemeral behavior in local config or init-time choices

Useful examples:

- mark Codespaces or container hosts with `data.codespaces = true`
- skip GUI-only configuration in headless environments
- defer password-manager login to a later explicit step when unattended startup cannot support it

## Codespaces

Codespaces deserves explicit treatment because the bootstrap path often differs from a long-lived laptop.

### Good Codespaces habits

- keep bootstrap non-interactive by default
- pass an explicit `--source` path during init
- isolate source state in `src/` when the repo contains docs, CI, and scripts
- keep install scripts idempotent so rebuilds are safe

Example install pattern:

```sh
chezmoi init --apply --source "$PWD/src"
```

Why this is better than relying on defaults:

the bootstrap remains correct even when the repository layout is not the default chezmoi user source directory.

### What to avoid in Codespaces

- prompts that block unattended startup
- password-manager flows that require desktop login UI unless the environment was explicitly prepared for that
- scripts that assume persistent machine-local state from previous runs

## Cross-platform design patterns that scale

### Pattern: local config expresses machine role

Use local config to express role or environment, then branch minimally in templates.

Example:

```yaml
data:
  profile: work
  codespaces: true
```

Template:

```text
{{- if .codespaces -}}
export EDITOR="code --wait"
{{- end -}}
```

Why this works:

the template stays readable and the branching reason is explicit.

### Pattern: one template plus per-platform includes

Keep the top-level file shared, but include platform-specific fragments when syntax is mostly shared and only a small section differs.

This is cleaner than maintaining three whole near-duplicate configs.

### Pattern: separate scripts by scripting ecosystem

Keep shell bootstrap in shell scripts and Windows bootstrap in PowerShell scripts. Do not force one scripting ecosystem to impersonate the other.

## Decision rule

Before creating a separate platform file, ask:

1. Is the file syntax genuinely different?
2. Is the operational model genuinely different?
3. Would a small branch or included fragment be clearer than full duplication?

If the answer to the first two questions is no, keep one shared file.
