# Scope Selection Rules

Decide scan scope in this order.

## 1) Explicit user instruction has highest priority

If user explicitly specifies scan scope, follow it exactly:

- "Scan all files" -> run full scope scan, do not use diff-only fallback.
- "Scan only staged files" -> inspect staged diff only.
- "Scan commit messages only" -> run only commit message checks.

## 2) Default scope (when user does not specify)

Apply this default behavior:

1. Scan staged diff (`git diff --cached`).
2. Scan local-vs-remote diff using merge-base to compare only local changes (for example, `git diff @{upstream}...HEAD` to show changes introduced on the local branch).
3. If there are no staged files, scan all changed files in working tree (`unstaged + untracked` where relevant).

## 3) Remote baseline selection

When comparing local branch against remote:

1. Detect upstream branch first (for example `@{upstream}`).
2. Fetch latest remote refs when possible.
3. Compare against latest remote commit, not `HEAD~1`.

## 4) Requested path/range constraints

If user provides specific directories or files, apply scope logic only within that range. After resolving the range, convert it to a concrete file list for scanning.

## 5) Safety rule

If scope is ambiguous, use the broadest safe interpretation within user intent and clearly state assumptions in the report.
