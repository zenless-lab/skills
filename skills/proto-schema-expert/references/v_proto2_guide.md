# Proto2 Guide

**Proto2** is the legacy syntax, offering fine-grained control but higher complexity.

## Key Characteristics
1.  **Qualifiers Required**: Every field must be `optional`, `required`, or `repeated`.
2.  **Explicit Defaults**: You can specify `[default = value]`.
3.  **Extensions**: Allows extending messages defined in other files (replaced by `Any` in Proto3).

## Example
```protobuf
syntax = "proto2";

message SearchRequest {
  required string query = 1; // Validation fails if missing
  optional int32 page_number = 2 [default = 1]; // Defaults to 1 if unset
}
```
