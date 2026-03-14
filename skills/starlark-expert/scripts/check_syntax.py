# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///

import ast
import sys
import argparse

# Map of Python AST nodes to Starlark error messages
FORBIDDEN_NODES = {
    ast.While: "Starlark does not support 'while' loops. Use 'for' loops instead.",
    ast.Yield: "Starlark does not support 'yield' (generators).",
    ast.YieldFrom: "Starlark does not support 'yield from'.",
    ast.ClassDef: "Starlark does not support 'class' definitions. Use 'struct' or dictionaries.",
    ast.Try: "Starlark does not support exception handling ('try/except' blocks).",
    ast.TryStar: "Starlark does not support exception handling.",
    ast.Raise: "Starlark does not support raising exceptions. Use 'fail()' instead.",
    ast.Global: "Starlark does not support the 'global' keyword.",
    ast.Nonlocal: "Starlark does not support the 'nonlocal' keyword.",
    ast.Is: "Starlark does not support the 'is' operator. Use '==' instead.",
    ast.Import: "Starlark does not support standard 'import'. Use the 'load()' statement.",
    ast.ImportFrom: "Starlark does not support 'from ... import ...'. Use the 'load()' statement."
}

class StarlarkValidator(ast.NodeVisitor):
    """Walks the AST to find Python features that are invalid in Starlark."""
    def __init__(self):
        self.errors = []

    def generic_visit(self, node):
        node_type = type(node)
        if node_type in FORBIDDEN_NODES:
            line = getattr(node, 'lineno', '?')
            col = getattr(node, 'col_offset', '?')
            self.errors.append(f"Line {line}:{col} - {FORBIDDEN_NODES[node_type]}")
        super().generic_visit(node)

def main():
    parser = argparse.ArgumentParser(description="Validate Starlark syntax using Python's AST.")
    parser.add_argument(
        "file",
        nargs="?",
        type=argparse.FileType('r', encoding='utf-8'),
        default=sys.stdin,
        help="Starlark (.bzl or BUILD) file to check (defaults to stdin)"
    )
    args = parser.parse_args()

    try:
        source = args.file.read()
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Check basic syntax validty (subset of Python 3)
    try:
        tree = ast.parse(source, filename=args.file.name)
    except SyntaxError as e:
        print(f"SyntaxError in {args.file.name}:{e.lineno}:{e.offset}: {e.msg}", file=sys.stderr)
        if e.text:
            print(e.text.rstrip(), file=sys.stderr)
            print(" " * (e.offset - 1 if e.offset else 0) + "^", file=sys.stderr)
        sys.exit(1)

    # Step 2: Check for Starlark-specific restrictions
    validator = StarlarkValidator()
    validator.visit(tree)

    if validator.errors:
        print(f"Starlark Compatibility Errors in {args.file.name}:", file=sys.stderr)
        for err in validator.errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"Syntax OK: {args.file.name}")
    sys.exit(0)

if __name__ == "__main__":
    main()
