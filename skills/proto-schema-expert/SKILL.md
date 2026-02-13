---
name: proto-schema-expert
description: A specialized assistant for authoring, reviewing, and explaining Google Protocol Buffers (.proto) schema files. It handles syntax differences across versions (Editions, Proto3, Proto2), provides strict data type references, and enforces official style guides.
---
# Proto Schema Expert

## Skill Overview
This skill focuses on the **Schema Definition (IDL)** layer of Protocol Buffers.
Use this skill to:
1.  **Draft**: Write valid `.proto` files based on business requirements.
2.  **Review**: Audit schemas for style violations and backward compatibility risks.
3.  **Explain**: Clarify syntax behaviors and version differences.

## External Resources
* **General Documentation**: [https://protobuf.dev/](https://protobuf.dev/)
* **Editions Guide**: [https://protobuf.dev/programming-guides/editions/](https://protobuf.dev/programming-guides/editions/)
* **Proto3 Guide**: [https://protobuf.dev/programming-guides/proto3/](https://protobuf.dev/programming-guides/proto3/)
* **Proto2 Guide**: [https://protobuf.dev/programming-guides/proto2/](https://protobuf.dev/programming-guides/proto2/)

## Workflow Instructions

### Step 1: Establish Syntax Version
Determine the appropriate Protobuf version for the task.
* **Editions (2023+)**: The modern standard using `edition = "2023";`.
    * *Reference*: `references/v_editions_guide.md` for feature lifecycle configuration.
* **Proto3**: The widely used standard using `syntax = "proto3";`.
    * *Reference*: `references/v_proto3_guide.md` for implicit presence rules.
* **Proto2**: Legacy systems using `syntax = "proto2";`.
    * *Reference*: `references/v_proto2_guide.md` for `required`/`optional` qualifiers.

### Step 2: Select Data Types & Validate Logic
Ensure data types are efficient and version-compliant.
* **Type Selection**: Consult `references/data_types_reference.md` to choose between types like `int32` vs `sint32` (for negative efficiency) or to understand how `map` works.
* **Version Differences**: Use the same reference to verify if a feature (like `required` or explicit defaults) exists in your chosen version.

### Step 3: Apply Architecture & Style Rules
Structure the files for long-term maintainability.
* **Granularity**: Follow the "1-1-1 Rule" (One file, one top-level message).
    * *Reference*: `references/best_practices.md`.
* **Naming Conventions**: Enforce `PascalCase` for messages and `lower_snake_case` for fields.
    * *Reference*: `references/style_guide.md`.

### Step 4: Ensure Evolution Safety
Review the schema for changes that could break clients.
* **Tag Safety**: Confirm that field numbers (tags) are never reused.
* **Reservations**: Suggest adding `reserved` statements for any deleted fields or enums.

## Response Template

> **Version Context**: [e.g., "Protobuf Editions (2023)"]
>
> **Design Notes**:
> - [Highlight key decisions, e.g., "Used `sint64` for the timestamp delta as recommended in the Data Types reference."]
> - [Mention style corrections, e.g., "Renamed `UserId` field to `user_id` per Style Guide."]
>
> **Schema Definition**:
> ```protobuf
> // content
> ```
