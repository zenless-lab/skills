# Scenario: Diff and Staging Scan

Use this reference when scan scope is based on changes, not full repository.

## Objectives

1. Catch newly introduced secret/privacy leaks quickly.
2. Prioritize review on content likely to be committed or recently diverged from remote.

## Checklist

1. Inspect staged diff first.
2. Inspect local-vs-latest-remote diff for current branch.
3. If no staged files exist, inspect all changed files in working tree.

## Detection focus in diffs

Prioritize added lines (`+`) and newly created files.

Also inspect context lines when:

- an added reference points to existing sensitive value,
- refactor moved secrets from one file to another,
- renamed files may retain leaked content.

## Typical high-risk locations

- Environment/config files (`.env`, `*.yaml`, `*.json`, `*.toml`, `*.ini`)
- CI/CD definitions and deployment manifests
- Test fixtures and sample payload files
- Script outputs or generated artifacts accidentally added to VCS

## Required output fields

For each finding in this scenario include:

- Diff scope (`staged` / `local-vs-remote` / `working-tree-change`)
- File path and nearby marker (line/diff hunk)
- Whether value appears newly added or pre-existing
