---
name: secret-scanner
description: Use this skill when instructed to perform a security scan, find leaked secrets, or check for PII in the codebase or git diffs. Trigger this even if the user broadly asks to check for security issues, leaked credentials, passwords, API tokens, emails, or sensitive data before committing.
---

# Secret Scanner Skill

This skill provides a multi-step workflow for scanning code, files, or git changes to detect leaked confidential information, including credentials, API keys, and Personally Identifiable Information (PII) like emails, phone numbers, and real names.

## Scanning Workflow

When a user requests a secret scan, you MUST follow this multi-step process:

### Step 1: Programmatic Scanning (If available)
If the user's environment has `gitleaks` or `trufflehog` installed (or can run them via docker), execute them first against the specified scope.
*   For instructions on running or configuring these tools, consult [references/programmatic_scanning.md](references/programmatic_scanning.md).
*   If neither tool is available, or if the scope is too small to warrant it (e.g., a simple uncommitted diff), you may skip to Step 2.

### Step 2: Chunk/File Level Manual Analysis
Gather the content of the specified scan scope (e.g., staged git changes, unstaged changes, specific files).
*   If you need help retrieving the content for the specified scope, consult [references/scope_commands.md](references/scope_commands.md) for shell commands.
*   Once retrieved, meticulously analyze the content chunk by chunk or file by file.
*   **List all potential leak points.** Look for:
    *   **Common Secrets:** `password`, `secret`, `token`, `api_key`, `access_key`, `jwt`, private cryptographic keys.
    *   **Common PII:** Electronic mail addresses (emails), phone numbers, real human names, physical addresses.
    *   *Note: This step focuses on gathering a raw list of candidates. Do not filter out false positives yet.*
    *   For a broader list of secret types and PII to look for, consult [references/secret_types.md](references/secret_types.md).

### Step 3: Deep Analysis & Triage
Focus deeply on the potential leaks identified in Step 2. For each identified potential leak, provide an analysis addressing:
1.  **Context:** What is the identified string?
2.  **False Positive Check:** Is it a dummy/placeholder value (e.g., `example@email.com`, `YOUR_API_KEY_HERE`, test data), or a real secret? Explain your reasoning.
3.  **Severity/Risk Level:** Assess the danger level (Critical, High, Medium, Low).
4.  **Remediation:** Suggest how to fix the issue (e.g., use `.env` file, environment variables, remove PII from logs, rotate the compromised key).

### Step 4: Verification of Scanned Scope
Conclude your response by explicitly listing the boundaries of what you scanned.
*   List the specific files, directories, or git commit ranges that were analyzed.
*   This ensures the user can verify if anything was missed or if the scan needs to be broadened.

## Common Secret Types

By default, focus your manual analysis on these common targets:

*   **API Tokens & Keys:** AWS, Google Cloud, Stripe, GitHub, Slack, OpenAI, etc.
*   **Authentication:** Passwords, connection URIs, JWTs, Bearer tokens.
*   **Cryptography:** RSA/SSH Private Keys, SSL certificates.
*   **PII:** Personal email addresses, personal phone numbers, real names associated with user data (ignore clear placeholders like `john.doe@example.com` or standard author names in standard license files unless requested).

For a comprehensive catalog of secrets and their corresponding risk levels, refer to [references/secret_types.md](references/secret_types.md).

### Adaptive Detection
**Crucially, you are not limited to the types of secrets explicitly listed.** You must use your judgment and contextual awareness to identify ANY information that appears to be confidential, proprietary, or uniquely sensitive, including but not limited to:
*   Unusual strings of high entropy in variable assignments.
*   Internal infrastructure URLs or internal IP addresses.
*   Proprietary algorithmic parameters, internal business logic details, or unreleased product names if they appear out of place.
*   Any other data that, if leaked, could cause security, privacy, or business risk to the user or organization.
