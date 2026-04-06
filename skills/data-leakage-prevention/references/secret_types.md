# Secret Types

Load this file only when severity is unclear after reading the content and surrounding context.

This file is a classification aid, not a complete catalog. Secrets and privacy leaks are not limited to the examples below. Prefer the semantic severity rules in `SKILL.md` when the context is clear.

## Typical High-Severity Secrets

Examples:

- cloud access keys
- private keys
- signing keys
- production API tokens
- database passwords for live systems
- SSH credentials
- CI credentials with release or deployment scope

Default severity:

- usually `Critical`
- downgrade only when the value is clearly fake, revoked, sample-only, or unusable

## Typical Sensitive Personal Data

Examples:

- personal email addresses
- phone numbers
- government identifiers
- passport or driver-license numbers
- home addresses
- employee or customer identifiers tied to a real person

Default severity:

- `High` when clearly real and attributable
- `Medium` when incomplete, masked, or weakly attributable

## Context-Dependent Findings

Examples:

- internal hostnames
- Slack webhooks
- test environment tokens
- service account identifiers without secrets
- metadata inside exported documents
- partial credentials

Default severity:

- `Medium` when the risk is plausible but not fully validated
- `Low` when the data looks synthetic, low-impact, or operationally harmless

## Common False-Positive Patterns

Examples:

- mock secrets in tests
- fixture phone numbers such as `555`
- documentation examples copied from vendor docs
- hashes, UUIDs, or opaque identifiers with no authentication value
- placeholder emails like `user@example.com`

These should not be auto-dismissed. Keep them in a separate `suspected false positives` section when uncertainty remains.
