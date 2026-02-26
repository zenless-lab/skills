# YAML Frontmatter Specification Guide

Every `SKILL.md` file **MUST** begin with YAML frontmatter containing core metadata. Since the Agent only loads this section during the discovery phase, it must be precise and strictly compliant.

## Required Fields

### 1. `name`

The unique identifier for the skill.

* **Length**: 1 - 64 characters.
* **Characters**: Strictly limited to lowercase alphanumeric characters and hyphens (`a-z`, `0-9`, `-`).
* **Format**:
  * Cannot start or end with a hyphen `-`.
  * Cannot contain consecutive hyphens (e.g., `my--skill` is invalid).
* **Consistency**: Must exactly match the name of the parent folder housing the `SKILL.md`.

### 2. `description`

The sole basis for an Agent discovering and activating the skill.

* **Length**: 1 - 1024 characters. Cannot be empty.
* **Content Principle**: Must clearly state *what* the skill does and *when / under what circumstances* it should be used.
* **Best Practices**: Include rich, keyword-heavy trigger scenarios.
  * ✅ **Good**: `Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.`
  * ❌ **Bad**: `Helps with PDFs.` (Lacks specific trigger scenarios and capability details).

## Optional Fields

Keep the frontmatter lean unless specific needs arise.

* **`license`**: Specifies the license. Keep it short (e.g., `MIT` or `Proprietary. LICENSE.txt has complete terms`).
* **`compatibility`**: Indicates specific environment requirements (Max 500 characters). Use only for hard dependencies (e.g., `Requires git, docker, jq, and access to the internet`).
* **`metadata`**: Arbitrary key-value map for extra metadata. Use somewhat unique keys to prevent collisions.
* **`allowed-tools`**: (Experimental) Space-delimited list of pre-approved tools. e.g., `Bash(git:*) Read`.
