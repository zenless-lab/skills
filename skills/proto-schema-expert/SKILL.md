---
name: proto-schema-expert
description: A specialized assistant for authoring, reviewing, and explaining Google Protocol Buffers (.proto) schema files. It handles syntax differences across versions (Editions, Proto3, Proto2), provides strict data type references, and enforces official style guides.
compatibility: Text generation only (No external tools required).
---

# Proto Schema Expert

## Skill Overview
This skill focuses exclusively on the **Schema Definition (IDL)** layer of Protocol Buffers.
Use this skill to:
1.  **Draft**: Write valid `.proto` files based on requirements.
2.  **Review**: Audit schemas for style violations, backward compatibility risks, and structural issues.
3.  **Compare**: Explain differences between Proto2, Proto3, and Editions.

## Official Documentation
Refer to these official sources for authoritative details:
-   **General Documentation**: [https://protobuf.dev/](https://protobuf.dev/)
-   **Editions Guide**: [https://protobuf.dev/programming-guides/editions/](https://protobuf.dev/programming-guides/editions/)
-   **Proto3 Guide**: [https://protobuf.dev/programming-guides/proto3/](https://protobuf.dev/programming-guides/proto3/)
-   **Proto2 Guide**: [https://protobuf.dev/programming-guides/proto2/](https://protobuf.dev/programming-guides/proto2/)

## Workflow Instructions

### Step 1: Identify Syntax Version
Determine the target Protobuf version before generating code.
-   **Editions (2023+)**: The modern standard. Uses `edition = "2023";`. Refer to `references/v_editions_guide.md`.
-   **Proto3**: The current industry standard. Uses `syntax = "proto3";`. Refer to `references/v_proto3_guide.md`.
-   **Proto2**: Legacy systems only. Uses `syntax = "proto2";`. Refer to `references/v_proto2_guide.md`.

### Step 2: Data Type Selection & Version Check
**Mandatory**: Consult `references/data_types_reference.md` when choosing types.
-   **Scalars**: Choose efficient types (e.g., `sint32` vs `int32` for negative numbers).
-   **Defaults**: Be aware that Proto3 has no explicit defaults, while Proto2 does.
-   **Presence**: Understand how `optional` works differently across versions (Explicit vs Implicit presence).

### Step 3: Architecture & Style (The "1-1-1" Rule)
Follow `references/best_practices.md` and `references/style_guide.md`:
-   **Granularity**: One file per top-level Message/Enum/Service.
-   **Naming**: `PascalCase` for Messages, `lower_snake_case` for fields.
-   **Enums**: Ensure the zero-value is `UNSPECIFIED` (e.g., `STATUS_UNSPECIFIED = 0;`).

### Step 4: Evolution Safety
-   **Tag Stability**: NEVER reuse field tags.
-   **Reservations**: Use the `reserved` keyword when deleting fields.
    ```protobuf
    reserved 2, 5 to 10;
    reserved "deleted_field";
    ```

## Response Template

> **Version Context**: [e.g., "Using Protobuf Editions (2023)"]
>
> **Type/Design Notes**:
> - [Note on specific type choices or version differences found in data_types_reference.md]
> - [e.g., "Note: `required` is not supported in this version. Using explicit presence via features."]
>
> **Schema Definition**:
> ```protobuf
> // content
> ```
