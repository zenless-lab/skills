# /// script
# requires-python = ">=3.9"
# ///

import sys
from pathlib import Path

def log(level, category, message):
    colors = {"ERROR": "\033[91m", "WARNING": "\033[93m", "INFO": "\033[94m"}
    reset = "\033[0m"
    print(f"[{colors.get(level, '')}{level}{reset}] {category}: {message}")

def validate(skill_dir: str):
    ref_dir = Path(skill_dir).resolve() / "references"
    if not ref_dir.exists() or not ref_dir.is_dir():
        log("INFO", "Structure", "No 'references/' directory found. Skipping reference validation.")
        sys.exit(0)

    errors, warnings, infos = 0, 0, 0

    for filepath in ref_dir.rglob("*"):
        if filepath.is_dir():
            if filepath.parent != ref_dir:
                log("WARNING", "Structure", f"Nested directory found: {filepath.relative_to(ref_dir)}. Recommended to keep references one level deep.")
                warnings += 1
            continue

        if filepath.suffix.lower() == ".md":
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            line_count = len(lines)
            if line_count < 10:
                log("WARNING", "Granularity", f"Reference '{filepath.name}' is very short ({line_count} lines). Merge into SKILL.md to avoid fragmentation.")
                warnings += 1
            elif line_count < 20:
                log("INFO", "Granularity", f"Reference '{filepath.name}' is {line_count} lines. Monitor for potential over-fragmentation.")
                infos += 1

    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run validate_references.py <path_to_skill_directory>")
        sys.exit(1)
    validate(sys.argv[1])
