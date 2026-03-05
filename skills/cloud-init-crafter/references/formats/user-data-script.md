# User-data Script Format

**Type:** Standard Shell Script (e.g., `#!/bin/sh`)
**Format:** Shell script

A single script to be executed relatively late in the boot process, during cloud-init's final stage as part of the `cc_scripts_user` module.

## Execution Frequency

- Runs **once per instance**.

## Important Notes

- **Warning:** The use of the `INSTANCE_ID` environment variable within user-data scripts is deprecated. Use Jinja templates with `v1.instance_id` instead.

## Example Configuration

```shell
#!/bin/sh
echo "Initialization Complete" > /var/tmp/output.txt
```
