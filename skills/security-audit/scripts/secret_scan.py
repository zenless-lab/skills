# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "detect-secrets>=1.5.0",
# ]
# ///

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_TEXT_EXTENSIONS = {
    ".c",
    ".cc",
    ".cfg",
    ".conf",
    ".cpp",
    ".cs",
    ".css",
    ".csv",
    ".env",
    ".go",
    ".h",
    ".hpp",
    ".html",
    ".ini",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".kt",
    ".kts",
    ".log",
    ".md",
    ".mjs",
    ".php",
    ".properties",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".svg",
    ".tf",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


@dataclass
class FileRecord:
    path: str
    file_type: str
    size_bytes: int


@dataclass
class SkippedRecord:
    path: str
    reason: str


@dataclass
class FindingRecord:
    path: str
    line: int
    column: int
    detector: str
    source: str
    summary: str


@dataclass
class GitleaksRule:
    rule_id: str
    description: str
    regex: re.Pattern[str]
    path_regex: re.Pattern[str] | None


@dataclass
class GitleaksPolicy:
    path_filters: list[re.Pattern[str]]
    secret_filters: list[re.Pattern[str]]
    stopwords: set[str]
    custom_rules: list[GitleaksRule]
    config_path: str | None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan files for secrets using detect-secrets and optional gitleaks policy filters."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to scan. Use '-' to read from stdin.",
    )
    parser.add_argument(
        "--stdin-path",
        default="./stdin.txt",
        help="Display path used when reading content from stdin.",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=1_500_000,
        help="Skip files larger than this many bytes.",
    )
    parser.add_argument(
        "--gitleaks-config",
        default="",
        help="Optional explicit .gitleaks.toml path.",
    )
    return parser


def display_path(path: Path) -> str:
    try:
        rel_path = path.resolve().relative_to(Path.cwd().resolve())
        return f"./{rel_path.as_posix()}"
    except ValueError:
        return path.as_posix()


def is_probably_binary(path: Path) -> bool:
    with path.open("rb") as handle:
        sample = handle.read(4096)
    return b"\x00" in sample


def iter_input_files(paths: list[str]) -> tuple[list[Path], list[SkippedRecord]]:
    resolved: list[Path] = []
    skipped: list[SkippedRecord] = []

    for raw in paths:
        if raw == "-":
            continue

        target = Path(raw)
        if not target.exists():
            skipped.append(SkippedRecord(path=raw, reason="path does not exist"))
            continue

        if target.is_file():
            resolved.append(target)
            continue

        if target.is_dir():
            for candidate in sorted(target.rglob("*")):
                if candidate.is_file() and ".git" not in candidate.parts:
                    resolved.append(candidate)
            continue

        skipped.append(SkippedRecord(path=raw, reason="unsupported path type"))

    return resolved, skipped


def locate_gitleaks_config(explicit_path: str) -> Path | None:
    if explicit_path:
        candidate = Path(explicit_path)
        return candidate if candidate.is_file() else None

    for base in [Path.cwd(), *Path.cwd().parents]:
        for name in (".gitleaks.toml", "gitleaks.toml"):
            candidate = base / name
            if candidate.is_file():
                return candidate
    return None


def collect_string_list(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def safe_compile(pattern: str) -> re.Pattern[str] | None:
    try:
        return re.compile(pattern)
    except re.error:
        return None


def extend_filters_from_allowlist(container: object, policy: GitleaksPolicy) -> None:
    if not isinstance(container, dict):
        return

    for key in ("paths", "path"):
        for pattern in collect_string_list(container.get(key)):
            compiled = safe_compile(pattern)
            if compiled:
                policy.path_filters.append(compiled)

    for key in ("regexes", "regex"):
        for pattern in collect_string_list(container.get(key)):
            compiled = safe_compile(pattern)
            if compiled:
                policy.secret_filters.append(compiled)

    for stopword in collect_string_list(container.get("stopwords")):
        policy.stopwords.add(stopword.lower())


def load_gitleaks_policy(explicit_path: str) -> GitleaksPolicy:
    policy = GitleaksPolicy(
        path_filters=[],
        secret_filters=[],
        stopwords=set(),
        custom_rules=[],
        config_path=None,
    )

    config_path = locate_gitleaks_config(explicit_path)
    if not config_path:
        return policy

    policy.config_path = display_path(config_path)

    try:
        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except OSError:
        return policy
    except tomllib.TOMLDecodeError:
        return policy

    extend_filters_from_allowlist(data.get("allowlist"), policy)
    for container in data.get("allowlists", []):
        extend_filters_from_allowlist(container, policy)

    for rule in data.get("rules", []):
        if not isinstance(rule, dict):
            continue

        extend_filters_from_allowlist(rule.get("allowlist"), policy)
        for container in rule.get("allowlists", []):
            extend_filters_from_allowlist(container, policy)

        regex_value = rule.get("regex")
        if not isinstance(regex_value, str):
            continue

        compiled_regex = safe_compile(regex_value)
        if not compiled_regex:
            continue

        path_regex = None
        path_value = rule.get("path")
        if isinstance(path_value, str):
            path_regex = safe_compile(path_value)

        rule_id = rule.get("id") if isinstance(rule.get("id"), str) else "custom-rule"
        description = (
            rule.get("description")
            if isinstance(rule.get("description"), str)
            else f"Custom gitleaks rule {rule_id}"
        )
        policy.custom_rules.append(
            GitleaksRule(
                rule_id=rule_id,
                description=description,
                regex=compiled_regex,
                path_regex=path_regex,
            )
        )

    return policy


def path_matches_any(path_label: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(path_label) for pattern in patterns)


def line_matches_policy(line_text: str, policy: GitleaksPolicy) -> bool:
    lowered = line_text.lower()
    if any(stopword in lowered for stopword in policy.stopwords):
        return True
    return any(pattern.search(line_text) for pattern in policy.secret_filters)


def read_text_file(path: Path, max_bytes: int) -> tuple[str | None, str | None]:
    size = path.stat().st_size
    if size > max_bytes:
        return None, f"file exceeds max-bytes ({size} > {max_bytes})"

    if path.suffix.lower() not in DEFAULT_TEXT_EXTENSIONS and is_probably_binary(path):
        return None, "binary file"

    try:
        return path.read_text(encoding="utf-8", errors="replace"), None
    except OSError as exc:
        return None, f"read error: {exc}"


def create_temp_file_from_stdin(path_label: str) -> tuple[Path, str]:
    content = sys.stdin.read()
    temp_dir = Path(tempfile.mkdtemp(prefix="security-audit-"))
    temp_file = temp_dir / Path(path_label).name
    temp_file.write_text(content, encoding="utf-8")
    return temp_file, content


def scan_with_detect_secrets(paths: list[Path]) -> dict[str, list[dict[str, object]]]:
    try:
        from detect_secrets import SecretsCollection
        from detect_secrets.settings import default_settings
    except ImportError as exc:
        raise SystemExit(
            "Failed to import detect-secrets. Run this script with uv so dependencies from the PEP 723 header are installed."
        ) from exc

    collection = SecretsCollection()
    with default_settings():
        for path in paths:
            collection.scan_file(str(path))
    return collection.json()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.paths:
        parser.error("at least one path or '-' is required")

    policy = load_gitleaks_policy(args.gitleaks_config)
    scanned_files: list[FileRecord] = []
    skipped_files: list[SkippedRecord] = []
    findings: list[FindingRecord] = []

    input_files, pre_skipped = iter_input_files(args.paths)
    skipped_files.extend(pre_skipped)

    stdin_temp: Path | None = None
    stdin_content = ""
    if "-" in args.paths:
        stdin_temp, stdin_content = create_temp_file_from_stdin(args.stdin_path)
        input_files.append(stdin_temp)

    file_text_cache: dict[str, str] = {}
    filtered_files: list[Path] = []
    path_label_map: dict[str, str] = {}

    for path in input_files:
        label = args.stdin_path if stdin_temp and path == stdin_temp else display_path(path)
        path_label_map[str(path)] = label

        if path_matches_any(label, policy.path_filters):
            skipped_files.append(SkippedRecord(path=label, reason="ignored by gitleaks path policy"))
            continue

        text, error = read_text_file(path, args.max_bytes)
        if error:
            skipped_files.append(SkippedRecord(path=label, reason=error))
            continue

        filtered_files.append(path)
        file_text_cache[str(path)] = stdin_content if stdin_temp and path == stdin_temp else (text or "")
        scanned_files.append(
            FileRecord(
                path=label,
                file_type="stdin" if stdin_temp and path == stdin_temp else (path.suffix.lower() or "<no-extension>"),
                size_bytes=len(file_text_cache[str(path)].encode("utf-8"))
                if stdin_temp and path == stdin_temp
                else path.stat().st_size,
            )
        )

    raw_findings = scan_with_detect_secrets(filtered_files)

    for filename, items in raw_findings.items():
        label = path_label_map.get(filename, filename)
        text = file_text_cache.get(filename, "")
        lines = text.splitlines()

        for item in items:
            line_number = int(item.get("line_number", 1))
            line_text = lines[line_number - 1] if 0 < line_number <= len(lines) else ""
            if line_matches_policy(line_text, policy):
                continue

            findings.append(
                FindingRecord(
                    path=label,
                    line=line_number,
                    column=1,
                    detector=str(item.get("type", "Unknown secret")),
                    source="Detect-secrets",
                    summary=f"Detected {item.get('type', 'secret candidate')}",
                )
            )

    for path in filtered_files:
        label = path_label_map[str(path)]
        text = file_text_cache.get(str(path), "")
        lines = text.splitlines()
        for rule in policy.custom_rules:
            if rule.path_regex and not rule.path_regex.search(label):
                continue
            for line_number, line_text in enumerate(lines, start=1):
                match = rule.regex.search(line_text)
                if not match:
                    continue
                if line_matches_policy(line_text, policy):
                    continue
                findings.append(
                    FindingRecord(
                        path=label,
                        line=line_number,
                        column=match.start() + 1,
                        detector=rule.rule_id,
                        source="custom-rule",
                        summary=rule.description,
                    )
                )

    payload = {
        "tool": "Detect-secrets",
        "gitleaks_config": policy.config_path,
        "findings": [asdict(record) for record in findings],
        "scanned_files": [asdict(record) for record in scanned_files],
        "skipped_files": [asdict(record) for record in skipped_files],
    }
    json.dump(payload, sys.stdout, ensure_ascii=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
