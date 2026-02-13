# Best Practices

## 1. The "1-1-1" Rule
-   **One File, One Message**: ideally, define only one top-level message, enum, or service per file.
-   **Benefits**: Reduces transitive dependencies and compilation time.

## 2. Tag Management
-   **Immutable Tags**: Never change the numeric tag of a field.
-   **Never Reuse**: If a field is removed, its tag is burned.
-   **Use Reserved**:
    ```protobuf
    reserved 2, 15, 9 to 11;
    reserved "foo", "bar";
    ```

## 3. Package Versioning
-   Structure files in directories matching the package.
-   Use version suffixes in packages (e.g., `package my.app.v1`) to allow breaking changes in `v2` without affecting `v1` clients.
