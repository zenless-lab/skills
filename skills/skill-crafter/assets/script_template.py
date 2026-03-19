# /// script
# requires-python = ">=3.11"
# dependencies = [
# ]
# ///

"""
Agent Script Template

This is a self-contained Python script following PEP 723. It is designed to be
executed by an agent using `uv run`.
- It uses argparse for clear CLI definitions.
- It contains NO interactive prompts.
- It outputs structured data to stdout and diagnostics/errors to stderr.
"""

import argparse
import sys
import json

def main():
    parser = argparse.ArgumentParser(description="Description of what this agent helper script does.")
    parser.add_argument("--input", required=True, help="Path to the input file")
    parser.add_argument("--output", help="Path to the output file (defaults to stdout)")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format structure")

    args = parser.parse_args()

    try:
        # ---- Add logic here ----

        # Example structured result
        result = {
            "status": "success",
            "processed_file": args.input,
            "message": "Processing completed successfully."
        }

        # ---- End logic ----

        # Write output
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                if args.format == "json":
                    json.dump(result, f, indent=2)
                else:
                    f.write(str(result)) # Add CSV logic if needed
        else:
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print(str(result))

    except Exception as e:
        # Print a clear, helpful error message to stderr
        print(f"Error processing {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
