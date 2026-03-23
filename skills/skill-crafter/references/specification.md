# Skill Specification

Use this file when you need the exact structural and frontmatter rules for a skill.

## Directory structure

A skill is a directory containing at minimum:

```text
skill-name/
├── SKILL.md
├── scripts/      # optional
├── references/   # optional
├── assets/       # optional
└── ...
```

## `SKILL.md` format

`SKILL.md` must contain YAML frontmatter followed by Markdown instructions.

### Required frontmatter

- `name`
- `description`

### Optional frontmatter

- `license`
- `compatibility`
- `metadata`
- `allowed-tools`

## Field constraints

### `name`

- 1 to 64 characters
- lowercase letters, numbers, and hyphens only
- must not start or end with `-`
- must not contain consecutive hyphens
- must match the parent directory name

Valid examples:

```yaml
name: pdf-processing
name: data-analysis
name: code-review
```

Invalid examples:

```yaml
name: PDF-Processing
name: -pdf
name: pdf--processing
```

### `description`

- 1 to 1024 characters
- non-empty
- should describe both what the skill does and when to use it
- should contain intent-language that helps triggering

Good:

```yaml
description: Extract text and tables from PDFs, fill forms, and merge files. Use this skill when working with PDF documents, form workflows, or document extraction tasks.
```

Poor:

```yaml
description: Helps with PDFs.
```

### `license`

- optional
- use a short identifier or point to a bundled license file

Example:

```yaml
license: Proprietary. LICENSE.txt has complete terms
```

### `compatibility`

- optional
- 1 to 500 characters if present
- mention only real environment constraints

Examples:

```yaml
compatibility: Requires Python 3.14+ and uv
compatibility: Requires git, jq, docker, and internet access
```

### `metadata`

- optional key-value mapping
- use for extra properties not defined by the spec

Example:

```yaml
metadata:
  author: example-org
  version: "1.0"
```

### `allowed-tools`

- optional
- space-delimited list
- experimental and client-dependent

Example:

```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

## Body guidance

The Markdown body has no rigid schema, but it should contain only what helps the agent do the work. Recommended content:

- step-by-step workflow
- selection rules
- output expectations
- examples when they reduce ambiguity
- explicit links to references

Avoid turning `SKILL.md` into a dump of all background knowledge. Move details to `references/`.

## Progressive disclosure

Skills should be organized in three layers:

- Metadata: `name` and `description`, loaded for all skills
- Instructions: `SKILL.md` body, loaded when the skill triggers
- Resources: `scripts/`, `references/`, and `assets/`, loaded only as needed

Guidelines:

- keep `SKILL.md` under roughly 500 lines
- split long variant-specific material into separate reference files
- keep reference links one level deep from `SKILL.md`

## Optional directories

### `scripts/`

Use for executable logic that should be deterministic or reused. Scripts should:

- be self-contained where practical
- produce concise errors
- handle expected bad inputs
- document or inline their dependencies

### `references/`

Use for detailed material an agent may need on demand, such as:

- schemas
- API details
- workflow variants
- edge-case guidance

Keep files focused and discoverable from `SKILL.md`.

### `assets/`

Use for static resources that are copied into outputs or serve as templates, such as:

- starter code
- config templates
- sample fixtures
- diagrams or images

## Validation checklist

- directory name equals frontmatter `name`
- `name` satisfies all naming rules
- `description` states what and when
- frontmatter is valid YAML
- references linked from `SKILL.md` are real and useful
- no extra documentation files were added without need
- scripts, references, and assets each have a clear role
