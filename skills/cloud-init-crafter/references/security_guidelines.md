# Security Guidelines

Cloud-init automates cloud instance initialization. Because user-data configuration is processed at boot and may be accessible to others on the local network depending on the cloud platform's Instance Metadata Service (IMDS), adhering to strict security practices is required.

## 1. Updated Packages

To ensure available security fixes are applied to VM images upon launch, update packages on first boot.

**Example:**

```yaml
#cloud-config
package_update: true
package_upgrade: true
```

## 2. No Plaintext Passwords or Credentials

The most significant security exposure comes from custom user-data or scripts providing credentials in clear text or encoded in URLs.

* **No Hardcoded Credentials:** Do not include plaintext passwords or credentials in any `runcmd`, `bootcmd`, or user-data scripts (e.g., `#!/bin/bash`).
* **Credential Retrieval:** Retrieve credentials for service endpoints dynamically from a secure vault or configuration management service (e.g., Puppet, Chef, Ansible, SaltStack) rather than embedding them in user-data.
* **User Creation:** When creating users, **never** use the `plain_text_passwd` key. Always use `hashed_passwd` as a secure alternative.
* **Password Setting:** Avoid plaintext passwords when using the `chpasswd` module.

## 3. SSH Key Authentication

Rely on SSH public/private key pairs for access rather than user passwords.

* Use `ssh_authorized_keys` to import standard SSH public keys for users.
* Use `ssh_import_id` to import public keys from trusted sources like GitHub or Launchpad.

## 4. SSH Host Key Validation

To prevent man-in-the-middle (MITM) attacks, validate the machine you are connecting to.

* Cloud-init publishes the generated SSH host public keys to the instance's **serial console**.
* Always validate these keys from the serial console output prior to establishing any SSH client connection to the newly launched VM.
