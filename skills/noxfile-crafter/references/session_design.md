# Session Design

Design sessions for clarity first.

## Good Defaults
Common default sessions:
- `tests`
- `lint`
- `format`
- `typecheck`
- `docs`
- `build`

## Naming And User-Facing Behavior
- Keep public session names stable if CI or contributors already use them.
- Add docstrings so `nox --list` and `nox --usage` remain useful.
- Use `default=False` for destructive or special-purpose sessions.
- Forward user arguments with `session.posargs`.

## Python Selection
- Align session Python versions with `requires-python`, classifiers, or CI.
- Use `python=[...]` for normal interpreter matrices.
- Use `@nox.parametrize("python", ...)` only when you need to exclude or reshape combinations.

## Parameterization And Tags
- Use parameterization for real matrix coverage, not cosmetic complexity.
- Add `ids=[...]` or `nox.param(..., id=...)` when generated names become hard to use.
- Use tags only when they help contributors run meaningful subsets.

## Session Composition
- Use `requires=[...]` when ordering is a real dependency.
- Use `session.notify(...)` when a follow-up session should run after the current one.
- Avoid deeply nested helpers in small noxfiles. A short, explicit noxfile is easier to maintain.
