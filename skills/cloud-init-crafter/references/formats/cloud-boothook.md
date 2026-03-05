# Cloud Boothook Format

**Type:** `#cloud-boothook`
**Format:** Shell script

A cloud boothook is a script run very early in the boot process, during the network stage, before any other cloud-init modules are executed.

## Execution Frequency

- Runs **every boot**.

## Important Notes

- **Warning:** The use of the `INSTANCE_ID` environment variable within boothooks is deprecated. Use Jinja templates with `v1.instance_id` instead.

## Example Configuration

```shell
#cloud-boothook
#!/bin/sh
echo <REDACTED_IP_ADDRESS> <REDACTED_HOSTNAME> > /etc/hosts
```

**Once-per-instance pattern:**

```bash
#cloud-boothook
#!/bin/sh

# Early exit 0 when script has already run for this instance-id
cloud-init-per instance do-hosts /bin/false && exit 0
echo <REDACTED_IP_ADDRESS> <REDACTED_HOSTNAME> >> /etc/hosts
```
