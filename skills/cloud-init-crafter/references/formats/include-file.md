# Include File Format

**Type:** `#include`
**Format:** Text (List of URLs)

An include file contains a list of URLs, one per line. Cloud-init will read each URL, and the content can be any valid user-data format.

## Execution Behavior

- If an error occurs while reading a file, the remaining files in the list will **not** be read.

## Example Configuration

```text
#include
https://<YOUR_INTERNAL_DOMAIN>/path/to/cloud-config-run-cmds.txt
https://<YOUR_INTERNAL_DOMAIN>/path/to/cloud-config-boot-cmds.txt
```
