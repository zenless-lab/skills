# Scope Selection Rules

Decide scan scope in this order.

## 1) Explicit user instruction has highest priority

If user explicitly specifies scan scope, follow it exactly:

- "Scan all files" -> run full scope scan, do not use diff-only fallback.
- "Scan only staged files" -> inspect staged diff only.
- "Scan commit messages only" -> run only commit message checks.
- "Scan all commits in this PR" -> scan staged/unstaged changes (if any) and scan every commit in the PR range one by one.

## 2) Default scope (when user does not specify)

Apply this default behavior:

1. Scan staged diff (index vs `HEAD`, for example `git diff --cached` / `git diff --staged`).
2. Scan unstaged working tree diff (working tree vs index, for example `git diff`, which excludes already-staged changes).
3. If there are no staged files and a broader scope is needed, scan all changed files in the working tree by taking the union of staged, unstaged, and untracked files (file sets from `git diff --cached`, `git diff`, and untracked file listing), without re-counting changes already covered by the previous diffs.
4. Do not scan all PR commits unless user explicitly requests it.

## 3) PR all-commits mode (explicit only)

When user explicitly asks to scan all commits in a PR:

1. Detect PR commit range using upstream/default branch merge base when possible.
2. Scan each commit in the PR range commit-by-commit (diff + commit message).
3. Keep staged/unstaged working tree scans in addition to commit-range scans.

## 4) Remote baseline selection

When comparing local branch against remote:

1. Detect upstream branch first (for example `@{upstream}`).
2. Fetch latest remote refs when possible.
3. Compare against latest remote commit, not `HEAD~1`.

This remote baseline logic applies only when user explicitly requests remote/PR commit-range scanning.

## 5) Requested path/range constraints

If user provides specific directories or files, apply scope logic only within that range. After resolving the range, convert it to a concrete file list for scanning.

## 6) Safety rule

If scope is ambiguous, use the broadest safe interpretation within user intent and clearly state assumptions in the report.
