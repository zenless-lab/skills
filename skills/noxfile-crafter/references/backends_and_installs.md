# Backends And Installs

Choose the backend and installation model that matches the repository.

## Default Backend Rule
If uv is already part of the project workflow, or uv is installed and there is no reason to avoid it, prefer:

```python
nox.options.default_venv_backend = "uv|virtualenv"
```

This keeps local runs fast while preserving a fallback for environments without uv.

## When To Use Specific Backends
- `uv`: repositories that intentionally use uv and install it in CI
- `uv|virtualenv`: best default when uv is preferred but not guaranteed everywhere
- `virtualenv`: traditional default when the project does not use uv
- `venv`: when the project explicitly standardizes on stdlib `venv`
- `conda`, `mamba`, `micromamba`: scientific or binary-heavy environments
- `none`: only for intentional no-venv workflows

## Install Strategy
Prefer the repository's existing dependency source.

Examples:

### Editable package with extras
```python
session.install("-e", ".[test]")
```

### Requirements file
```python
session.install("-r", "requirements.txt")
```

### uv-native sync flow
```python
session.run_install(
    "uv",
    "sync",
    "--extra=test",
    f"--python={session.virtualenv.location}",
    env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
)
```

Do not switch dependency models unless the user asked for that change or the current model is clearly broken.

## Reuse And No-Venv Notes
- `reuse_venv=True` is useful for expensive setups.
- Keep reuse settings aligned with contributor expectations and CI speed.
- In no-venv mode, avoid `session.install()` and use `session.run("pip", ...)` only when you intentionally want to modify the active interpreter.
