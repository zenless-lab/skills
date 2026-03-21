# Editing And Validation

Prefer safe, incremental noxfile edits.

## Before Editing
1. Read the existing `noxfile.py`.
2. Identify which sessions are used by CI.
3. Preserve session names unless the user asked for a rename.
4. Decide what will change before editing.

## Good Incremental Changes
- adding docstrings
- aligning Python versions with `requires-python`
- replacing ad-hoc commands with existing project tools
- introducing `uv|virtualenv` where the repo already uses uv
- simplifying duplicate install logic without changing session behavior

## Risky Changes
- renaming public sessions without updating CI
- changing dependency sources without confirming they are canonical
- forcing uv without installing it in CI
- replacing explicit commands with abstractions that hide behavior

## Validation Checklist
- run `nox --list`
- run `nox --usage <session>` for important sessions
- run at least one representative session when possible
- verify Python versions against package metadata and CI
- verify GitHub Actions templates still match session names and backend expectations
