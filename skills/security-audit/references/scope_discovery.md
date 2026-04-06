# Scope Discovery

Load this file only when you need concrete command help for resolving the audit boundary.

## Git Scopes

Run all git inspection commands with `--no-pager` when reading history or diffs.

Use three views deliberately:

- `--name-only` to resolve the file boundary
- `--stat` to estimate review cost and choose deep versus fast review
- full diff output to inspect actual content when semantic review is needed

### Staged

Use staged content when the user asks for the submit-ready delta:

```bash
git --no-pager diff --cached --name-only
git --no-pager diff --cached --stat
git --no-pager diff --cached
```

Command guidance:

- `git --no-pager diff --cached --name-only`
  Returns only the staged file paths. Use this first to construct the scan list.
- `git --no-pager diff --cached --stat`
  Shows file counts and insertion or deletion volume. Use it to decide whether the change is small enough for deep review.
- `git --no-pager diff --cached`
  Shows the exact staged patch. Use it when semantic review should be limited to what will actually be committed.

Practical notes:

- `--cached` means the index, not the working tree. This is the correct boundary for pre-commit style auditing.
- A file may have both staged and unstaged edits. If the user asks for a commit-time audit, the staged view is authoritative.
- If the staged file list is empty, report that the staged boundary resolved to no files instead of silently falling back to `changed`.

### Changed

Use changed content when the user asks for modified but not necessarily staged files:

```bash
git --no-pager diff --name-only
git --no-pager diff --stat
git --no-pager diff
git --no-pager ls-files --others --exclude-standard
```

Combine tracked modifications and untracked files when building the file list.

Command guidance:

- `git --no-pager diff --name-only`
  Lists tracked files with unstaged modifications relative to the index.
- `git --no-pager diff --stat`
  Gives a compact size summary for tracked unstaged modifications.
- `git --no-pager diff`
  Shows the actual unstaged patch content.
- `git --no-pager ls-files --others --exclude-standard`
  Lists untracked files while honoring `.gitignore` and standard excludes.

Practical notes:

- `git diff` without `--cached` does not include staged changes.
- If the user wants the full current working set, combine:
  tracked unstaged changes, staged changes if relevant, and untracked files.
- Untracked files often carry the highest secret risk because they have not gone through repository tooling yet.

### Commit `<hash>`

Resolve one commit or a commit range:

```bash
git --no-pager show --stat --name-only <hash>
git --no-pager show <hash>
git --no-pager diff <hash>^ <hash> --name-only
```

For merge commits, inspect the commit itself with `git --no-pager show <hash>`.

Command guidance:

- `git --no-pager show --stat --name-only <hash>`
  Fast summary view for the commit. Use it to resolve touched files and review scale.
- `git --no-pager show <hash>`
  Full commit patch plus metadata. Use it when semantic review should follow the exact historical commit content.
- `git --no-pager diff <hash>^ <hash> --name-only`
  Explicitly compares the commit against its first parent and returns only changed file names.

Practical notes:

- `<hash>^` means the first parent. This is correct for most non-merge commits.
- For merge commits, `git show <hash>` is usually more informative than forcing a single-parent diff, because the merge context matters.
- If the user gives a commit range rather than one hash, use the same pattern across the range and make the chosen interpretation explicit in the report.

### PR `<id>`

Prefer the repository's native tooling if available, such as `gh` or GitLab CLI. If not, resolve the target branch and compare against the merge base:

```bash
git --no-pager branch -r
git --no-pager merge-base HEAD origin/main
git --no-pager diff --name-only "$(git merge-base HEAD origin/main)"...HEAD
git --no-pager diff "$(git merge-base HEAD origin/main)"...HEAD
```

Replace `origin/main` with the actual base branch when known.

Command guidance:

- `git --no-pager branch -r`
  Lists remote branches so you can infer likely base branches such as `origin/main` or `origin/master`.
- `git --no-pager merge-base HEAD origin/main`
  Computes the common ancestor between the current branch and the base branch. This is the anchor for PR-style comparison.
- `git --no-pager diff --name-only "$(git merge-base HEAD origin/main)"...HEAD`
  Returns the PR file set. Use this for the scan boundary.
- `git --no-pager diff "$(git merge-base HEAD origin/main)"...HEAD`
  Returns the PR patch content. Use this for semantic review.

Practical notes:

- The three-dot diff is the correct review boundary for branch or PR style work because it compares from the merge base, not from the current tip of the base branch alone.
- If repository-native tooling such as `gh pr diff <id>` exists and the user gave a concrete PR ID, prefer that because it reflects the platform's actual PR boundary.
- When the base branch is uncertain, state the assumption explicitly instead of guessing silently.

## Filesystem Scopes

### Entire Repo

Prefer a file-aware enumerator over raw `find` when available:

```bash
rg --files .
```

Fallback:

```bash
find . -type f
```

Command guidance:

- `rg --files .`
  Fastest general-purpose file enumerator in most developer environments. It is usually preferred because it is much faster than `find`.
- `find . -type f`
  Portable fallback when `rg` is unavailable.

Practical notes:

- `rg --files` typically respects ignore files such as `.gitignore`, which is often desirable for repository-centered review.
- `find` will return ignored and generated files unless extra filters are added. Use it carefully if the repository contains build output, vendored dependencies, or cache directories.
- For full-repo audits, apply policy-based exclusions after enumeration rather than assuming every file should be scanned.

### Directory

```bash
rg --files ./path/to/dir
```

Fallback:

```bash
find ./path/to/dir -type f
```

Command guidance:

- `rg --files ./path/to/dir`
  Preferred directory-scoped enumerator when the target should follow normal ignore behavior.
- `find ./path/to/dir -type f`
  Fallback when `rg` is unavailable or when you need more explicit filesystem traversal.

Practical notes:

- Directory-scoped review is useful when the user points to a service, module, or docs folder instead of a git boundary.
- If the directory contains generated assets or binary exports, split those into fast review or skipped coverage early.

### Specific File

Use the exact user-provided path. Confirm that the path exists before scanning.

Practical notes:

- Do not widen a specific-file request into a directory scan unless the user asks for related context.
- If the file is binary, convert it to text first when possible and record whether the original binary file was only partially covered.

## Practical Filtering

Exclude paths that are clearly outside the intended boundary, especially when the user asks for targeted review. Honor project ignore rules from local policy files before constructing the final scan list.

Examples of filters that often matter:

- `.gitleaks.toml` allowlists or path exclusions
- generated output directories
- vendored dependencies
- submodules when the user only wants first-party code
- archives or binary blobs that cannot be converted locally

Before scanning, make the resolved boundary explicit:

- the scope type
- the command or method used to resolve it
- the final file list or the rule used to generate it
