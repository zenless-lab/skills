import nox


nox.needs_version = ">=2024.4.15"
nox.options.sessions = ["lint", "tests"]
nox.options.default_venv_backend = "uv|virtualenv"

PYTHONS = ["3.11", "3.12"]


@nox.session
def lint(session: nox.Session) -> None:
    """Run lint checks."""
    session.install("-e", ".[test]")
    session.run("ruff", "check", ".", *session.posargs)


@nox.session(python=PYTHONS)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.install("-e", ".[test]")
    session.run("pytest", *session.posargs)
