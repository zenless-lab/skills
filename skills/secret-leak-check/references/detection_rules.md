# Detection Rules

Use these rules to classify and score findings.

## Category A: Traditional Secrets

Detect likely exposures of:

- API keys and access tokens
- Cloud credentials and service principals
- Database passwords and connection strings
- Private keys, certificates with private material
- Bearer/Auth headers embedded in code or docs

### Signals

1. High-entropy strings near auth-related keywords (`token`, `secret`, `apikey`, `password`, `Authorization`).
2. Known provider prefixes/patterns (for example GitHub, AWS, Azure, GCP, Stripe-like formats).
3. Multi-part secrets in URL/userinfo fields.

### False-positive reduction

- Ignore obvious placeholders (`YOUR_TOKEN_HERE`, `example_key`, `xxxxx`).
- Downgrade risk when value is clearly synthetic test data and non-functional.

## Category B: Internal Structure Leakage

Detect information that may expose internal architecture beyond acceptable disclosure:

- Detailed database schema DDL with sensitive naming
- Internal table/column mapping revealing regulated or business-critical entities
- Internal service topology, private hostnames, private subnets

### Escalation conditions

- Appears in public-facing repository context
- Combined with credentials, endpoint URLs, or admin instructions

## Category C: Privacy/PII Leakage

Detect personal data exposure, including:

- Personal email addresses
- Phone numbers
- Real-name identifiers when unnecessary

### Notes

- Names alone can be ambiguous; increase confidence when accompanied by contact info or explicit identity context.
- For logs/samples, check whether data belongs to real users.

## Severity Mapping

- **critical**: directly usable secret/credential/private key
- **high**: likely real PII or sensitive internal structure with exploitation value
- **medium**: suspicious but uncertain secret/PII signal
- **low**: weak indicator or likely placeholder

## Remediation Guidelines

1. Remove leaked data from tracked files.
2. Rotate credentials immediately if exposure is plausible.
3. Rewrite history when secret was committed (`rebase`/`filter-repo`/equivalent process).
4. Replace real PII with synthetic fixtures.
5. Add preventive controls (secret scanning hooks, CI checks, masked templates).
