# Agent Skills Specification

## Directory Structure
A skill is a directory containing, at minimum, a `SKILL.md` file:
```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

## `SKILL.md` Frontmatter

YAML frontmatter is REQUIRED at the top of `SKILL.md` (bounded by `---`).

| Field           | Required | Constraints |
| --------------- | -------- | ----------- |
| `name`          | Yes      | Max 64 chars. Lowercase letters, numbers, and hyphens only. Must not start/end with a hyphen. Must not contain consecutive hyphens (`--`). Must match parent directory name. |
| `description`   | Yes      | Max 1024 chars. Non-empty. Describes what the skill does and when to use it. Should use imperative phrasing (e.g., "Use this skill when..."). |
| `license`       | No       | License name or reference to a bundled license file. |
| `compatibility` | No       | Max 500 chars. Indicates environment requirements (e.g., intended product, system packages, network access). |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata. |
| `allowed-tools` | No       | Space-delimited list of pre-approved tools the skill may use. (Experimental) |

## Progressive Disclosure Structure
1. **Metadata (~50-100 tokens):** The `name` and `description` fields are loaded at session startup.
2. **Instructions (< 5000 tokens recommended):** The full `SKILL.md` body is loaded when the skill is activated. Keep the main `SKILL.md` under 500 lines.
3. **Resources (variable tokens):** Files in `scripts/`, `references/`, and `assets/` are loaded on demand by the agent when referenced in `SKILL.md`. Use relative paths from the skill root (e.g., `references/guide.md`).

## File References
When referencing other files within the skill, use relative paths from the skill root:
```markdown
See [the reference guide](references/REFERENCE.md) for details.
Run the script: `scripts/extract.py`
```
Avoid deeply nested reference chains. Keep references one level deep from `SKILL.md`.
