# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pyyaml",
# ]
# ///

import sys
import argparse
import yaml

def validate_cloud_config(filepath: str) -> bool:
    """
    Validates a cloud-init cloud-config file for correct headers and valid YAML syntax.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Error reading file '{filepath}': {e}", file=sys.stderr)
        return False

    lines = content.lstrip().splitlines()
    if not lines:
        print("❌ Error: The provided file is empty.", file=sys.stderr)
        return False

    # 1. Validate the mandatory cloud-init header
    first_line = lines[0].strip()
    if not first_line.startswith("#cloud-config"):
        print(f"❌ Error: Missing mandatory '#cloud-config' header.", file=sys.stderr)
        print(f"   Found: '{first_line}'", file=sys.stderr)
        print("   Fix: Ensure the very first line of your file is exactly '#cloud-config'.", file=sys.stderr)
        return False

    # 2. Validate YAML syntax
    try:
        parsed_yaml = yaml.safe_load(content)

        # cloud-config should ideally parse into a dictionary
        if parsed_yaml is not None and not isinstance(parsed_yaml, dict):
            print("⚠️ Warning: File is valid YAML, but the top-level structure is not a dictionary.", file=sys.stderr)
            print("   cloud-init typically expects key-value pairs at the root level.", file=sys.stderr)

    except yaml.YAMLError as exc:
        print("❌ Error: Invalid YAML format detected.", file=sys.stderr)
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            print(f"   Location: Line {mark.line + 1}, Column {mark.column + 1}", file=sys.stderr)
            print(f"   Details: {exc.problem}", file=sys.stderr)
        else:
            print(f"   Details: {exc}", file=sys.stderr)
        return False

    print(f"✅ Success: '{filepath}' is a valid cloud-config file.")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Offline validator for cloud-init user-data (cloud-config) files."
    )
    parser.add_argument(
        "file",
        help="Path to the cloud-config YAML file to validate."
    )
    args = parser.parse_args()

    if validate_cloud_config(args.file):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
