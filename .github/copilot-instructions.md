# Copilot Instructions for Skills Repository

## Repository Overview

This repository is a **collection of reusable skills** focused on AI training, software development, and data analytics. Skills are modular knowledge units that can be referenced by AI agents to provide specialized expertise in specific domains.

### Purpose
- Store and organize specialized knowledge domains as "skills"
- Provide structured reference materials for AI assistants
- Maintain consistency in technical guidance across multiple domains

### Key Technologies
- **Documentation Format**: Markdown
- **Structure**: Modular skill-based organization
- **Quality Tools**: Pre-commit hooks, secret scanning, Detect-secrets
- **License**: Apache 2.0

## Repository Structure

```
.
├── .github/
│   ├── agents/              # Custom agent definitions
│   │   └── create-skill.agent.md  # Expert agent for creating new skills
│   └── workflows/           # CI/CD workflows
│       └── secret.yml       # Secret scanning workflow
├── .devcontainer/           # Development container configuration
│   └── devcontainer.json    # VS Code dev container setup with Python, Node.js
├── skills/                  # Core skills directory
│   ├── proto-schema-expert/ # Protocol Buffers expertise
│   │   ├── SKILL.md         # Main skill definition
│   │   └── references/      # Reference documentation
│   └── python-standards/    # Python coding standards
│       ├── SKILL.md         # Main skill definition
│       └── references/      # Reference documentation
│           ├── doc_styles/  # Docstring formats (Google, Sphinx, NumPy)
│           ├── layouts/     # Project layouts (Src, Flat, FastAPI, Data Science)
│           ├── style/       # PEP 8 and code style guides
│           └── testing/     # Testing frameworks (pytest, unittest, BDD)
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── .secrets.baseline        # Baseline for secret detection
└── README.md                # Repository overview
```

## Skill Structure

Each skill follows a consistent structure:

### SKILL.md Format
Each skill has a main `SKILL.md` file with:
- **Front matter** (YAML): name, description, compatibility notes
- **Skill Overview**: Purpose and use cases
- **External Resources**: Official documentation links
- **Workflow Instructions**: Step-by-step guidance
- **Response Template**: Format for structured outputs

### References Directory
Supporting documentation organized by topic:
- Each reference file focuses on a specific aspect
- Progressive loading approach (load only what's needed)
- Examples and practical guidance included

## Development Workflow

### Quality Checks

**Pre-commit Hooks** (`.pre-commit-config.yaml`):
Run before every commit to ensure code quality:
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

Enabled checks:
- Trailing whitespace removal
- End-of-file fixing
- YAML validation
- Merge conflict detection
- Large file detection (max 2MB)
- Secret detection using detect-secrets

**Secret Scanning**:
- GitHub Actions workflow runs TruffleHog on all commits
- Local baseline maintained in `.secrets.baseline`
- Update baseline when legitimate secrets-like patterns are added

### Creating New Skills

Use the custom agent for consistency:
- A `create-skill.agent.md` agent exists in `.github/agents/`
- This agent is an expert in creating and structuring skills
- Prefer using this agent when creating new skills

### Development Environment

The repository includes a dev container configuration:
- **Base Image**: Ubuntu (Noble)
- **Pre-installed**: Python (with pre-commit), Node.js, Git LFS, Zsh
- **VS Code Extensions**: GitHub Copilot, Remote Containers
- **MCP Server**: HuggingFace integration configured

To use the dev container:
1. Open the repository in VS Code
2. Press `Ctrl+Shift+P` and select "Dev Containers: Reopen in Container"
3. Wait for the container to build and initialize

## Common Patterns and Best Practices

### When Working with Skills

1. **Understand the Skill Structure First**
   - Read the `SKILL.md` file to understand the workflow
   - Skills use progressive loading - load only relevant references
   - Don't dump all references at once

2. **Pattern Matching**
   - Skills like `python-standards` identify patterns before loading references
   - Example: Check if project uses `src/` layout before loading `src.md`
   - Example: Identify docstring style (Google/Sphinx/NumPy) before applying rules

3. **Reference Organization**
   - References are granular and focused
   - Each reference file addresses one specific topic
   - Cross-references between files guide progressive learning

### Documentation Standards

1. **Markdown Format**
   - Use standard markdown syntax
   - Include code examples with proper language tags
   - Use tables for structured comparisons

2. **Front Matter**
   - Use YAML front matter for metadata
   - Required fields: `name`, `description`
   - Optional: `compatibility`, `version`, etc.

3. **File Naming**
   - Use lowercase with underscores for reference files
   - Keep names descriptive but concise
   - Example: `best_practices.md`, `data_types_reference.md`

## Making Changes

### Adding a New Skill

1. Create a new directory under `skills/`
2. Add a `SKILL.md` file following the established pattern
3. Create a `references/` subdirectory for supporting docs
4. Organize references by topic (similar to existing skills)
5. Update the main README.md if needed

### Modifying Existing Skills

1. **Minimal Changes**: Make surgical, focused changes
2. **Consistency**: Match existing style and structure
3. **Testing**: Manually review that references are valid
4. **Documentation**: Update related sections if logic changes

### Quality Assurance

Before finalizing changes:
1. Run pre-commit hooks: `pre-commit run --all-files`
2. Check for secrets: Review `.secrets.baseline` updates
3. Validate YAML/Markdown syntax
4. Ensure all links are valid
5. Test that skill workflows make sense end-to-end

## Common Issues and Troubleshooting

### Pre-commit Hook Failures

**Trailing Whitespace**:
- Pre-commit will auto-fix trailing whitespace
- Re-stage the files and commit again

**Secret Detection**:
- Review detected secrets carefully
- If false positive, update `.secrets.baseline`:
  ```bash
  detect-secrets scan > .secrets.baseline
  ```
- Never commit real secrets

**YAML Validation**:
- Use a YAML linter to check syntax
- Common issue: incorrect indentation (use spaces, not tabs)

### Large File Detection

- Maximum file size: 2000 KB (2 MB)
- If you need larger files, consider:
  - Splitting into smaller chunks
  - Using Git LFS
  - Storing externally and linking

### Markdown Formatting

- Keep lines under 120 characters when possible
- Use consistent heading levels
- Ensure code blocks have language tags
- Test that tables render correctly

## Agent Integration

### Custom Agents

The repository includes custom agents in `.github/agents/`:
- **create-skill.agent.md**: Expert for creating new skills
- These agents have specialized knowledge for the repository
- Use them via the `task` tool when appropriate

### Using Skills with AI Assistants

Skills are designed to be:
1. **Discoverable**: Clear naming and descriptions
2. **Modular**: Load only what's needed for the task
3. **Progressive**: Start general, get specific as needed
4. **Practical**: Include examples and templates

## Testing Strategy

This repository is primarily documentation-based:
- **No unit tests** required for markdown files
- **Manual validation**: Read through changes to ensure clarity
- **Structural validation**: Ensure all links work
- **Consistency checks**: Match existing patterns and styles

## Tips for Efficient Work

1. **Explore First**: Use `view` and `grep` to understand structure before editing
2. **Pattern Match**: Identify which skill/reference is most similar to your task
3. **Parallel Operations**: When reading multiple files, do it in one tool call
4. **Minimal Changes**: Only modify what's necessary for the task
5. **Use Custom Agents**: When creating skills, use the create-skill agent
6. **Validate Early**: Run pre-commit hooks frequently during development
7. **Reference Existing Skills**: Follow established patterns in proto-schema-expert and python-standards

## Security Considerations

1. **Secret Scanning**: Always enabled via pre-commit and GitHub Actions
2. **No Sensitive Data**: This is a public repository, never commit:
   - API keys or tokens
   - Passwords or credentials
   - Private information or PII
3. **License**: Apache 2.0 - ensure contributions comply

## Getting Help

- Check existing skills for patterns and examples
- Review `.github/agents/create-skill.agent.md` for skill creation guidance
- Examine reference files for documentation standards
- Use the dev container for consistent environment

---

**Last Updated**: 2026-02-14
**Maintained By**: ryan-minato
**License**: Apache 2.0
