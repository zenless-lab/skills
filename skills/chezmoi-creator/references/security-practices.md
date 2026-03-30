# Security Practices

Use this reference whenever the request involves secrets, credentials, private keys, API tokens, certificates, sensitive host configuration, or any file that would be risky to commit in plaintext. The purpose is to choose the least risky mechanism that still fits the operational workflow.

## Security design priority

Prefer this order of choices:

1. Password-manager template functions for individual secrets or structured secret records.
2. Encrypted source-state files for full files that must live in the repo.
3. Machine-local config only for non-secret identity data or bootstrap pointers to secret backends.

This order reflects a simple rule: keep secret material out of git entirely unless there is a strong reason the repo itself must carry the encrypted artifact.

## Step 1: classify the secret correctly

Before choosing a mechanism, decide what kind of thing you are managing.

### Small secret value or record

Examples:

- API token
- password
- OAuth client secret
- username plus password pair
- short JSON-like credential record

Preferred mechanism: password manager lookup at render time.

### Opaque secret file

Examples:

- SSH private key
- certificate bundle
- license file
- app config that is almost entirely secret material

Preferred mechanism: encrypted source-state file.

### Non-secret selector or identity value

Examples:

- machine role
- profile name
- vault name
- item identifier
- hostname-specific feature flag

Preferred mechanism: local config.

These values control how secrets are found. They are not the secrets themselves.

## When to use an external password manager

Use a password manager when:

- the secret should never live in git history, even encrypted
- the secret rotates independently from repo changes
- the target file can be rendered from fields at apply time
- the repo may be public or widely shared
- interactive or pre-authenticated CLI access is acceptable in the environment

Typical examples:

- render cloud tokens into shell exports
- render application credentials into config templates
- fetch database passwords or API keys on demand

Why this is often the safest default:

the repo contains structure and references, but not the secret material itself.

## When to use encrypted files

Use encrypted source-state files when:

- the managed artifact is naturally a whole file
- splitting it into template fields would make the design worse
- the file should stay versioned with the source state
- the file must still be available when the password manager is unavailable

Typical examples:

- private keys
- certificate chains
- small opaque config files that are almost entirely sensitive

Why not use encrypted files for everything:

small tokens and passwords become harder to rotate and reason about when buried in opaque encrypted blobs.

## When to use machine-local config

Use machine-local config when the value is not secret but does vary by machine, host, user, or environment.

Good examples:

- `profile = "work"`
- `codespaces = true`
- `onepasswordVault = "Personal"`  <!-- pragma: allowlist secret -->
- `githubTokenItem = "personal/github-token"`

Bad examples:

- raw API tokens
- private key contents
- long-lived secrets copied from a password manager

## Password manager usage patterns

Password managers are preferred for most field-level secrets because the source state can remain public or at least non-sensitive.

### 1Password

#### `onepasswordRead`

Use `onepasswordRead` when you already know the `op://` field path and only need a single value.

Example:

```text
{{ onepasswordRead "op://Personal/cloudflare-api-token/password" }}
```

Use it for:

- passwords
- tokens
- single named fields

Why it is good:

it is simple, explicit, and keeps the template readable.

#### `onepasswordDocument`

Use this when the secret is stored in 1Password as a full document and should be emitted as a whole file.

Example:

```text
{{- onepasswordDocument "uuid" -}}
```

Choose this over field-by-field assembly when the document is already the canonical unit.

#### `onepasswordDetailsFields`

Use this when the item contains structured fields and the template needs several of them.

Example:

```text
{{ (onepasswordDetailsFields "item-uuid" "vault-uuid").password.value }}
```

Operational notes:

- requires the `op` CLI
- requires a valid authentication context
- better for a few related fields than for many unrelated lookups spread through one large template

### Bitwarden

#### `bitwarden`

Use this when you need the full item JSON.

Example:

```text
{{ (bitwarden "item" "item-id").login.username }}
```

#### `bitwardenFields`

Use this when custom fields are the main thing you need.

Example:

```text
{{ (bitwardenFields "item" "item-id").token.value }}
```

#### `bitwardenAttachment`

Use this when the secret material is stored as an attachment rather than ordinary item fields.

Operational notes:

- depends on the `bw` CLI
- often depends on an unlocked session such as `BW_SESSION`
- unattended environments need deliberate session handling

### Generic secret backends with `secret.command`

When there is no dedicated chezmoi helper, configure a generic backend and call it through `secret` or `secretJSON`.

Example config:

```toml
[secret]
    command = "vault"
```

Template examples:

```text
{{ secret "kv" "get" "-field=value" "secret/app/token" }}
{{ (secretJSON "kv" "get" "-format=json" "secret/app/config").data.data.token }}
```

Use `secret` for raw string output. Use `secretJSON` when the CLI returns structured JSON that the template should query.

## Password manager best practices

- store secret values in the password manager, not in `.chezmoidata.*`
- keep local config limited to vault names, item IDs, profile selectors, and other references
- test secret-backed templates with `chezmoi execute-template` before broad apply runs
- keep one template focused on one related set of secrets; many unrelated lookups in one file are harder to debug and slower to render

## Encrypted file workflow

Use encrypted files when the secret is naturally a file.

### Add an encrypted file

```sh
chezmoi add --encrypt ~/.ssh/id_ed25519
```

This creates an encrypted source-state entry. The file can then be applied normally while the stored source content remains encrypted.

### Edit an encrypted file

```sh
chezmoi edit ~/.ssh/id_ed25519
chezmoi edit-encrypted encrypted_private_dot_ssh/id_ed25519.age
```

Use the first form when you think in terms of the target path. Use the second form when you intentionally want to operate on the encrypted source entry itself.

### Prefer age for new setups

For new designs, prefer age unless the user already standardized on GPG.

Example local config:

```toml
encryption = "age"

[age]
    recipient = "age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    identity = "~/.config/chezmoi/key.txt"
```

Why age is often the better default:

- simpler recipient model
- straightforward bootstrap for repo-stored encrypted blobs
- good ergonomics for personal dotfiles repositories

### Bootstrap pattern for encrypted identity material

If encrypted files depend on a local identity that itself must be provisioned, use a small `run_onchange_before_` script to place or decrypt the local identity into a machine-local path before other encrypted content is needed.

This is appropriate when the identity can be unlocked with a one-time passphrase or another operator step.

## Safe composition patterns

### Pattern: non-secret structure plus secret lookup

```text
[profile prod]
token = {{ onepasswordRead "op://Infra/prod-api-token/password" | quote }}
region = "us-east-1"
```

Why it is good:

- the file structure stays visible in git
- only the sensitive field is fetched dynamically

### Pattern: encrypted key plus templated config

- keep the private key as an encrypted managed file
- keep the SSH config as a template that references the key path and host logic

Why it is good:

- the opaque secret remains a file-level blob
- the readable routing logic remains easy to review

### Pattern: local config stores references, not secrets

```yaml
data:
  onepasswordVault: Personal
  githubTokenItem: personal/github-token
```

Template:

```text
{{ onepasswordRead (printf "op://%s/%s/password" .onepasswordVault .githubTokenItem) }}
```

Why it is good:

machine-local differences stay local, but no secret is copied into config.

## Anti-patterns

- committing plaintext secrets into templates or `.chezmoidata.*`
- storing long-lived secrets in config `data`
- using hooks for secret bootstrap when a source-state script or password-manager lookup is the real mechanism
- splitting an opaque secret file into dozens of template fragments when one encrypted file would be simpler
- writing secret-derived files without `private_` when restrictive permissions are needed

## Codespaces and automation

In unattended environments:

- avoid secret flows that require interactive desktop login unless the environment is explicitly prepared for it
- prefer encrypted files when a bootstrap must succeed without live password-manager auth
- otherwise keep base bootstrap non-secret and defer authenticated secret retrieval to an intentional later step

The `chezmoi/dotfiles` example repository demonstrates two useful operational habits:

- the install flow passes an explicit `--source` path
- bootstrap config makes source directory selection explicit

For repositories that also contain CI, docs, and project metadata, prefer an isolated `src/` source directory so only chezmoi-managed state lives under the source root.

## Final decision rule

Ask three questions:

1. Is the secret naturally a field or a file?
2. Must the repo carry the secret artifact at all?
3. Can the environment authenticate to a secret backend safely at render time?

If it is a field and runtime auth is acceptable, use a password manager.

If it is a file and the repo must carry it, use encryption.

If it is not actually secret, keep only the selector or reference in local config.
