# Instance-data Reference

**Format:** JSON (Accessible via Jinja templates or CLI)

`instance-data` is a JSON object containing instance-specific variables in a standardized format. Cloud-init separates sensitive data so it is only readable by root.

## Usage Requirements

To use `instance-data` in User-data scripts or Cloud-config, the file MUST begin with the Jinja template header:

```text
## template: jinja
```

## Example Configurations

**Cloud-config Example:**

```yaml
## template: jinja
#cloud-config
runcmd:
  - echo 'Public hostname: {{ ds.meta_data.public_hostname }}' > /tmp/metadata
  - echo 'Availability zone: {{ v1.availability_zone }}' >> /tmp/metadata
```

**User-data Script Example:**

```bash
## template: jinja
#!/bin/bash
{% if v1.region == '<YOUR_TARGET_REGION>' -%}
echo 'Installing custom proxies for {{ v1.region }}'
sudo apt-get install my-xtra-fast-stack
{%- endif %}
```

## Standardized `v1` Keys

Standardized `v1` keys are guaranteed to exist on all cloud platforms. Jinja operator characters (like `-` or `.`) in keys are replaced with underscores for safe dot-notation referencing.

| Key | Description | Example Value |
| :--- | :--- | :--- |
| `v1.cloud_name` | Name of the cloud provider | `aws`, `azure`, `openstack` |
| `v1.platform` | Cloud platform instance type | `ec2`, `gce`, `nocloud` |
| `v1.instance_id` | Unique instance ID allocated | `<REDACTED_INSTANCE_ID>` |
| `v1.region` | Physical region / data center | `us-east-2` |
| `v1.availability_zone`| Physical availability zone | `us-east-2b` |
| `v1.local_hostname` | Internal/local hostname | `ip-10-41-41-70` |
| `v1.public_ssh_keys`| List of provided SSH keys | `['ssh-rsa AA...', ...]` |
| `v1.distro` | Linux distribution name | `ubuntu`, `centos`, `alpine` |
| `v1.distro_version` | Linux distribution version | `20.04`, `7.5` |
| `v1.machine` | CPU architecture | `x86_64`, `aarch64` |

## Other Important Top-Level Keys

- `ds`: Datasource-specific data crawled for the specific cloud platform (e.g., `ds.meta_data.public_hostname`).
- `merged_system_cfg`: Merged base configuration. Contains sensitive info.
- `sys_info`: OS, Python, architecture, and kernel info.

## CLI Discovery & Debugging Commands

```shell-session
# List all instance-data keys and values (requires root for sensitive data)
$ sudo cloud-init query --all

# List all top-level instance-data keys available
$ cloud-init query --list-keys

# Test expected value using valid instance-data key path
$ cloud-init query -f "My AMI: {{ds.meta_data.ami_id}}"

# Introspect nested keys on an object
$ cloud-init query -f "{{ds.keys()}}"
```

## JSON Structure Overview (Truncated)

```json
{
  "v1": {
    "cloud_name": "aws",
    "instance_id": "<REDACTED_INSTANCE_ID>",
    "region": "<REDACTED_REGION>",
    "availability_zone": "<REDACTED_AZ>"
  },
  "ds": {
    "meta_data": {
      "ami_id": "<REDACTED_AMI_ID>",
      "local_ipv4": "<REDACTED_PRIVATE_IP>",
      "public_ipv4": "<REDACTED_PUBLIC_IP>"
    }
  },
  "sys_info": {
    "dist": ["ubuntu", "20.04", "focal"],
    "machine": "x86_64"
  }
}
```
