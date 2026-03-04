# Local Testing with LXD

LXD offers a streamlined experience for Linux system containers with first-class `cloud-init` support.

## 1. Pass Configuration at Launch

The fastest way to test a single configuration:

```bash
lxc launch ubuntu:noble test-container --config=user.user-data="$(cat user-data.yaml)"
```

## 2. Using Profiles (Reusable)

Create a reusable profile for development environments:

```bash
lxc profile create dev-config
lxc profile set dev-config user.user-data - < user-data.yaml
lxc launch ubuntu:noble test-container -p default -p dev-config
```

## 3. Data Mapping Table

LXD maps configuration keys as follows:

| Data Type | LXD Configuration Option |
| :--- | :--- |
| **user-data** | `cloud-init.user-data` (or `user.user-data`) |
| **vendor-data** | `cloud-init.vendor-data` |
| **network-config** | `cloud-init.network-config` |

## 4. Verification

Execute a shell inside the container to check status:

```bash
lxc shell test-container
cloud-init status --wait
cloud-init query userdata # Inspect the received data
```

## 5. Official Reference

* [LXD Instance Configuration](https://documentation.ubuntu.com/lxd/en/latest/instances/)
* [Custom Network Configuration](https://documentation.ubuntu.com/lxd/en/latest/cloud-init/)
