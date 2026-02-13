# Proto3 Guide

**Proto3** simplifies the language and improves interoperability (especially with JSON).

## Key Characteristics
1.  **Implicit Presence (Singular fields)**: By default, scalar fields do not track presence. A value of `0` is indistinguishable from "unset".
2.  **`optional` Keyword**: Added back in protoc 3.12 (experimental), GA in 3.15+, to allow checking presence (e.g., `has_field()`).
3.  **JSON Mapping**: Defines a canonical JSON encoding (lowerCamelCase names).
4.  **No `required`**: Removed to improve evolution safety.

## Example
```protobuf
syntax = "proto3";

message SearchRequest {
  string query = 1; // Implicit presence (default "")
  int32 page_number = 2; // Implicit presence (default 0)
  optional int32 results_per_page = 3; // Explicit presence (can be null/unset)
}
```
