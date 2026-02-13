# Editions Guide (2023+)

**Editions** replace the binary `syntax` model with a continuous evolution model based on **Features**.

## Key Changes
1.  **Header**: Use `edition = "2023";` instead of `syntax`.
2.  **No `syntax` keyword**: The concept is obsolete.
3.  **No `required`**: Strictly removed.
4.  **No `group`**: Removed (replaced by delimited encoding).

## Feature Configuration
Behaviors are controlled via `features`.

| Behavior | Proto2 Equivalent | Proto3 Equivalent | Editions Config |
| :--- | :--- | :--- | :--- |
| **Presence** | `optional` | `optional` | `[features.field_presence = EXPLICIT]` |
| **Implicit** | N/A | Default (Singular) | `[features.field_presence = IMPLICIT]` |
| **Enums** | Closed | Open | `option features.enum_type = OPEN;` |

### Example
```protobuf
edition = "2023";
package my.pkg;

message User {
  // Explicit presence (has_name generated)
  string name = 1 [features.field_presence = EXPLICIT];

  // Implicit presence (no has_age, default 0)
  int32 age = 2 [features.field_presence = IMPLICIT];
}
```
