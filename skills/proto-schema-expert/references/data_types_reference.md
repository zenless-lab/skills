# Protocol Buffers Data Types & Version Evolution

This reference details the scalar types and highlights critical behavioral differences between **Proto2**, **Proto3**, and **Editions**.

## 1. Scalar Value Types

| .proto Type | Description | Notes on Encoding |
| :--- | :--- | :--- |
| **double** | 64-bit floating point | Fixed 8 bytes. |
| **float** | 32-bit floating point | Fixed 4 bytes. |
| **int32** | Variable-length encoding (Varint). | Inefficient for negative numbers. |
| **int64** | Variable-length encoding (Varint). | Inefficient for negative numbers. |
| **uint32** | Varint. Unsigned. | |
| **uint64** | Varint. Unsigned. | |
| **sint32** | ZigZag encoded Varint. | **Efficient for negative numbers.** |
| **sint64** | ZigZag encoded Varint. | **Efficient for negative numbers.** |
| **fixed32** | Fixed 4 bytes. Unsigned. | More efficient than uint32 for large values (>2^28). |
| **fixed64** | Fixed 8 bytes. Unsigned. | More efficient than uint64 for large values (>2^56). |
| **sfixed32** | Fixed 4 bytes. Signed. | |
| **sfixed64** | Fixed 8 bytes. Signed. | |
| **bool** | Boolean value. | Encoded as varint (0 or 1). |
| **string** | UTF-8 encoded string. | Max length 2^32. |
| **bytes** | Arbitrary byte sequence. | Max length 2^32. |

---

## 2. Critical Version Differences

### A. Field Rules (Cardinality)

| Feature | Proto2 | Proto3 | Editions (2023+) |
| :--- | :--- | :--- | :--- |
| **required** | **Supported** (Discouraged). Parsing fails if missing. | **REMOVED**. | **REMOVED**. (Can be simulated with `features.field_presence = LEGACY_REQUIRED` only for migration). |
| **optional** | **Supported**. Explicit presence. Generates `has_x()` methods. | **Supported** (v3.15+). Restores explicit presence. Prior to v3.15, fields were implicit only. | **Supported**. Controlled via `features.field_presence = EXPLICIT`. |
| **repeated** | **Supported**. Not packed by default. Requires `[packed=true]`. | **Supported**. **Packed by default** for scalar numeric types. | **Supported**. Packed by default (configurable via features). |

### B. Default Values

* **Proto2**: Supports explicit default values in the schema.
    ```protobuf
    optional int32 result_per_page = 3 [default = 10];
    ```
* **Proto3**: **NO explicit defaults**. Fields default to their "zero value":
    * Numbers: `0`
    * Strings: `""`
    * Bool: `false`
    * Enums: The `0` value.
    * *Reasoning*: Simplifies parsing and removes ambiguity between "unset" and "default".
* **Editions**: Follows the Proto3 zero-value philosophy. Explicit defaults are generally discouraged or removed in favor of application-level logic.

### C. Enums

* **Proto2**: First value can be any integer. Enums are "Closed" (parsing fails on unknown values).
* **Proto3**: **First value MUST be 0**. Enums are "Open" (unknown values are preserved).
    ```protobuf
    enum Status {
      STATUS_UNSPECIFIED = 0; // Mandatory
      STATUS_ACTIVE = 1;
    }
    ```
* **Editions**: Defaults to "Open", but can be configured as "Closed" via `features.enum_type = CLOSED`.

### D. Maps

* **Proto2**: Supported via special syntax only in newer compiler versions.
* **Proto3**: First-class support. `map<key_type, value_type> map_field = N;`.
    * *Note*: Map fields cannot be `repeated`, `optional`, or `required`.

---

## 3. Special Types

* **Any (`google.protobuf.Any`)**:
    * *Usage*: Replaces Proto2 `extensions`. Allows embedding arbitrary messages without .proto dependency at compile time.
* **Oneof**:
    * *Usage*: A union where only one field can be set at a time.
    * *Note*: `oneof` fields explicitly track presence in all versions.
