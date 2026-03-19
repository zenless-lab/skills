<div align="center">

# 🤖 AI Agent Skills Repository

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Format](https://img.shields.io/badge/content-Markdown-0f172a.svg)](https://daringfireball.net/projects/markdown/)
[![Focus](https://img.shields.io/badge/focus-AI%20Agent%20Skills%20%7C%20Engineering-7c3aed.svg)](https://github.com/zenless-lab/skills)
[![Quality](https://img.shields.io/badge/quality-pre--commit-brightgreen.svg)](https://pre-commit.com/)

**A curated collection of reusable, production-ready Agent Skills and documentation, crafted specifically to empower AI Agents (like VS Code Copilot) across varying technical domains.**

[**Explore Skills**](#️-available-skills) • [**Quick Start**](#-quick-start) • [**Create a Skill**](#️-creating-a-new-skill) • [**Contributing**](#-contributing)

</div>

---

## 🌟 Overview

The `skills` repository is designed around **progressive disclosure**.
Each skill retains core operational instructions in `SKILL.md` while deep-dive context, scripts, and templates are structured into dedicated `references/`, `scripts/`, or `assets/` directories. This prevents context bloat, reduces LLM hallucination, and ensures high-quality generation.

---

## 🧭 Repository Structure

```text
📦 skills
 ┣ 📂 .agents/              # Local agent configuration files
 ┣ 📂 .devcontainer/        # Development environment configuration
 ┣ 📂 .github/              # GitHub-specific configuration
 ┃  ┗ 📂 agents/            # Reusable agent definition files (.agent.md)
 ┣ 📂 skills/               # Core agent skills
 │  ┣ 📂 skill-crafter/
 │  ┣ 📂 agents-md-crafter/
 │  ┣ 📂 cloud-init-crafter/
...
```

---

## 🛠️ Available Skills

| Domain & Skill | Description |
| :--- | :--- |
| **🤖 Agent Engineering** | |
| 🪛 [`skill-crafter`](skills/skill-crafter) | Create, edit, evaluate, and optimize new Agent Skills efficiently. |
| 📜 [`agents-md-crafter`](skills/agents-md-crafter) | Design and update standard AI agent instruction files like `AGENTS.md`. |
| 📝 [`readme-crafter`](skills/readme-crafter) | Focused documentation agent for creating and revising `README.md` files. |
| **🧠 AI / Machine Learning** | |
| 🚀 [`huggingface-accelerate-guide`](skills/huggingface-accelerate-guide) | Guide for Hugging Face Accelerate: distributed training, inference, large models. |
| 📉 [`llm-training-guide`](skills/llm-training-guide) | Reference-first guide for strategy, VRAM estimation, alignment methods, and health metrics. |
| **🐍 Python Ecosystem** | |
| 📏 [`python-standards`](skills/python-standards) | Apply Python coding standards (PEP 8, Google), infer project style, and manage references. |
| ⚡ [`ruff-python-guide`](skills/ruff-python-guide) | Integrate, configure, and troubleshoot Ruff for Python linting and formatting. |
| 📜 [`python-docstring-expert`](skills/python-docstring-expert) | Expert methodology for evaluating, formatting, and generating Python docstrings. |
| 💬 [`python-comment-expert`](skills/python-comment-expert) | Expertise in writing, reviewing, and modifying Python logic code comments. |
| 🇬 [`google-docstring-crafter`](skills/google-docstring-crafter) | Google Style Python Docstring expertise: modules, classes, functions, and formatting. |
| 🔢 [`numpy-docstring-crafter`](skills/numpy-docstring-crafter) | NumPy Style Python Docstring expertise: scientific ecosystem, parameters, and returns. |
| 📑 [`rst-docstring-crafter`](skills/rst-docstring-crafter) | Guidance for reStructuredText (reST), Python docstrings, and Sphinx projects. |
| **⚙️ DevOps & Security** | |
| ☁️ [`cloud-init-crafter`](skills/cloud-init-crafter) | Create and validate cloud-init / user-data scripts for cloud instance provisioning. |
| 🔒 [`secret-scanner`](skills/secret-scanner) | Perform security scans to detect edge cases, passwords, API tokens, and PII. |
| 🏗️ [`starlark-expert`](skills/starlark-expert) | Consult and generate scripts written in Starlark (e.g. for Bazel, Buck, etc.). |
| **🗂️ Data & Schemas** | |
| 🏷️ [`proto-schema-expert`](skills/proto-schema-expert) | Draft, design, and clarify Protobuf schemas (Proto2/Proto3/Editions). |

---

## ⚡ Quick Start

### 1️⃣ Development Container (Recommended)

This repository includes a robust **[Dev Container](https://containers.dev/)** configured with Ubuntu, Python, Pre-commit, Git LFS, and AI agent dependencies.

1. Open this repository in Visual Studio Code.
2. Hit `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac).
3. Search and select: **Dev Containers: Reopen in Container**.

### 2️⃣ Local Setup

If developing locally:

```bash
# Install pre-commit globally or in a virtualenv
pip install pre-commit

# Install git hook scripts
pre-commit install

# Run against all files manually
pre-commit run --all-files
```

---

## ✍️ Creating a New Skill

Follow our standard directory topography when authoring new instructions:

1. **`SKILL.md`**: Keep it minimal and actionable. This defines the agent's persona, strict rules, and routing logic.
2. **`references/`**: Heavy documentation and rulesets. Read dynamically by agents only when needed.
3. **`assets/`**: Executable templates, JSON schemas, or example configurations.
4. **`scripts/`**: Helpers (e.g., Python validation scripts).

> 💡 **Tip:** Refer to the `skill-crafter` to help generate your new skills!

---

> _Managed by AI, built for AI._
> Check out [`AGENTS.md`](AGENTS.md) to understand how AI operates within this repository.

For CI, repository workflows also run secret scanning checks.

## 🤝 Contributing

Contributions are welcome! Suggested flow:

1. Create or update a skill under `skills/`
2. Keep changes focused and minimal
3. Run `pre-commit run --all-files`
4. Open a pull request with a clear summary and rationale

*If you are creating a new skill, use the custom agent definition in `.github/agents/agents-crafter.agent.md` as a structural reference.*

## 📄 License

Licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for details.
