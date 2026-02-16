# Reporting Template

Use this structure for final scan output.

## 1) Scope and assumptions

- Scan mode: `staged diff` / `local-vs-remote diff` / `changed files` / `full scan`
- Target range: directories/files/commit range
- Assumptions: open-source context, privacy requirement, exclusions
- File coverage:
	- in-scope files: `N`
	- read at least once: `N`
	- checked at least once: `N`
	- excluded/unscannable files: `N` (with reasons)

## 2) Findings summary

- Critical: `N`
- High: `N`
- Medium: `N`
- Low: `N`

## 3) Detailed findings

For each finding:

- Severity:
- Category: `secret` / `privacy` / `metadata`
- Location: file + pointer (or commit hash)
- Evidence: masked snippet or description
- Risk:
- Recommendation:

## 4) Commit message check

- Range checked: local commits not in latest remote commit
- Result: pass/fail
- Findings: hashes and remediation actions if any

## 5) Git identity privacy check (conditional)

- Open-source scenario: yes/no
- GitHub remote: yes/no
- Current git email source: local/global
- Privacy result and recommendation

## 6) Final verdict

- `pass`: no actionable leak detected
- `needs-action`: one or more findings require remediation before share/merge
