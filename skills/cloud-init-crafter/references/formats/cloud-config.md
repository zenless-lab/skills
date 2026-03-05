# Cloud Config Format

**Type:** `#cloud-config`
**Format:** YAML

Cloud-config is used to define how an instance should be configured in a human-friendly YAML format. It uses keys to describe the desired instance state.

## Common Use Cases

- Performing package upgrades on first boot
- Configuring different package mirrors or sources
- Initial user or group setup
- Importing SSH keys or host keys

## Execution Frequency

Modules processing cloud-config data may run once per instance, every boot, or once ever, depending on the specific module associated with the configuration.

## Example Configuration

```yaml
#cloud-config
password: <REDACTED_PASSWORD>
chpasswd:
  expire: False
```
