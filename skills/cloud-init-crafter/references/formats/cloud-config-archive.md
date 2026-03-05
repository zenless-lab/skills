# Cloud Config Archive

**Type:** `#cloud-config-archive`
**Format:** YAML List of Dictionaries

A simpler YAML alternative to building raw MIME multi-part archives for specifying more than one type of data.

## Fields Reference

- `type` (**Required**): The Content-Type identifier (e.g., `text/cloud-boothook`, `text/cloud-config`).
- `content` (**Required**): The actual user-data configuration payload.
- `launch-index` (*Optional*): The EC2 Launch-Index.
- `filename` (*Optional*): Used only if a user-data format requires a filename in a MIME part.
- *Any other fields are interpreted as MIME part headers.*

## Example Configuration

```yaml
#cloud-config-archive
- type: "text/cloud-boothook"
  content: |
    #!/bin/sh
    echo "this is from a boothook." > /var/tmp/boothook.txt
- type: "text/cloud-config"
  content: |
    bootcmd:
    - echo "this is from a cloud-config." > /var/tmp/bootcmd.txt
```
