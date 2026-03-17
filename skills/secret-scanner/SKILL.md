---
name: secret-scanner
description: Use this skill when instructed to perform a security scan, find leaked secrets, or check for PII in the codebase or git diffs. Trigger this even if the user broadly asks to check for security issues, leaked credentials, passwords, API tokens, emails, or sensitive data before committing.
---

# Secret Scanner Skill

This skill provides a multi-step workflow for scanning code, files, or git changes to detect leaked confidential information, including credentials, API keys, and Personally Identifiable Information (PII) like emails, phone numbers, and real names.

## Recommended Scanning Workflow

The following guidelines outline a standard multi-step process for effectively scanning code for secrets:

### Programmatic Scanning
When programmatic scanning is preferred or requested, tools like `gitleaks` or `trufflehog` should be used.
*   For instructions on running or configuring these tools, consult [references/programmatic_scanning.md](references/programmatic_scanning.md).

### Chunk/File Level Manual Analysis
When reviewing the content of a specified scope (e.g., staged git changes, unstaged changes, specific files), it helps to list all potential leak points first.
*   To retrieve the content for the specified scope, consult [references/scope_commands.md](references/scope_commands.md) for shell commands.
*   Look for:
    *   **Common Secrets:** `password`, `secret`, `token`, `api_key`, `access_key`, `jwt`, private cryptographic keys.
    *   **Common PII:** Electronic mail addresses (emails), phone numbers, real human names, physical addresses.
    *   For a broader list of secret types and PII, consult [references/secret_types.md](references/secret_types.md).

### Deep Analysis & Triage
Potential leaks can be evaluated by providing an analysis addressing:
1.  **Context:** What is the identified string?
2.  **False Positive Check:** Is it a dummy/placeholder value (e.g., `example@email.com`, `YOUR_API_KEY_HERE`, test data), or a real secret?
3.  **Severity/Risk Level:** Assess the danger level (Critical, High, Medium, Low).
4.  **Remediation:** Suggest how to fix the issue (e.g., use `.env` file, environment variables, remove PII from logs, rotate the compromised key).

### Scope Verification
It is best practice to conclude a scan by explicitly listing the boundaries of what was scanned (specific files, directories, or git commit ranges). This ensures transparency.

## Common Secret Types

By default, focus your manual analysis on these common targets:

*   **API Tokens & Keys:** AWS, Google Cloud, Stripe, GitHub, Slack, OpenAI, etc.
*   **Authentication:** Passwords, connection URIs, JWTs, Bearer tokens.
*   **Cryptography:** RSA/SSH Private Keys, SSL certificates.
*   **PII:** Personal email addresses, personal phone numbers, real names associated with user data (ignore clear placeholders like `john.doe@example.com` or standard author names in standard license files unless requested).

For a comprehensive catalog of secrets and their corresponding risk levels, refer to [references/secret_types.md](references/secret_types.md).

### Adaptive Detection
Secret types are not limited to explicit lists. Contextual awareness is necessary to identify information that appears to be confidential, proprietary, or uniquely sensitive, including but not limited to:
*   Unusual strings of high entropy in variable assignments.
*   Internal infrastructure URLs or internal IP addresses.
*   Proprietary algorithmic parameters, internal business logic details, or unreleased product names if they appear out of place.
*   Any other data that, if leaked, could cause security, privacy, or business risk to the user or organization.
