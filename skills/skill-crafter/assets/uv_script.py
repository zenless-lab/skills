#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Template for a self-contained skill script runnable with uv run."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Optional input value for the script template.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.input is None:
        print("Success: script template is wired correctly.")
        return 0

    print(f"Success: received input={args.input!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
