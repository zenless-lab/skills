# Jinja Template Format

**Type:** `## template: jinja`
**Format:** Jinja2 Template Header

Jinja templates allow the use of instance-data variables (e.g., `{{ v1.instance_id }}`) dynamically within scripts or configs.

## Compatibility

- **Supported for:** cloud-config, user-data scripts, and cloud-boothooks.
- **Not supported for:** meta configs.
- **Requirement:** The template header must be placed above the original format header.

## Example Configurations

**Cloud-config Example:**

```yaml
## template: jinja
#cloud-config
runcmd:
  - echo 'Running on {{ v1.cloud_name }}' > /var/tmp/cloud_name
```

**User-data Script Example:**

```shell
## template: jinja
#!/bin/sh
echo 'Current instance id: {{ v1.instance_id }}' > /var/tmp/instance_id
```
