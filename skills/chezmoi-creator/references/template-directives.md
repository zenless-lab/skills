# Template Directives

chezmoi supports file-level template directives using the form `chezmoi:template:KEY=VALUE`. Use directives when output formatting itself matters, not just the template logic.

Directives are easy to misuse because they look powerful. In practice, they should solve concrete rendering problems such as delimiter collisions, newline policy, or strict missing-key handling.

## Where directives belong

Directives are attached to a templated file and influence how that file is rendered. They are not global configuration and they are not a substitute for clearer template design.

Use a directive when:

- the target format conflicts with normal `{{ ... }}` delimiters
- the generated file requires a specific encoding or line ending policy
- silent missing keys would be dangerous

Do not use a directive just because a template became hard to read. If readability is the problem, split the template or move repeated logic into `.chezmoitemplates/`.

## Supported directives and when they are useful

### `left-delimiter` and `right-delimiter`

Use custom delimiters when the target language already uses `{{` and `}}` heavily.

Common examples:

- Helm-like or Jinja-like config fragments
- files that embed Go templates for another tool
- documentation examples that must contain literal `{{` text

Example:

```text
# chezmoi:template:left-delimiter=[[
# chezmoi:template:right-delimiter= ]]
user = [[ .email | quote ]]
```

Why this is useful:

it removes delimiter collisions without forcing awkward escaping throughout the file.

### `encoding`

Use `encoding` only when the target consumer requires a specific text encoding.

Typical cases are rare, but they do exist in:

- Windows-specific legacy tooling
- application config formats that are not UTF-8 by default

If the target accepts UTF-8, do not introduce an explicit encoding just for completeness.

### `format-indent` and `format-indent-width`

Use these when serialization helpers like `toToml`, `toYaml`, or pretty JSON output should follow a specific indentation style in the generated file.

This matters when:

- a downstream formatter is not available
- the generated file is meant to stay hand-readable
- indentation inconsistencies create noisy diffs

### `line-endings`

Use `line-endings=lf`, `line-endings=crlf`, or `line-endings=native` when newline policy is part of compatibility.

Good uses:

- PowerShell or batch-adjacent files that require CRLF
- cross-platform repos that intentionally defer to the current OS

Bad use:

- setting CRLF on every Windows-managed file without a real compatibility need

Example:

```text
# chezmoi:template:line-endings=crlf
Write-Host "bootstrap"
```

### `missing-key`

Use `missing-key=error` when an absent value should fail fast.

This is especially important for:

- secret-backed templates
- environment-critical configs
- machine-role-specific files where omission would create a subtly broken file

Example:

```text
# chezmoi:template:missing-key=error
[user]
email = {{ .email | quote }}
```

Why this matters:

without strict missing-key handling, a typo in config data can silently produce an invalid or incomplete file.

## Example patterns

### Strict host-specific config

```text
# chezmoi:template:missing-key=error
[core]
editor = {{ .editor | quote }}
```

Use this when the file is invalid without the local config value.

### Alternate delimiters for embedded templates

```text
# chezmoi:template:left-delimiter=[[
# chezmoi:template:right-delimiter=]]
prompt = "[[ .chezmoi.hostname ]]"
literal = "{{ this stays untouched }}"
```

Use this when the target file itself must contain literal `{{ ... }}` text.

## Common mistakes

- using directives to compensate for poor template decomposition
- setting `line-endings=native` when the file must actually be stable across OSes
- leaving `missing-key` permissive for files that contain secrets or required identifiers
- specifying encoding with no consumer requirement

## Practical rule

If a reviewer asks, "Why is this directive here?" the answer should be concrete:

- because the target syntax conflicts with normal delimiters
- because this file must be CRLF
- because missing values must fail fast

If there is no concrete answer, the directive probably does not belong there.
