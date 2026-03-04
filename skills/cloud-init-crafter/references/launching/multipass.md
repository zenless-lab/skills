# Local Testing with Multipass

Multipass is a cross-platform tool for launching Ubuntu VMs on Linux, Windows, and macOS.

## 1. Usage

Pass the `user-data` file using the `--cloud-init` flag.

```bash
multipass launch noble --name test-vm --cloud-init user-data.yaml
```

## 2. Constraints

* **Validation**: Multipass validates the `user-data` file before starting the VM.
* **Format**: It strictly supports the *user-data cloud-config* format. Other formats like scripts or boothooks might be rejected by the pre-launch validator.

## 3. Official Reference

* [Multipass Documentation](https://multipass.run/)
