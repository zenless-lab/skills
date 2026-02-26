# Reference File Best Practices

The `references/` directory stores auxiliary documents loaded strictly on-demand. This is the mechanism that powers Progressive Disclosure.

## Granularity and Merging

* **Stay Focused**: Each reference file should focus on a single topic (e.g., `api-endpoints.md` or `data-schema.md`).
* **Prevent Over-fragmentation**: During the global planning stage, if a reference file is projected to be very short (e.g., under 20 lines or a simple list), **DO NOT** create a separate file. Merge it directly into the `SKILL.md` body or another relevant reference file. Tiny files waste tokens and increase I/O load.

## Formatting and Structure

* **High Scannability**: Reference files must be highly structured. Use Markdown headings (`##`, `###`), lists, and tables heavily. Agents parse structured data far more efficiently than walls of text.
* **Provide Clear Examples**: If documenting a procedure, always provide concrete `Input` and `Output` examples.

## Path Referencing Rules

* **Strictly Relative Paths**: Any link from `SKILL.md` to a reference, or from a reference to an asset, **MUST use relative paths** starting from the skill root directory.
  * ✅ **Valid**: `Please see the [API Guide](references/api-guide.md)`
  * ✅ **Valid**: `Run the parser: scripts/parser.py`
  * ❌ **Invalid**: `See /Users/name/skills/my-skill/references/api-guide.md`
* **Shallow Hierarchy**: Prefer a flat or single-level structure inside `references/` (e.g., `references/layouts/fastapi.md`). Avoid deeply nested trees (e.g., `references/docs/v1/api.md`), which are highly discouraged.
