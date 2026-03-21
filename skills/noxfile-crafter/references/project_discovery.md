# Project Discovery

Inspect the project before touching `noxfile.py`.

## Read These First
- `pyproject.toml`
- `setup.py`
- `setup.cfg`
- `requirements.txt`
- `requirements/*.txt`
- `tox.ini`
- `uv.lock`
- `.python-version`
- `.github/workflows/*.yml`
- existing `noxfile.py`

## Facts To Extract
- supported Python versions
- package layout and whether editable installs are expected
- dependency groups, optional dependencies, and lockfile usage
- current test, lint, format, type, docs, and build commands
- CI-facing session names that should remain stable
- whether uv, conda, or another backend is already part of the workflow

## Source Of Truth Priority
Use this order unless the repository clearly establishes a different one:
1. `pyproject.toml`
2. `setup.cfg` or `setup.py`
3. lockfiles and requirements files
4. CI workflows and project docs

Do not invent extras, dependency groups, or Python support ranges that are not already supported by the project.
