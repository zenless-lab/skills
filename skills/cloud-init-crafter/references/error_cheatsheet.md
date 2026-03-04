# Error Cheatsheet

This reference provides a centralized guide for log locations, status code definitions, and standardized troubleshooting workflows for `cloud-init`.

## 1. Log Files and Locations

* **`/run/cloud-init/cloud-init-generator.log`**: Early boot logs; useful for diagnosing why `cloud-init` failed to start or was skipped.
* **`/run/cloud-init/ds-identify.log`**: Platform detection logs; records how the datasource was (or was not) identified.
* **`/var/log/cloud-init.log`**: The primary log file; contains detailed, verbose debugging information for all stages.
* **`/var/log/cloud-init-output.log`**: Capture of stdout and stderr for every stage; essential for debugging `runcmd` outputs and user-provided scripts.

## 2. Status and Exit Codes

### CLI Return Codes

When executing `cloud-init status`, the exit code indicates the health of the process:

* **0**: **Success**. All modules completed without error.
* **1**: **Critical Failure**. An unrecoverable error occurred; the instance is in an unknown or broken state.
* **2**: **Recoverable Failure**. The process finished, but one or more modules failed (check `recoverable_errors` in the status output).

### Reported Status Labels

* `not started`: Initial state before execution.
* `running`: Actively executing boot stages.
* `done`: Finished successfully.
* `error - done`: Finished, but encountered at least one critical error.
* `degraded done`: Finished, but encountered recoverable errors (e.g., a non-critical module failed).
* `disabled`: Cloud-init was prevented from running (e.g., by a marker file or kernel command line).

## 3. Standard Troubleshooting Scenarios

### Scenario A: Cannot Log In to the Instance

1. **Serial Console**: Check the cloud provider's serial console for boot errors or SSH host key fingerprints.
2. **Password Access**: Verify if a password was set via `cc_users_groups`. This only works if that specific module reached the "done" state.
3. **Local Reproduction**: Run the same user-data locally via QEMU or LXD to inspect logs in a controlled environment.

### Scenario B: Cloud-init Did Not Run

1. **Check Status**: Run `cloud-init status --long` to view the `boot_status_code`.
2. **Identification Log**: Inspect `/run/cloud-init/ds-identify.log` to see if a valid datasource was detected.
3. **Service Health**: Check the init system services:

   ```bash
   systemctl status cloud-init-local.service cloud-init-network.service \
                    cloud-config.service cloud-final.service
   ```

### Scenario C: Unexpected Behavior (Logical Errors)

1. **Schema Validation**: Run `cloud-init schema --system --annotate` to highlight YAML syntax or constraint violations.
2. **Detailed Errors**: Look for specific keys in `cloud-init status --long` under `errors` or `recoverable_errors`.
3. **Module Output**: Search `/var/log/cloud-init-output.log` for the specific command or module that failed to behave as expected.

### Scenario D: Hangs or Timeouts

1. **Kernel Logs**: Check `dmesg -T | grep -i -e warning -e error -e fatal` for hardware or driver issues.
2. **Blocking Jobs**:

   ```bash
   systemctl list-jobs --after
   # Identify jobs in 'running' state that precede cloud-final.service.
   ```

3. **Process Tree**: Use `pstree <PID>` on the cloud-init process to find child scripts waiting for input or stuck in a deadlock.

## 4. Essential Debugging Commands

* **Verbose Status**: `cloud-init status --long`
* **JSON Analysis**: `cloud-init status --format json`
* **Schema Check**: `cloud-init schema -c <file>.yaml --annotate`
* **Simulate Clean Boot**: `sudo cloud-init clean --logs --reboot`
* **Bug Reporting**: `sudo cloud-init collect-logs` (generates `cloud-init.tar.gz` containing all relevant logs and system info).
