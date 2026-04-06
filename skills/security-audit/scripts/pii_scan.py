# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "presidio-analyzer[stanza]>=2.2.0",
# ]
# ///

from __future__ import annotations

import argparse
import json
import sys
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
    entity_type: str
    score: float
    source: str
    summary: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan files for PII using Microsoft Presidio with a Stanza NLP engine."
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
        "--language",
        default="en",
        help="Language code for Presidio and Stanza. Defaults to 'en'.",
    )
    parser.add_argument(
        "--entities",
        default="",
        help="Comma-separated entity types to limit detection.",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.35,
        help="Minimum Presidio confidence score to report.",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=1_500_000,
        help="Skip files larger than this many bytes.",
    )
    return parser


def display_path(path: Path) -> str:
    try:
        rel_path = path.resolve().relative_to(Path.cwd().resolve())
        return f"./{rel_path.as_posix()}"
    except ValueError:
        return path.as_posix()


def offset_to_line_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    line_start = text.rfind("\n", 0, offset)
    column = offset + 1 if line_start == -1 else offset - line_start
    return line, column


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


def create_analyzer(language: str):
    try:
        from presidio_analyzer import AnalyzerEngine
        from presidio_analyzer.nlp_engine import StanzaNlpEngine
    except ImportError as exc:
        raise SystemExit(
            "Failed to import Presidio. Run this script with uv so dependencies from the PEP 723 header are installed."
        ) from exc

    try:
        nlp_engine = StanzaNlpEngine(
            models=[{"lang_code": language, "model_name": language}],
            download_if_missing=True,
        )
        nlp_engine.load()
        return AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=[language])
    except Exception as exc:
        raise SystemExit(
            f"Failed to initialize Presidio with Stanza for language '{language}': {exc}"
        ) from exc


def scan_text(
    analyzer,
    path_label: str,
    text: str,
    language: str,
    entities: list[str] | None,
    min_score: float,
) -> list[FindingRecord]:
    findings: list[FindingRecord] = []
    results = analyzer.analyze(
        text=text,
        language=language,
        entities=entities or None,
        score_threshold=min_score,
    )

    for result in results:
        line, column = offset_to_line_column(text, result.start)
        findings.append(
            FindingRecord(
                path=path_label,
                line=line,
                column=column,
                entity_type=result.entity_type,
                score=round(result.score, 4),
                source="Presidio",
                summary=f"Detected {result.entity_type}",
            )
        )

    return findings


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.paths:
        parser.error("at least one path or '-' is required")

    entities = [item.strip() for item in args.entities.split(",") if item.strip()]
    analyzer = create_analyzer(args.language)
    scanned_files: list[FileRecord] = []
    skipped_files: list[SkippedRecord] = []
    findings: list[FindingRecord] = []

    input_files, pre_skipped = iter_input_files(args.paths)
    skipped_files.extend(pre_skipped)

    if "-" in args.paths:
        stdin_text = sys.stdin.read()
        findings.extend(
            scan_text(
                analyzer=analyzer,
                path_label=args.stdin_path,
                text=stdin_text,
                language=args.language,
                entities=entities,
                min_score=args.min_score,
            )
        )
        scanned_files.append(
            FileRecord(
                path=args.stdin_path,
                file_type="stdin",
                size_bytes=len(stdin_text.encode("utf-8")),
            )
        )

    for path in input_files:
        text, error = read_text_file(path, args.max_bytes)
        label = display_path(path)
        if error:
            skipped_files.append(SkippedRecord(path=label, reason=error))
            continue

        findings.extend(
            scan_text(
                analyzer=analyzer,
                path_label=label,
                text=text or "",
                language=args.language,
                entities=entities,
                min_score=args.min_score,
            )
        )
        scanned_files.append(
            FileRecord(
                path=label,
                file_type=path.suffix.lower() or "<no-extension>",
                size_bytes=path.stat().st_size,
            )
        )

    payload = {
        "tool": "Presidio",
        "language": args.language,
        "findings": [asdict(record) for record in findings],
        "scanned_files": [asdict(record) for record in scanned_files],
        "skipped_files": [asdict(record) for record in skipped_files],
    }
    json.dump(payload, sys.stdout, ensure_ascii=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
