---
name: data-leakage-prevention
description: Audit staged changes, modified files, commits, pull requests, repositories, directories, and single files for secrets, PII leakage, compliance issues, binary-document exposure, and git identity disclosure. Use this skill during code submission checks or general file reviews when you need hybrid static tooling plus semantic triage.
---

# Data Leakage Prevention

Use this skill for submission-time security checks and general file compliance reviews. Combine semantic review with deterministic tooling, and make the audit boundary explicit before any scan starts.

## Core Rules

1. Declare the audit boundary first. State the scope type and the resolved files before scanning.
2. Collect environment context early. Check whether the target is git-backed, whether `.gitleaks.toml` or similar policy files exist, whether `.pre-commit-config.yaml` exists, and whether local text-extraction tools are available for binary documents.
3. Respect repository rules before running detectors. If `.gitleaks.toml` or similar config exists, honor its ignore rules and use its custom rules as review constraints when possible.
4. Choose scan depth from the change summary. Do not default to full semantic review for generated, third-party, or oversized changes.
5. Report precise findings and keep likely false positives separate.

## Boundary And Context

Supported scope types:

- Git: `staged`, `changed`, `commit <hash>`, `pr <id>`
- Filesystem: `entire repo`, `directory`, `specific file`

When the scope is git-based, review git identity unless the user explicitly says not to:

- inspect `git config user.name`
- inspect `git config user.email`
- review authors inside the audit range with `git --no-pager log --format="%an <%ae>"`
- flag names or emails that appear to expose personal identity inappropriately

Load references only when needed:

- [Scope Discovery](references/scope_discovery.md) for concrete git or filesystem commands
- [Git Identity Review](references/git_identity_review.md) for exact identity-check commands and interpretation help
- [Secret Types](references/secret_types.md) only when severity is unclear after semantic review

## Scan Mode Selection

Use `deep review` for most user-authored code, configuration, infrastructure files, documentation, and other manageable text where context changes severity.

Use `fast review` for:

- third-party code
- vendored or submodule content
- generated files
- very large diffs
- very long files where broad semantic reading is wasteful

Escalate from fast review to targeted semantic review when automation finds something material.

## CUDA-Aware `uv run` Invocation

Before running `pii_scan.py`, run a simple CUDA availability check once in the current environment:

```bash
command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1
```

- If the command succeeds, run with normal `uv run`.
- If the command fails, run with `uv run --default-index https://download.pytorch.org/whl/cpu ...` so PyTorch-related dependencies resolve to CPU wheels.

## Scan Procedure

### Deep Review

1. Read the files or the relevant diff hunks.
2. Perform semantic fuzz review for secrets, PII, unsafe metadata, and context that changes severity.
3. Run [pii_scan.py](scripts/pii_scan.py) for Presidio-based PII detection with CUDA-aware `uv run` selection.
4. Run [secret_scan.py](scripts/secret_scan.py) for detect-secrets-based secret detection.
5. If `.pre-commit-config.yaml` exists and already contains relevant scanning hooks, run the matching pre-commit hooks instead of inventing a parallel workflow.
6. Reconcile semantic findings with tool findings and classify likely false positives explicitly.

Run the bundled Python scripts with `uv run` so their PEP 723 dependencies are installed automatically. Do not invoke them with plain `python` unless dependency management has already been handled separately. For `pii_scan.py`, choose `uv run` arguments based on the CUDA check above.

### Fast Review

1. Skip broad semantic reading.
2. Run [pii_scan.py](scripts/pii_scan.py) and [secret_scan.py](scripts/secret_scan.py), applying the same CUDA-aware `uv run` rule for `pii_scan.py`.
3. If `.pre-commit-config.yaml` exists and already contains relevant scanning hooks, run the matching hooks.
4. Inspect only flagged locations or obviously high-risk files semantically.

Use `uv run` for both bundled scripts in fast review as well.

## Binary And Non-Plaintext Files

If the scope contains files such as PDF, PPT, DOCX, XLSX, or other binary formats:

1. Try to convert them to text first.
2. Scan the extracted text when conversion succeeds.
3. Record the original binary file in the report.
4. If no suitable local tool exists, mark the file as skipped and state the reason.

Do not claim coverage for binary files that were not actually converted or scanned.

## Severity Guidance

Use semantic judgment first. The categories below are guidance, not a closed taxonomy.

- `Critical`: live credentials, private keys, production secrets, cloud tokens, signing material, or anything that can plausibly grant direct access or privileged control
- `High`: real personal data, real customer data, internal secrets, or combinations of identifiers that create material exposure
- `Medium`: partial or contextual sensitive data, non-production secrets with unclear validity, or findings that need more confirmation
- `Low`: weak signals, low-impact metadata, sample-like data with some risk, or findings likely to be test fixtures

## Reporting Requirements

The final report must include:

- whether secrets or PII were found
- the declared audit boundary
- the chosen scan mode and why
- the resolved file list and file types
- confirmed findings
- suspected false positives
- skipped files and reasons
- git identity review results when the scope is git-based

List concrete findings in this format:

```text
./path/to/file:line:column | Severity | PII|Secret | Source | Status | Summary
```

Use these source labels when possible:

- `Presidio`
- `Detect-secrets`
- `Fuzzy review`
- `custom-rule` when a repository policy file contributes a direct hit

If a detector only provides a line number, use column `1`.
