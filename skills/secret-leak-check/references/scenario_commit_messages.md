# Scenario: Commit Message Review

Review commit messages for leakage risk.

## Default behavior

If user does not explicitly disable commit message checking:

1. Identify the remote tracking branch (for example, `@{upstream}`).
2. Inspect local commits that are reachable from local `HEAD` but not from the remote tracking branch (for example, `HEAD` but not `@{upstream}`).
3. Scan commit subject and body for secrets/privacy leakage.

Do not limit this to only the immediate previous commit.

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
