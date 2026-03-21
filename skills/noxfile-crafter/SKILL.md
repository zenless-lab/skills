---
name: noxfile-crafter
description: Use this skill when you need to create, edit, review, or modernize a project's noxfile.py, define Nox sessions, align Python automation with pyproject.toml/setup.cfg/requirements files, or wire Nox into GitHub Actions. Trigger this even when the user asks to automate tests, linting, typing, docs, packaging, or multi-Python CI without explicitly naming Nox, and when migrating from tox, Make, shell scripts, or ad-hoc CI jobs.
---

# Noxfile Crafter

This skill helps the agent create or update noxfile.py files that match the project's packaging metadata, dependency sources, Python support policy, and CI workflow.

## Context & Domain Knowledge
- Nox configuration should reflect the project's actual source of truth: pyproject.toml, setup.py, setup.cfg, requirements files, lockfiles, and CI workflows.
- Always inspect an existing noxfile.py before changing it. Preserve working session names and behavior unless there is a concrete reason to change them.
- Prefer a small set of focused sessions with docstrings, predictable names, and explicit dependency installation.
- If the project uses uv, or uv is already available in the environment, prefer a uv-first backend. The safest shared default is `nox.options.default_venv_backend = "uv|virtualenv"` so local runs prefer uv while other environments still have a fallback.
- Use session tags, requires, notify, and posargs only when they simplify the workflow. Avoid making a simple project's noxfile overly dynamic.
- Keep GitHub Actions aligned with the noxfile's Python versions, selected sessions, and backend assumptions.
- Keep the main instructions short. If anything is unclear, consult the topic-specific files in `references/` before changing the workflow.

## Workflow / Instructions
1. **Discover the project state**:
   - Inspect `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt`, `requirements/*.txt`, `tox.ini`, `.python-version`, `uv.lock`, and `.github/workflows/`.
   - Extract supported Python versions, dependency groups or extras, test commands, lint or type or doc or build tools, and whether the project is package-based or script-based.
   - Detect uv usage from `pyproject.toml`, `uv.lock`, docs, CI, or installed tooling.
2. **Inspect existing Nox automation**:
   - If `noxfile.py` already exists, read it first.
   - Record existing session names, default sessions, Python matrices, backend settings, reusable helpers, and CI-facing expectations.
   - Create a change plan before editing. Preserve compatible behavior unless the user asked for a redesign.
3. **Choose the dependency and backend strategy**:
   - Prefer `pyproject.toml` dependency groups or extras when available.
   - Use requirements files only when they are the established source of truth.
   - If uv is in use or already installed, default to `nox.options.default_venv_backend = "uv|virtualenv"`.
   - Use per-session backends only when the project truly needs them, such as Conda-based scientific stacks.
4. **Design sessions deliberately**:
   - Start with the smallest useful set: `tests`, `lint`, `format`, `typecheck`, `docs`, `build`, or project-specific equivalents.
   - Add docstrings so `nox --list` and `nox --usage` stay informative.
   - Use `session.posargs` to forward user-provided arguments.
   - Use `requires=` for deterministic prerequisites and `session.notify()` only for intentionally queued follow-up work.
5. **Implement or update the noxfile**:
   - Keep imports and helpers minimal.
   - Prefer explicit install commands over opaque wrappers.
   - Match session commands to the repo's existing tooling rather than introducing replacements by default.
   - If the repo is uv-native, prefer `session.run_install("uv", "sync", ...)` patterns. Otherwise keep standard `session.install(...)` flows.
6. **Align GitHub Actions**:
   - Use the bundled templates in `assets/` as starting points.
   - Ensure the workflow installs required tools, mirrors Python support, and only runs sessions that actually exist.
   - If the noxfile depends on uv semantics, install uv in CI instead of silently falling back.
7. **Validate before finishing**:
   - Run `nox --list` and `nox --usage <session>` when possible.
   - Run one or more representative sessions if the environment allows it.
   - Check for mismatches between declared Python versions, package metadata, and CI matrices.

When you need details, check the matching reference file instead of guessing:
- project discovery and source-of-truth selection: `references/project_discovery.md`
- session naming, structure, parameterization, and user-facing behavior: `references/session_design.md`
- backend, install, and uv strategy: `references/backends_and_installs.md`
- GitHub Actions and CI alignment: `references/github_actions.md`
- incremental edits and validation: `references/editing_and_validation.md`

## Troubleshooting & Edge Cases
- If the project has no package metadata, build sessions around the existing command set and requirements files instead of inventing extras.
- If Python versions are unclear, prefer `requires-python` from `pyproject.toml` or classifiers over guesswork.
- If uv is installed locally but not guaranteed in CI, either install uv in GitHub Actions or use `uv|virtualenv` as the backend fallback.
- If the repo already has a complex noxfile, refactor incrementally and keep stable public session names whenever possible.
- If a session runs external tools not installed in the environment, either install them in the session or intentionally rely on `external=True` where appropriate.

## Bundled Resources
- [Nox API Reference](references/api_reference.md): Compact but complete reference for the APIs and Noxfile options covered by the upstream configuration docs.
- [Project Discovery](references/project_discovery.md): What to inspect first and how to identify the real source of truth.
- [Session Design](references/session_design.md): Session naming, docstrings, Python matrices, parameterization, tags, and defaults.
- [Backends And Installs](references/backends_and_installs.md): `virtualenv`, `uv`, conda-family backends, reuse rules, and install strategies.
- [GitHub Actions Guidance](references/github_actions.md): How to keep CI and the noxfile aligned.
- [Editing And Validation](references/editing_and_validation.md): Safe change planning, backward-compatible edits, and validation checklist.
- [GitHub Actions CI Template](assets/github_actions_ci.yml): Standard Python matrix workflow for Nox projects.
- [GitHub Actions uv CI Template](assets/github_actions_uv_ci.yml): uv-first workflow for repos that use uv explicitly.
- [Pyproject-oriented Noxfile Template](assets/noxfile_pyproject_template.py): A reusable starting point for typical package-based projects.
