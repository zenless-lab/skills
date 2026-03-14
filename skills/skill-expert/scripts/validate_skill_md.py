# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///

import sys
import re
import yaml
from pathlib import Path

def log(level, category, message):
    colors = {"ERROR": "\033[91m", "WARNING": "\033[93m", "INFO": "\033[94m"}
    reset = "\033[0m"
    print(f"[{colors.get(level, '')}{level}{reset}] {category}: {message}")

def validate(skill_dir: str):
    skill_path = Path(skill_dir).resolve()
    skill_name_dir = skill_path.name
    md_path = skill_path / "SKILL.md"

    errors, warnings, infos = 0, 0, 0

    if not md_path.exists():
        log("ERROR", "Structure", "SKILL.md is missing. This is a mandatory file.")
        sys.exit(1)

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split('\n')

    # 1. Frontmatter Parsing
    match = re.match(r"^\s*---\s*\n(.*?)\n---\s*", content, re.DOTALL)
    if not match:
        log("ERROR", "Frontmatter", "Missing or malformed YAML frontmatter.")
        sys.exit(1)

    try:
        metadata = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as e:
        log("ERROR", "Frontmatter", f"YAML parsing failed: {e}")
        sys.exit(1)

    # 2. Name Validation (Mandatory constraints)
    name = str(metadata.get("name") or "")
    if not name:
        log("ERROR", "Frontmatter", "Missing required field: 'name'.")
        errors += 1
    else:
        if not (1 <= len(name) <= 64):
            log("ERROR", "Frontmatter", f"'name' must be 1-64 characters (current: {len(name)}).")
            errors += 1
        elif len(name) > 55:
            log("INFO", "Frontmatter", f"'name' length ({len(name)}) is approaching the 64-character limit.")
            infos += 1

        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            log("ERROR", "Frontmatter", "'name' has invalid characters or consecutive/leading/trailing hyphens.")
            errors += 1

        if name != skill_name_dir:
            log("ERROR", "Structure", f"'name' ('{name}') does not match folder name ('{skill_name_dir}').")
            errors += 1

    # 3. Description Validation
    desc = str(metadata.get("description") or "")
    if not desc:
        log("ERROR", "Frontmatter", "Missing required field: 'description'.")
        errors += 1
    else:
        if not (1 <= len(desc) <= 1024):
            log("ERROR", "Frontmatter", f"'description' must be 1-1024 characters (current: {len(desc)}).")
            errors += 1
        elif len(desc) > 900:
            log("INFO", "Frontmatter", f"'description' length ({len(desc)}) is approaching the 1024-character limit.")
            infos += 1

    # 4. Length Constraints (Advisory)
    line_count = len(lines)
    if line_count > 500:
        log("WARNING", "Progressive Disclosure", f"SKILL.md has {line_count} lines. Advised to be under 500 lines.")
        warnings += 1
    elif line_count > 450:
        log("INFO", "Progressive Disclosure", f"SKILL.md has {line_count} lines, approaching the 500-line recommended limit.")
        infos += 1

    # 5. Absolute Path Checks
    if re.search(r"(/Users/|[A-Z]:\\|file://|/home/)", content):
        log("WARNING", "Paths", "Found potential absolute paths. Skill files should use relative paths.")
        warnings += 1

    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run validate_skill_md.py <path_to_skill_directory>")
        sys.exit(1)
    validate(sys.argv[1])
