# Script Standards

Use this file when adding or reviewing scripts bundled inside a skill.

## When to add a script

Add a script only when at least one of these is true:

- the same logic would otherwise be rewritten repeatedly
- deterministic execution matters
- the operation is error-prone enough that code is safer than prose
- the script reduces context load substantially

## Python default

Prefer Python 3 for skill scripts unless another language is clearly better for the environment or task.

## PEP 723 and `uv run`

For Python scripts, prefer a single self-contained file that can run directly with `uv run`.

Use PEP 723 inline metadata at the top of the file when dependencies are needed:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27",
#   "typer>=0.12",
# ]
# ///
```

This enables execution like:

```bash
uv run scripts/example.py --help
```

Prefer this pattern over creating a separate package or `requirements.txt` unless the script is large enough to justify a fuller project structure.

## Behavioral expectations

Scripts should:

- validate inputs early
- return actionable error messages
- avoid noisy tracebacks unless explicitly useful
- print concise, agent-readable success output
- avoid dumping huge payloads to stdout
- use sensible exit codes

## Dependency guidance

- keep dependencies minimal
- prefer mature libraries
- pin only when necessary
- keep the script runnable in isolation

## Recommended layout

- one file per discrete tool where practical
- a `main()` entry point
- type hints when they improve clarity
- comments only for non-obvious logic

Use `assets/uv_script.py` as the baseline template.
