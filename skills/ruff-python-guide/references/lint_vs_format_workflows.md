# Ruff Lint vs Format Workflows

This reference helps an agent choose the right Ruff command sequence for local development, automation, and migration.

## 1. Treat the Commands as Different Operations

Ruff exposes separate workflows:

* `ruff check` for diagnostics
* `ruff check --fix` for automatic lint fixes
* `ruff check --diff` for previewing fixes without rewriting files
* `ruff format` for code formatting
* `ruff format --check` for verification without rewriting files
* `ruff format --diff` for previewing formatting deltas

Do not collapse these into one mental model. They solve different problems and carry different rollout risks.

## 2. Local Development Flows

### Inspection flow

Use when you need visibility before editing:

```bash
ruff check
ruff format --check
```

Use `uv run` variants when Ruff is installed inside the project environment.

### Safe cleanup flow

Use when the repository already accepts Ruff fixes and formatting:

```bash
ruff check --fix
ruff format
```

This order matters because lint fixes can produce code that still needs formatting.

If the repository permits only safe fixes, do not add `--unsafe-fixes` by default.

### Narrow-scope flow

Use path-based runs when migrating a large codebase:

```bash
ruff check path/to/module
ruff check --fix path/to/module
ruff format path/to/module
```

## 3. CI and Policy Flows

### Fail-on-violation linting

Use when CI should report issues but not rewrite code:

```bash
ruff check .
```

### Format verification only

Use when formatting is enforced but CI should not mutate files:

```bash
ruff format --check .
```

Use `ruff format --diff .` when reviewers benefit from seeing the exact formatting delta in CI logs.

### Combined verification

Use when Ruff owns both responsibilities:

```bash
ruff check .
ruff format --check .
```

Keep them as separate commands so failures remain easy to interpret.

## 4. Fix Safety and Rollout

Ruff distinguishes between safe and unsafe fixes.

Default practice:

* use safe fixes by default
* enable unsafe fixes only when the repository explicitly accepts behavior-changing rewrites

Use unsafe fixes cautiously because they can alter runtime behavior, exception types, or surrounding comments.

If CI should fail when a fix or format would have changed files, use flags such as `--exit-non-zero-on-fix` or `--exit-non-zero-on-format` intentionally rather than relying on implicit policy.

## 5. When to Use `--add-noqa`

Use `ruff check --add-noqa` only during deliberate migration phases.

Good use cases:

* enabling a new rule family while preserving current release velocity
* documenting legacy exceptions before tightening standards

Bad use cases:

* hiding unknown failures without review
* replacing targeted configuration with blanket suppression

## 6. Notebooks and Documentation Files

If notebooks are included, decide whether Ruff should lint them, format them, or both. Keep exclusions explicit because notebook behavior can differ from library code expectations.

Remember that some rules behave differently for notebooks. For example, `E402` applies at the top of a notebook cell rather than the top of the whole file.

If documentation code blocks are in scope, verify that the formatter mode and include settings match the repository's documentation workflow.

## 7. Recommended Operational Order

Choose the command order based on policy:

1. `ruff check` first when surveying a repository.
2. `ruff check --fix` before `ruff format` when applying changes.
3. `ruff format --check` in CI when formatting must be enforced without mutation.
4. keep lint and format commands separate in automation for clearer failure output.

## 8. What an Agent Should Report

When proposing a Ruff workflow, summarize:

1. which commands are local-only
2. which commands are CI-only
3. whether fixes are allowed
4. whether formatting is authoritative
5. what order the commands should run in
