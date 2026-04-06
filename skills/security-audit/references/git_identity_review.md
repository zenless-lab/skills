# Git Identity Review

Load this file only when the audit scope is git-based and you need exact command help.

## Current Local Identity

Inspect the identity configured in the current repository first:

```bash
git config user.name
git config user.email
```

Command guidance:

- `git config user.name`
  Reads the repository-local author name if one is set. This is the most relevant value for an imminent commit in the current repository.
- `git config user.email`
  Reads the repository-local author email if one is set.

If a value is unset locally, inspect the effective value:

```bash
git config --get user.name
git config --get user.email
git config --global --get user.name
git config --global --get user.email
```

Command guidance:

- `git config --get user.name`
  Returns the effective value resolved from the available config layers for the current context.
- `git config --get user.email`
  Returns the effective email value resolved for the current context.
- `git config --global --get user.name`
  Reads the user's global default name. This is useful when the repository-local value is absent and the commit would inherit a personal identity accidentally.
- `git config --global --get user.email`
  Reads the user's global default email.

Practical notes:

- Start with repository-local config because that is what the current repository will use first.
- If local config is missing, global identity often explains why a user is about to leak a personal mailbox into a work repository.
- Missing values are not themselves a leak. The risk is in the effective identity that git will actually use.

## Historical Identities In Scope

Use the audit boundary to decide which commits to inspect.

### Staged Or Changed

Review recent local history that is relevant to the branch:

```bash
git --no-pager log --format="%an <%ae>" -n 20
```

Command guidance:

- `git --no-pager log --format="%an <%ae>" -n 20`
  Prints the author name and email for the most recent 20 commits. Use this to detect mixed identities or accidental drift in a local branch before a new commit is created.

Practical notes:

- This does not prove the exact staged content author, because staged changes are not yet committed.
- It is still useful for spotting an obvious mismatch, such as recent work commits from `alice@company.com` while the current config is `alice.personal@gmail.com`.
- Adjust `-n 20` if the branch is unusually short or long, but keep the inspection bounded.

### Commit `<hash>`

```bash
git --no-pager log --format="%an <%ae>" <hash>^..<hash>
```

Command guidance:

- `git --no-pager log --format="%an <%ae>" <hash>^..<hash>`
  Prints the author identity for the specified commit. Use this when the audit target is a single historical commit.

Practical notes:

- `<hash>^..<hash>` scopes the log to the commit itself relative to its first parent.
- For a non-merge commit, this is usually enough to determine whether the commit metadata contains sensitive personal information.
- If the user gives a range rather than one commit, inspect the full range and report that interpretation explicitly.

### PR Or Branch Delta

```bash
git --no-pager log --format="%an <%ae>" "$(git merge-base HEAD origin/main)"..HEAD
```

Replace `origin/main` with the actual base branch when known.

Command guidance:

- `git --no-pager log --format="%an <%ae>" "$(git merge-base HEAD origin/main)"..HEAD`
  Prints all author identities that appear in the current branch delta relative to the base branch. Use this for PR-style audits or branch reviews.

Practical notes:

- The merge base anchors the branch delta to the same review boundary used for PR diffs.
- If the repository uses `origin/master`, a release branch, or another integration branch, substitute that branch explicitly.
- If a hosting tool such as `gh` exposes the exact PR base branch, prefer that source over guessing.

## How To Interpret Identity Risk

Look for both direct leakage and policy mismatch.

Common signals:

- a personal mailbox in a repository that should use organization-managed addresses
- a full legal name in a repository that expects pseudonyms, handles, or team aliases
- mixed author identities in the same branch, suggesting accidental config drift
- emails embedding employee IDs, phone numbers, or other internal identifiers
- machine-generated commits using a personal identity rather than a service account

Context matters:

- an organization address with a full name is often normal in an internal repository
- an open-source repository may intentionally allow real names and personal email addresses
- a noreply address may still be acceptable if it matches repository policy
- a service account identity may be legitimate for automation and should not be flagged just because it is unusual

## What To Flag

Flag identities that appear to expose personal information inappropriately, for example:

- a real full name when the repository expects pseudonymous or organization-scoped identities
- a personal mailbox instead of an organization mailbox
- addresses containing employee IDs, phone numbers, or other embedded personal data
- mixed identities suggesting accidental leakage from local personal git config

Do not assume every personal-looking identity is a policy violation. Report the context and why it may be sensitive.

## Reporting Guidance

When reporting git identity issues, make the reasoning explicit:

- the scope you inspected
- the command or method used
- the identity value observed
- why it may be sensitive or out of policy
- whether it is a current configuration issue, a historical commit issue, or both

Good report language:

- `git config user.email` resolves to a personal mailbox in a repository that otherwise uses organization-scoped identities
- branch history contains mixed author emails, suggesting local git configuration drift
- commit metadata includes a real full name and personal address; treat as potential PII exposure unless the repository policy allows it

Avoid overclaiming:

- do not call every personal-looking name a leak
- do not assume a noreply address is unsafe
- do not infer repository policy unless the repository or user states it clearly
