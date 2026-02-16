# Scenario: Commit Message Review

Review commit messages for leakage risk.

## Default behavior

If user does not explicitly disable commit message checking:

1. Inspect commit messages only for commits whose diffs are included in the current explicit scan range (for example, the commit range or list of SHAs provided to the scanner).
2. By default, do not expand this range to the full PR commit history; only use the explicitly provided scan range.
3. For each included commit, scan the commit subject and body for secrets/privacy leakage.

If user explicitly asks to scan all commits in a PR, scan commit messages for every commit in that PR range.

## What to detect in commit messages

- Direct tokens, API keys, passwords, bearer values
- Connection strings, hostnames with credentials, private endpoints
- Personal email address, phone number, legal/real full name when unnecessary
- Database/table details that should remain internal in open context

## Typical risky patterns

- "temp token: ..."
- "debug account/password"
- "my email is ..."
- "call me at ..."
- "created table x with columns ..." (when confidential)

## Result expectations

For each risky commit message include:

- Commit hash
- Risk excerpt (masked when needed)
- Risk reason
- Suggested remediation (amend/reword/squash/rewrite history)
