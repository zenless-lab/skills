# Scenario: Full Scan

Use this reference only when user explicitly asks for full-file or full-repository scanning.

## Scope rules

1. Ignore diff-first defaults.
2. Scan all files in requested range.
3. Include tracked files and user-requested generated/config assets when applicable.
4. Build an explicit in-scope file list before detection.
5. Read every in-scope text file at least once.
6. Run at least one detection pass on every in-scope source file.

## Exclusions

- Build caches
- Dependency vendor directories
- Binary files without text extraction support

If exclusions are applied, list them explicitly. Also report file coverage:

- total in-scope files
- successfully read and checked files
- excluded files with reasons

## Detection strategy

1. Run pattern-based detection for secrets and privacy indicators.
2. Run context checks to reduce obvious false positives (for example placeholder values, docs examples explicitly marked fake).
3. Escalate findings in production config, deployment, or runtime credential sources.

## Severity guidance

- **critical**: active credentials/tokens, private keys, production connection strings
- **high**: likely personal data, internal architecture details with exploitation value
- **medium**: suspicious identifiers requiring manual validation
- **low**: weak signals, potential false positives
