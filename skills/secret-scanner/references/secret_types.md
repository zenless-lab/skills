# Comprehensive Secret and PII Types

This document provides a comprehensive list of confidential information types, including credentials, keys, and Personally Identifiable Information (PII), categorized by their risk levels.

## Critical Risk (High Impact, Immediate Action Required)
These secrets grant direct access to critical infrastructure, sensitive data, or financial resources.

*   **Cloud Provider Credentials:** AWS Access/Secret Keys, Google Cloud Service Account JSONs/API Keys, Azure Subscription IDs/Secrets, AliCloud Keys.
*   **Database Credentials:** Usernames and passwords, Connection strings (URIs) for production databases (PostgreSQL, MySQL, MongoDB, Redis, etc.).
*   **Private Keys:** SSH private keys (RSA, Ed25519, etc.), SSL/TLS private certificates, GPG private keys, Cryptographic signing keys (JWT secrets).
*   **Payment/Financial API Keys:** Stripe Secret Keys, PayPal Secret Keys, Braintree Tokens, Square Access Tokens.
*   **Source Code Infrastructure:** GitHub Personal Access Tokens (PATs), GitLab Tokens, Bitbucket Tokens, CI/CD Secrets (CircleCI, Travis, Jenkins tokens).
*   **Authentication & Identity Providers:** Okta API keys, Auth0 tokens, Firebase secret keys.

## High Risk (Significant Impact)
These secrets grant access to third-party services, internal tools, or could lead to significant privacy breaches.

*   **Messaging/Communication APIs:** Slack Bot/Webhook Tokens, Discord Tokens, Twilio API Keys, SendGrid Tokens.
*   **Social Media & Third-Party APIs:** Twitter API Keys, Facebook/Meta Graph API Secrets, OpenAI/Anthropic API Keys.
*   **Monitoring & Analytics:** Datadog API keys, New Relic App Tokens, Sentry Admin Tokens, Google Analytics backend keys.
*   **High-Sensitivity PII:**
    *   Social Security Numbers (SSN), National ID numbers.
    *   Driver's License numbers, Passport numbers.
    *   Full Credit Card Numbers (PAN), Bank Account numbers.
    *   Detailed health or medical records (HIPAA covered).

## Medium Risk (Moderate Impact)
Exposure may cause localized disruption, partial data disclosure, or facilitate targeted social engineering.

*   **Non-Production Credentials:** Staging/development database passwords, test environment API keys (though risk elevates if they share access with prod).
*   **Internal Service URLs with Auth:** URLs containing query parameter tokens (e.g., `https://internal.service.com/?token=abc`).
*   **General PII:**
    *   Full Real Names combined with other identifiers.
    *   Personal Email Addresses.
    *   Personal Phone Numbers.
    *   Physical Home Addresses.
    *   Date of Birth.

## Low Risk (Context-Dependent Impact)
Information that is often public or low-value but should generally not be hardcoded or logged unnecessarily.

*   **Public Identifiers:** Public Keys (SSH public keys), SSL/TLS Public Certificates.
*   **Business Contact Info:** Corporate email addresses (e.g., `john.doe@company.com` - unless mass scraped), company phone numbers, office addresses.
*   **Identifiers:** Internal user IDs, UUIDs, Database primary keys (without corresponding credentials).
