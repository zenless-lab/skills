# Skills

<p align="left">
	<img alt="License" src="https://img.shields.io/badge/license-Apache%202.0-blue.svg">
	<img alt="Format" src="https://img.shields.io/badge/content-Markdown-0f172a.svg">
	<img alt="Focus" src="https://img.shields.io/badge/focus-AI%20Training%20%7C%20Engineering-7c3aed.svg">
	<img alt="Quality" src="https://img.shields.io/badge/quality-pre--commit-brightgreen.svg">
</p>

A curated collection of reusable, reference-first **Agent Skills** for AI training, software engineering, and secure development workflows.

This repository is designed for progressive loading: each skill keeps core guidance in `SKILL.md` and deep context in `references/` (plus scripts/templates where needed).

## Why this repo

- **Reusable skill modules** for different technical domains
- **Reference-first design** to reduce hallucination and improve consistency
- **Practical workflows** with clear routing and response templates
- **Production-minded quality checks** with pre-commit and secret scanning

## Repository layout

```text
.
├── skills/
│   ├── huggingface-accelerate-guide/
│   ├── llm-training-guide/
│   ├── proto-schema-expert/
│   ├── python-standards/
│   └── secret-leak-check/
├── .github/agents/
├── .devcontainer/
├── .pre-commit-config.yaml
└── README.md
```

## Available skills

| Skill | Purpose | Key assets |
|---|---|---|
| `huggingface-accelerate-guide` | A specialized assistant for using Hugging Face Accelerate for distributed training, inference, and large model handling. | Training templates, inference scripts, troubleshooting tools |
| `llm-training-guide` | Reference-first guide for strategy, troubleshooting, alignment method selection, and training-health metrics. | Method deep dives, hardware + VRAM docs, metric taxonomy |
| `python-standards` | Apply project-aware Python conventions with PEP 8-first style and progressive reference loading. | Discovery/style/docstring/layout references |
| `proto-schema-expert` | Draft, review, and explain Protobuf schemas across Editions/Proto3/Proto2. | Type reference, style guide, version-specific docs |
| `secret-leak-check` | Detect secret/privacy leakage risks across diffs, commit messages, and git identity contexts. | Detection rules, scope logic, reporting templates |

## Quick start

### 1) Open in a Dev Container (recommended)

This repo includes a ready-to-use dev container with:

- Ubuntu base image
- Git + Git LFS
- Node.js
- Python + `pre-commit`
- VS Code MCP server configuration for Hugging Face

In VS Code:

1. Open the repository
2. Run: **Dev Containers: Reopen in Container**

### 2) Set up local quality checks

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Working with skills

### Skill structure convention

Each skill should typically follow:

- `SKILL.md`: concise workflow + routing guidance
- `references/`: heavy documentation and deep dives
- `assets/`: executable templates (when needed)
- `scripts/`: executable helpers (when needed)

### Authoring principles

1. Keep `SKILL.md` concise and actionable.
2. Move detailed material into `references/`.
3. Load references progressively based on the user task.
4. Match existing style and naming conventions.

## Security and quality

Pre-commit hooks enforce:

- whitespace and EOF normalization
- YAML validation
- merge conflict detection
- large file checks (max 2 MB)
- secret scanning via `detect-secrets`

For CI, repository workflows also run secret scanning checks.

## Contributing

Contributions are welcome.

Suggested flow:

1. Create or update a skill under `skills/`
2. Keep changes focused and minimal
3. Run `pre-commit run --all-files`
4. Open a pull request with a clear summary and rationale

If you are creating a new skill, use the custom agent definition in `.github/agents/create-skill.agent.md` as a structural reference.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
