# Cloud-init Concepts and Boot Stages

This document outlines the core architecture of `cloud-init`, including configuration priorities, data sources, and the chronological execution of boot stages.

## 1. Core Architecture

`cloud-init` acts as the bridge between the cloud provider's infrastructure and the guest operating system. It consumes data from a **Datasource** to initialize the system according to the user's requirements.

### Data Types

* **User-data:** Instructions provided by the user (e.g., `#cloud-config` YAML or scripts). This is the most common way to customize an instance.
* **Vendor-data:** Configuration provided by the cloud platform or image creator to optimize the instance for that specific environment.
* **Meta-data:** Platform-specific information such as instance ID, hostname, and network configuration.

### Configuration Priority

Settings are prioritized by their source. A higher-priority source overrides a lower-priority one:

1. **Runtime Configuration:** Fetched from the datasource at launch. Includes user-data and vendor-data.
2. **Image Configuration:** Baked into the image before boot. Includes:
    * Machine-generated config: `/run/cloud-init/cloud.cfg`.
    * Configuration directories: `/etc/cloud/cloud.cfg` and `/etc/cloud/cloud.cfg.d/*.cfg`.
3. **Built-in Defaults:** Hardcoded defaults within the `cloud-init` source code.

---

## 2. The Five Boot Stages

`cloud-init` execution is divided into five sequential stages. Understanding these is critical for debugging timing-related issues.

| Stage | Service Name | Description | Key Actions |
| :--- | :--- | :--- | :--- |
| **Detect** | `ds-identify` | Platform identification. | Detects the datasource (e.g., AWS, Azure). If none is found, cloud-init is disabled to save boot time. |
| **Local** | `cloud-init-local` | Pre-networking setup. | Mounts `/` as RW, finds local datasources, and applies initial network configuration. **Blocks network bring-up.** |
| **Network** | `cloud-init-network` | Post-networking setup. | Networking is online. Fully processes user-data, fetches `#include` files, handles disks/mounts, and runs **boothooks**. |
| **Config** | `cloud-config` | Configuration modules. | Runs non-blocking configuration modules (e.g., `runcmd`). Does not block login. |
| **Final** | `cloud-final` | Late initialization. | Runs package installations, configuration management (Ansible/Chef), and user scripts. Comparable to `rc.local`. |

---

## 3. User-Data Formats

`cloud-init` identifies the content type using unique headers on the first line:

* **Cloud-config (`#cloud-config`):** YAML format for declarative state definition. Most common.
* **User-data Script (`#!/bin/sh`):** A shell script executed once during the **Final** stage.
* **Cloud Boothook (`#cloud-boothook`):** A script executed very early during the **Network** stage. **Runs on every boot.**
* **Include File (`#include`):** A list of URLs to be read; content can be any valid user-data format.
* **Jinja Template (`## template: jinja`):** Allows using instance variables (e.g., `{{ v1.instance_id }}`) within configurations.
* **Cloud-config Archive (`#cloud-config-archive`):** A YAML list containing multiple content types with specific metadata.

---

## 4. Failure Modes and Exit Codes

When running `cloud-init status`, the return code indicates the health of the initialization process:

* **0 (Success):** All tasks completed successfully.
* **1 (Critical Failure):** An unrecoverable error occurred (e.g., broken image or serious bug). Check `errors` in status output.
* **2 (Recoverable Failure):** Cloud-init finished, but some modules failed or warnings occurred. Check `recoverable_errors`.

### Reported Statuses

* `not started`: Execution has not yet begun.
* `running`: Cloud-init is currently processing a stage.
* `done`: Execution finished without critical errors.
* `degraded`: Execution finished but experienced recoverable errors or warnings.
* `disabled`: Cloud-init was explicitly disabled (e.g., via `/etc/cloud/cloud-init.disabled`).

---

## 5. See Also

* See [the Cloud-config API reference](references/cloud_config_api.md) for module syntax.
* See [the Error Cheatsheet](references/error_cheatsheet.md) for log analysis and troubleshooting.
* See [the Security Guidelines](references/security_guidelines.md) for hardening your configuration.
