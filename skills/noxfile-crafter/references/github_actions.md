# GitHub Actions Guidance

Keep CI and the noxfile in sync.

## Alignment Rules
- Use the same Python versions in GitHub Actions and the noxfile.
- Run only session names that actually exist.
- If the noxfile depends on uv behavior, install uv in CI explicitly.
- Cache the package manager the project actually uses.
- Prefer one clear matrix job over duplicated workflows when possible.

## Template Selection
- Use `assets/github_actions_ci.yml` for standard pip-based or fallback-friendly setups.
- Use `assets/github_actions_uv_ci.yml` when the repository is intentionally uv-first.

## Common Failure Modes
- CI runs a session name that was renamed in `noxfile.py`.
- CI pins Python versions that no longer match `requires-python`.
- The noxfile assumes uv, but CI never installs uv.
- The workflow matrix and `nox.options.sessions` drift apart over time.
