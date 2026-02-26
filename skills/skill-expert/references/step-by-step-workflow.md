# Agent Skill Core Workflow Guide

This document defines the Standard Operating Procedure (SOP) for building, editing, and refactoring Agent Skills. As an Agent executing file operations, you **MUST** strictly follow these three major stages sequentially to ensure modular, compliant, and highly reliable outputs.

## Stage 1: Global Planning & Reflection

Before generating or modifying any files, you must build a complete global perspective internally and refine your plan autonomously.

1. **Current State Assessment (For Edits/Refactoring only)**:
   * Read the existing `SKILL.md`, directory structure, scripts, and reference files to fully understand the skill's current state and boundaries.
2. **Formulate a Global Plan**:
   * **Goal**: What core task must this skill accomplish?
   * **Inclusions**: List all necessary files and their specific purposes (`SKILL.md`, `references/...`, `scripts/...`).
   * **Exclusions**: Explicitly identify what files are *not* needed to avoid over-engineering.
   * **Granularity Warning**: Evaluate the size of planned `references/`. If a reference file is extremely short, merge it into `SKILL.md` or another reference file. Fragmented files increase I/O burden and defeat the purpose of progressive disclosure.
3. **Deep Self-Reflection & Autonomous Correction**:
   * Review if the global plan strictly adheres to agentskills.io specs (e.g., naming conventions, progressive disclosure).
   * **Self-Correct**: If redundancies or compliance issues are found, immediately adjust the plan. Do NOT wait for user confirmation to proceed.

## Stage 2: Creating or Editing Files

Apply the global plan from Stage 1 using a **Top-Down (Overall to Local)** strategy.

1. **Adhere to the Top-Down Order**:
   * **Step 1 (Core)**: ALWAYS start with `SKILL.md`. **Note: If evaluating an existing `SKILL.md` reveals it is in good condition and requires no changes, DO NOT force modifications.** Proceed to the next layer.
   * **Step 2 (Dependencies)**: Following the top-down principle, sequentially create or edit `references/`, `scripts/`, and `assets/`.
2. **Execute the "Local Plan -> Apply" Loop**:
   * For *every* file being processed, before outputting the file content, you MUST output a brief **Local Plan** explaining the file's specific structure, core logic, and its relations to other files.
   * Immediately following the local plan, output the complete file content using the designated code block formatting.
   * Ensure all internal links use **relative paths** (e.g., `scripts/run.py`).
   * Ensure newly created Python scripts include PEP 723 inline metadata (`# /// script ...`).

## Stage 3: Validating and Fixing Issues

Generating files is not the end. You must validate your work using automated tools to ensure strict compliance.

1. **Invoke Validation Scripts**:
   * Actively run the three dedicated validation tools provided in this manager's `scripts/` directory against the target skill:
     * `uvx scripts/validate_skill_md.py <target_skill_dir>`
     * `uvx scripts/validate_references.py <target_skill_dir>`
     * `uvx scripts/validate_scripts.py <target_skill_dir>`
2. **Analyze and Process Results**:
   * Carefully read the returned `[ERROR]`, `[WARNING]`, and `[INFO]` logs.
   * **Resolve Fatal Errors (`[ERROR]`)**: Issues that break the skill (e.g., malformed YAML, missing PEP 723, broken paths) MUST be analyzed and fixed immediately by editing the file again.
   * **Evaluate and Shelve Minor Issues (`[WARNING]`/`[INFO]`)**: Reflect on advisory warnings. If you determine the current state is optimal for the specific context, you may skip the fix, but you MUST briefly explain your reasoning in your internal logic or output.
