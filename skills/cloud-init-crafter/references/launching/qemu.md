# Local Testing with QEMU

QEMU is a versatile hardware emulator. The `NoCloud` datasource allows passing configuration to local cloud images without a network service, making it ideal for rapid development.

## 1. Prepare Configuration Files

Ensure the following files exist in your working directory:

* `user-data`: Your YAML `#cloud-config`.
* `meta-data`: Instance metadata (e.g., `instance-id`).
* `network-config`: Optional network settings.

## 2. Method A: ISO Seed Image

Create a seed disk using `genisoimage` to pass files to the instance.

```bash
genisoimage \
    -output seed.img \
    -volid cidata -rational-rock -joliet \
    user-data meta-data network-config
```

### Boot with ISO

```bash
qemu-system-x86_64 -m 1024 -net nic -net user \
    -drive file=noble-server-cloudimg-amd64.img,index=0,format=qcow2,media=disk \
    -drive file=seed.img,index=1,media=cdrom \
    -machine accel=kvm:tcg
```

## 3. Method B: SMBIOS Serial (No Disk)

On supported images, pass a URL directly via the SMBIOS serial string.

```bash
qemu-system-x86_64 -m 1024 -net nic -net user \
    -hda noble-server-cloudimg-amd64.img \
    -smbios type=1,serial=ds='nocloud;s=[http://10.0.2.2:8000/](http://10.0.2.2:8000/)'
```

*Note: `10.0.2.2` is the default gateway to the host from within QEMU.*

## 4. Validation

* **Wait for completion**: `cloud-init status --wait`
* **Official Reference**: [Datasource NoCloud](https://docs.cloud-init.io/en/latest/reference/datasources/nocloud.html)
