# Nox API Reference

This reference mirrors the APIs and Noxfile configuration surface described in the upstream configuration documentation. It is compact, but it is intended to be complete for day-to-day noxfile authoring.

## Noxfile Discovery

- Default configuration file: `noxfile.py`
- Alternate file: `nox --noxfile something.py` or `nox -f something.py`

## Session Definition APIs

### `@nox.session(...)`
Defines a Nox session from a Python function.

Important keyword arguments covered by the configuration docs:
- `python` or `py`: Interpreter selector. Accepts a version string, executable name, a list of versions, or `False` to disable virtualenv creation.
- `name`: Public session name shown by `nox --list` and used with `nox --session`.
- `default`: Whether the session is selected by default.
- `reuse_venv`: Reuse the session virtualenv unless CLI settings override it.
- `venv_backend`: Environment backend. Common values are `"virtualenv"`, `"venv"`, `"uv"`, `"conda"`, `"mamba"`, `"micromamba"`, and `"none"`.
- `venv_params`: Additional backend-specific arguments.
- `tags`: Session tags.
- `requires`: Sessions that must run first.

Example:
```python
@nox.session(name="tests", python=["3.11", "3.12"], reuse_venv=True)
def run_tests(session):
    """Run the test suite."""
    session.run("pytest")
```

### Session Docstrings
The first line of the session docstring is shown by `nox --list`. The full docstring is shown by `nox --usage <session>`.

Example:
```python
@nox.session
def tests(session):
    """Run the test suite.

    The test suite consists of all tests in tests/.
    """
    session.run("pytest")
```

### Session Name Selection
By default, the function name becomes the session name. Use `name=` to expose a different public name.

### Session Python Selection
Supported patterns from the configuration docs:
- `python="3.12"`
- `python=["3.10", "3.11", "3.12"]`
- `python=["3.6", "pypy-6.0"]`
- `python=False`

Behavior:
- Version-based sessions expand into separate collected sessions such as `tests-3.10`.
- If an interpreter is missing, `--download-python auto|always|never` controls download behavior.
- `python=False` and `venv_backend="none"` are equivalent no-venv modes.

### `@nox.parametrize(...)`
Parametrizes session arguments.

Supported authoring patterns reflected in the config docs:
- `@nox.parametrize("django", ["1.9", "2.0"])`
- stacked parameterization
- parameterizing Python via `@nox.parametrize("python", [...])`
- custom IDs with `ids=[...]`
- tag assignment with `tags=[...]`
- generator-driven `nox.param(...)` values

Examples:
```python
@nox.session
@nox.parametrize("django", ["1.9", "2.0"], ids=["old", "new"])
def tests(session, django):
    session.install(f"django=={django}")
    session.run("pytest")
```

```python
@nox.session
@nox.parametrize("python", ["3.10", "3.11", "3.12"])
def tests(session):
    session.run("pytest")
```

### `nox.param(...)`
Use `nox.param()` inside `@nox.parametrize(...)` when you need per-case IDs or tags.

Examples:
```python
@nox.session
@nox.parametrize("dependency", [
    nox.param("1.0", tags=["old"]),
    nox.param("2.0", tags=["new"]),
])
def tests(session, dependency):
    ...
```

## Session Object APIs

Nox calls each session function with an instance of `nox.sessions.Session`.

### Frequently used methods mentioned in the configuration docs
- `session.run(*args, env=None, external=False, silent=None)`: Run a command in the session environment.
- `session.install(*args)`: Install packages with pip inside the session environment.
- `session.conda_install(*args, channels=[...])`: Install packages with conda-family backends.
- `session.run_install(*args, env=None, external=False)`: Run install-time commands that still execute during `--install-only`.

### Frequently used attributes mentioned in the configuration docs
- `session.posargs`: Positional arguments forwarded after `--`.
- `session.venv_backend`: The backend actually selected for the session.
- `session.interactive`: Whether the current session is interactive.
- `session.virtualenv.location`: Filesystem path to the created virtualenv, when one exists.

### Common helper and control methods used in practical noxfiles
- `session.notify(name, posargs=None)`: Queue another session.
- `session.chdir(path)`: Change working directory.
- `session.log(message)`: Emit a log message.
- `session.warn(message)`: Emit a warning.
- `session.error(message)`: Abort the session.

### No-venv caution
`session.install()` without a virtualenv is deprecated because it mutates the global Python environment. In no-venv mode, use `session.run("pip", ...)` if you truly intend to modify the active interpreter.

## `nox.project` APIs

The configuration docs call out `nox.project` as the helper namespace for `pyproject.toml`-based workflows.

Useful helpers:
- `nox.project.load_toml(path)`: Load a `pyproject.toml` file or a PEP 723 script block.
- `session.install_and_run_script(path)`: Install dependencies from a PEP 723 script and run it.

## Global Noxfile Configuration

### `nox.options`
These Noxfile-level options map directly to CLI behavior.

Options covered by the configuration docs:
- `nox.options.envdir`
- `nox.options.sessions`
- `nox.options.pythons`
- `nox.options.keywords`
- `nox.options.tags`
- `nox.options.default_venv_backend`
- `nox.options.force_venv_backend`
- `nox.options.reuse_venv`
- `nox.options.reuse_existing_virtualenvs`
- `nox.options.stop_on_first_error`
- `nox.options.error_on_missing_interpreters`
- `nox.options.error_on_external_run`
- `nox.options.download_python`
- `nox.options.report`
- `nox.options.verbose`

Important behavior:
- CLI options override Noxfile options.
- If either `--sessions` or `--keywords` is given on the command line, both `nox.options.sessions` and `nox.options.keywords` from the Noxfile are ignored.

Examples:
```python
nox.options.envdir = ".cache"
nox.options.sessions = ["lint", "tests-3.12"]
nox.options.default_venv_backend = "uv|virtualenv"
```

### `nox.needs_version`
Use `nox.needs_version` at module scope to require a compatible Nox version.

Rules reflected in the configuration docs:
- It must be a string literal.
- It must be assigned at module level.
- It uses normal PEP 440 version specifiers.

Example:
```python
import nox

nox.needs_version = ">=2024.4.15"
```

## CLI Flags Closely Related To Noxfile Authoring

### File and session discovery
- `nox --noxfile something.py`
- `nox -l`
- `nox --list`
- `nox --list-sessions`
- `nox --usage tests`

### Session selection and filtering
- `nox -s tests`
- `nox --session tests`
- `nox -p 3.12`
- `nox --force-python 3.12`
- `nox -k "not lint"`
- `nox -t style`

### Backend and environment control
- `nox -db uv|virtualenv`
- `nox -fb conda`
- `nox --no-venv`
- `nox --reuse-venv=yes|no|always|never`
- `nox --reuse-existing-virtualenvs`
- `nox --no-reuse-existing-virtualenvs`
- `nox --download-python auto|never|always`

### Execution behavior
- `nox --stop-on-first-error`
- `nox --no-stop-on-first-error`
- `nox --error-on-missing-interpreters`
- `nox --no-error-on-missing-interpreters`
- `nox --error-on-external-run`
- `nox --no-error-on-external-run`
- `nox --install-only`
- `nox --report status.json`
- `nox -v`
- `nox --verbose`

## Compact Patterns

### Package session with forwarded args
```python
@nox.session
def tests(session):
    session.install("-e", ".[test]")
    session.run("pytest", *session.posargs)
```

### Multiple Pythons
```python
@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session):
    session.run("pytest")
```

### uv-first backend
```python
nox.options.default_venv_backend = "uv|virtualenv"
```

### uv-native install flow
```python
@nox.session(venv_backend="uv")
def tests(session):
    session.run_install(
        "uv",
        "sync",
        "--extra=test",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("pytest", *session.posargs)
```
