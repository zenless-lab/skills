# Configuration Formats And Hooks

Use this reference for two related but distinct concerns: choosing a config file format, and deciding when command hooks are appropriate. These topics belong together because both affect how chezmoi itself behaves rather than what files it manages.

## Choosing a configuration format

chezmoi supports:

- JSON
- JSONC
- TOML
- YAML

The format choice should optimize readability and operational safety, not personal taste alone.

## Recommended default: TOML

Prefer TOML unless the repository already standardized on another format or surrounding tooling strongly favors something else.

Why TOML is a strong default:

- compact for small machine-local config files
- explicit typing for booleans, arrays, and strings
- common in chezmoi examples and dotfile ecosystems
- avoids YAML's indentation sensitivity for simple key-value config

## When to choose another format

### YAML

Choose YAML when:

- the repo already uses YAML heavily
- local operators are more comfortable editing YAML
- the configuration contains nested structures where YAML is easier to scan

Risk:

indentation mistakes are easy to make, especially in small hand-edited local files.

### JSON or JSONC

Choose JSON when:

- nearby tooling already emits or consumes JSON
- strict machine-generated config is more important than hand editing

Choose JSONC when comments are useful but JSON ecosystem compatibility still matters.

Risk:

JSON is verbose for small human-edited config; JSONC is not universally supported by non-chezmoi tools.

## Practical format rule

If the file will mostly be edited by humans on local machines, TOML is usually the safest choice. If the file should match repo conventions or adjacent tooling, use that format deliberately.

## Hooks are not scripts

Hooks and source-state `run_*` scripts are often confused because both can execute commands. Their purpose is different.

### Use a hook when

the action belongs to a chezmoi command lifecycle event.

Examples:

- run a formatter after `chezmoi add`
- trigger repo maintenance after `chezmoi apply`
- perform bookkeeping around git auto-commit or auto-push events

### Use a source-state script when

the action belongs to the machine's desired managed state.

Examples:

- install plugins
- refresh caches
- create directories or run bootstrap setup

This distinction is important because hooks run because a command happened. Scripts run because the managed state requires them.

## Hook behavior that surprises people

### Hooks run even during `--dry-run`

This is the most important operational warning.

If a side effect should not happen during dry-run, it probably should not be a hook.

Examples of risky hook behavior:

- touching external systems
- mutating repo state
- prompting for secrets unexpectedly

### Hooks should be fast and idempotent

Because hooks are tied to command execution, slow or stateful hooks quickly make normal operations frustrating and unpredictable.

Good hook properties:

- fast
- deterministic
- safe to run repeatedly
- obvious from repo documentation

## Events and timing

Hooks can be attached to events such as:

- command events like `add` or `apply`
- `git-auto-commit`
- `git-auto-push`
- `read-source-state`

Each event can have `.pre` and `.post` entries.

### How to choose pre vs post

Use `.pre` when the hook should validate or prepare before the event proceeds.

Use `.post` when the hook should react to the completed event.

Examples:

- `apply.pre`: lightweight validation before apply
- `apply.post`: run a repo-local reporter or notifier after apply

## Hook forms

A hook entry can define:

- `command` with optional `args`
- `script` with optional `args`

### `command`

Use `command` when the executable is simple and explicit.

Example use:

- run `make lint`
- invoke a repo wrapper script with stable arguments

### `script`

Use `script` when the hook target is itself a script file and you want chezmoi to resolve the interpreter from configuration.

This is useful when file extension to interpreter mapping matters.

## Hook environment

Hook execution sets environment variables including:

- `CHEZMOI=1`
- `CHEZMOI_COMMAND`
- `CHEZMOI_COMMAND_DIR`
- `CHEZMOI_ARGS`

These variables are useful when the hook behavior should depend on which chezmoi command triggered it.

Example:

- a shared script can branch differently for `add` vs `apply` using `CHEZMOI_COMMAND`

## Good and bad hook examples

### Good hook

- run a lightweight repo linter after `chezmoi add`

Why it is good:

- directly tied to the command lifecycle
- quick to execute
- useful even during iterative editing

### Bad hook

- install fonts or large external tools on every dry-run apply

Why it is bad:

- expensive
- surprising
- belongs to managed machine state, so it should be a source-state script instead

## Decision rule

Ask one question:

"If chezmoi did not run this command, would I still want this action as part of the machine state?"

If the answer is yes, it should usually be a source-state script.

If the answer is no, and the action is about the lifecycle of the chezmoi command itself, a hook may be appropriate.
