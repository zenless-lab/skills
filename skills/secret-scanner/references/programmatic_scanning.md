# Programmatic Scanning Tools (Gitleaks & TruffleHog)

Programmatic scanning is the first line of defense. The following instructions cover configuration and usage of the two most prominent tools: Gitleaks and TruffleHog.

## 1. Gitleaks

Gitleaks is a SAST tool for detecting hardcoded secrets like passwords, API keys, and tokens in git repos.

### Installation
*   **MacOS:** `brew install gitleaks`
*   **Docker:**
    ```bash
    docker pull zricethezav/gitleaks:latest
    docker run -v ${PWD}:/path zricethezav/gitleaks:latest dir /path
    ```

### Usage
*   **Scan a local Git repository (history):**
    ```bash
    gitleaks git -v
    ```
*   **Scan directories or files (no git history needed):**
    ```bash
    gitleaks dir -v <path>
    ```
*   **Generate a JSON report:**
    ```bash
    gitleaks dir -v <path> --report-path findings.json --report-format json
    ```

### CI/CD Integration
**GitHub Actions (Gitleaks):**
```yaml
name: gitleaks
on: [pull_request, push, workflow_dispatch]
jobs:
  scan:
    name: gitleaks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Pre-commit Hook:**
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.2
    hooks:
      - id: gitleaks
```

---

## 2. TruffleHog

TruffleHog (v3) is a powerful secrets Discovery, Classification, and Validation tool. It can actively verify if secrets are live by calling external APIs.

### Installation
*   **MacOS:** `brew install trufflehog`
*   **Docker:**
    ```bash
    docker run --rm -it -v "$PWD:/pwd" trufflesecurity/trufflehog:latest git file:///pwd
    ```

### Usage
*   **Scan a local git repository (and verify secrets):**
    ```bash
    trufflehog git file://<path> --results=verified,unknown
    ```
    *Note: To scan safely locally without using malicious git config, you can clone the repo to a temp dir, or use `--trust-local-git-config`.*
*   **Scan files/directories without git history:**
    ```bash
    trufflehog filesystem <path>
    ```
*   **Scan for only verified results and output JSON:**
    ```bash
    trufflehog filesystem <path> --results=verified --json
    ```

### CI/CD Integration
**GitHub Actions (TruffleHog):**
```yaml
name: TruffleHog
on:
  push:
    branches: [main]
  pull_request:
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --results=verified,unknown
```
