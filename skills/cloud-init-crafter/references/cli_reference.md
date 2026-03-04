# Cloud-init CLI Reference

## cloud-init

Primary executable for interaction. Use `cloud-init <subcommand> --help` for real-time details.

### analyze

Reports on boot process timing.

* `blame`: Most costly operations first.
* `dump`: JSON dump of tracked events.
* `show`: Time-ordered report by stage.
* `boot`: Kernel vs. cloud-init start timestamps.

### clean

Removes artifacts from `/var/lib/cloud` to simulate a fresh boot.

* `--logs`: Remove `/var/log/cloud-init*`.
* `--reboot`: Reboot after cleaning.
* `--machine-id`: Reset `/etc/machine-id`.
* `--configs [all|ssh_config|network|datasource|fstab]`: Remove specific generated configs.
* `--seed`: Remove the seed directory.

### collect-logs

Tars logs and system info (dmesg, journalctl, etc.) for triage.

### query

Queries standardized instance-data.

* `--all`: Dump all as JSON.
* `--list-keys`: List available keys (e.g., `v1.cloud_name`, `instance_id`).
* `--format '<template>'`: Render output via Jinja template.
* `<varname>`: Path to variable (e.g., `cloud-init query ds.meta_data.public_ipv4`).

### schema

Validates cloud-config files.

* `-c <file>`: Path to YAML.
* `-t [cloud-config|network-config]`: Schema type.
* `--annotate`: Show errors directly in output.

### single

Runs a specific module manually.

* `--name <module>`: Module name (e.g., `set_hostname`).
* `--frequency [always|instance|once]`: Override default frequency.

### status

Reports current state. Exit codes: 0 (Success), 1 (Crash), 2 (Recoverable Errors).

* `--long`: Verbose status.
* `--wait`: Block until completion.
* `--format [yaml|json]`: Machine-readable output.

---

## cloud-init-per

Runs a command at a specific frequency.
**Format:** `cloud-init-per <frequency> <name> <command> [args]`
**Example:** `cloud-init-per once my-task echo "done" >> /tmp/log`
