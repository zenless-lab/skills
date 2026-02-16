# Scenario: Diff and Staging Scan

Use this reference when scan scope is based on changes, not full repository.

## Objectives

1. Catch newly introduced secret/privacy leaks quickly.
2. Prioritize review on content likely to be committed relative to local latest commit (`HEAD`).

## Checklist

1. Inspect staged diff first (index vs `HEAD`, for example `git diff --cached` / `git diff --staged`).
2. Inspect unstaged working tree changes (working tree vs index, for example `git diff`).
3. If no staged files exist, also inspect the full working tree diff against local `HEAD` (for example `git diff HEAD`).

## Explicit PR all-commits mode

Run this mode only when user explicitly asks to scan all commits in a PR.

1. Keep normal working tree checks (staged + unstaged/untracked when relevant).
2. Identify PR commit range.
3. Scan each commit in that range one by one:
  - commit diff content,
  - commit message leakage risk.

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

- Diff scope (`staged` / `working-tree-vs-HEAD` / `working-tree-change` / `pr-commit`)
- File path and nearby marker (line/diff hunk)
- Whether value appears newly added or pre-existing
