---
name: cloud-init-crafter
description: Expert assistant for creating, modifying, and debugging cloud-init and cloud-config (YAML) scripts. Focuses on security, idempotency, and multi-platform validation.
---
# Cloud-init Crafter

This skill provides a structured framework for generating and maintaining `cloud-init` configurations. It utilizes a library of baseline templates, localized reference guides, and automated validation scripts to ensure production-ready deployments.

## Core Principles

1. **Plan Before Execution:** Always define a concise implementation plan (listing target modules, baseline templates, and validation logic) before generating code.
2. **Standard Formatting:** Configurations MUST start with `#cloud-config` on the first line and adhere to YAML 1.1 specifications.
3. **Security by Default:** Prohibit plaintext passwords. Use `ssh_authorized_keys` or `hashed_passwd` exclusively.
4. **Idempotency:** Ensure all `runcmd`, `bootcmd`, and custom scripts are idempotent to allow safe re-execution.

## Assets (Baseline Templates)

Use these templates as a starting point for new configurations. Load them only when establishing a new baseline:
* [Minimal Template](assets/minimal_template.yaml) - Essential SSH-only access with password authentication disabled.
* [Default Template](assets/default_template.yaml) - Standard baseline for production including users, SSH keys, and package updates.
* [Complete Template](assets/complete_template.yaml) - Comprehensive setup including disk partitioning, file writing, and complex orchestration.

## Local References

Load these reference documents on-demand when specific technical details or troubleshooting steps are required:
* [Concepts and Boot Stages](references/concepts_and_boot_stages.md) - Overview of cloud-init principles and the five boot stages (Detect, Local, Network, Config, Final).
* [Cloud-config API](references/cloud_config_api.md) - Detailed syntax, configuration schema, and examples for common configuration modules.
* [Best Practices](references/best_practices.md) - Strategic guidelines for writing robust, idempotent, and maintainable cloud-init scripts.
* [Security Guidelines](references/security_guidelines.md) - Critical security hardening, credential management, and SSH host key verification.
* [CLI Reference](references/cli_reference.md) - Comprehensive command-line interface guide for `cloud-init` and `cloud-init-per`.
* [Error Cheatsheet](references/error_cheatsheet.md) - Troubleshooting workflows, log paths, status codes, and common failure modes.

### Platform Launching Guides
* [QEMU Launching](references/launching/qemu.md) - Guide for local instance testing using QEMU and the NoCloud datasource.
* [LXD Launching](references/launching/lxd.md) - Guide for testing with LXD containers using native configuration keys and profiles.
* [Multipass Launching](references/launching/multipass.md) - Guide for launching Ubuntu VMs with cloud-init on Linux, Windows, or macOS.
* [Libvirt Launching](references/launching/libvirt.md) - Guide for using `virt-install` to automate cloud-init seed image creation and deployment.
* [WSL Launching](references/launching/wsl.md) - Specific requirements for using cloud-init with Ubuntu 24.04+ on Windows Subsystem for Linux.

## Validation Tools
* [Config Validator](scripts/validate_config.py) - A Python script (PEP 723) to offline validate YAML syntax and the mandatory `#cloud-config` header.

## Official Documentation

Refer to these external resources for the most granular and up-to-date specifications:
* [Official Documentation](https://docs.cloud-init.io/en/latest/index.html) - Main landing page for all official cloud-init guides.
* [Cloud-config Modules Reference](https://docs.cloud-init.io/en/latest/reference/modules.html) - Detailed parameters and syntax for all available configuration modules.
* [Datasources Reference](https://docs.cloud-init.io/en/latest/reference/datasources.html) - Information on platform datasources and instance metadata retrieval.
* [Advanced Customization](https://docs.cloud-init.io/en/latest/reference/advanced_reference.html) - Reference for advanced configurations like part-handlers and boothooks.
* [Local Launching & Testing](https://docs.cloud-init.io/en/latest/howto/launching.html) - Official guides for local validation and instance launching.

## Standard Operating Procedure (SOP)

1. **Planning:** Analyze requirements and output a concise plan detailing the target modules, the selected baseline template, and any necessary reference documents.
2. **Execution:** Generate or modify the YAML configuration block adhering to formatting and security constraints.
3. **Validation:** Recommend validation via `cloud-init schema -c <file> --annotate` or the provided `scripts/validate_config.py` tool.
