# /// script
# requires-python = ">=3.9"
# ///

import sys
import re
from pathlib import Path

def log(level, category, message):
    colors = {"ERROR": "\033[91m", "WARNING": "\033[93m", "INFO": "\033[94m"}
    reset = "\033[0m"
    print(f"[{colors.get(level, '')}{level}{reset}] {category}: {message}")

def validate(skill_dir: str):
    scripts_dir = Path(skill_dir).resolve() / "scripts"
    if not scripts_dir.exists() or not scripts_dir.is_dir():
        log("INFO", "Structure", "No 'scripts/' directory found. Skipping script validation.")
        sys.exit(0)

    errors, warnings, infos = 0, 0, 0

    for py_file in scripts_dir.rglob("*.py"):
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Mandatory: Must contain PEP 723 inline metadata
        if not re.search(r"^# /// script\b.*^# ///$", content, re.MULTILINE | re.DOTALL):
            log("ERROR", "Standards", f"'{py_file.name}' is missing the PEP 723 metadata block. This is mandatory for generated Python scripts.")
            errors += 1

        # Advisory: Avoid blocking interactions
        if re.search(r"\binput\s*\(", content):
            log("WARNING", "Execution", f"'{py_file.name}' contains 'input()'. Scripts should generally be non-blocking for Agent execution.")
            warnings += 1

    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run validate_scripts.py <path_to_skill_directory>")
        sys.exit(1)
    validate(sys.argv[1])
