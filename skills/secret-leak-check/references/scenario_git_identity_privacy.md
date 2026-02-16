# Scenario: Git Identity Privacy Check

Run this check conditionally.

## When to run

1. Open-source project scenario -> check git email exposure risk.
2. Remote host is GitHub -> additionally check GitHub privacy email usage when privacy is desired.

## What to inspect

- Repository-local `user.email`
- Global `user.email` (if local is unset and global will be used)
- Remote URL host (GitHub vs others)

## Open-source email privacy rule

If configured email appears to be a personal/private mailbox and policy requires privacy, flag as risk and recommend using a project-safe address.

Examples of potentially personal domains:

- consumer mail domains (gmail/outlook/qq/163 etc.)
- employer domains tied to legal identity (based on org policy)

## GitHub-specific privacy rule

When remote is GitHub and privacy is required, recommend a GitHub no-reply email format:

- `<id>+<username>@users.noreply.github.com`
- or `<username>@users.noreply.github.com` (legacy format)

## Reporting

Return:

- whether project is treated as open-source
- whether remote is GitHub
- configured email source (local/global)
- privacy assessment and recommendation
