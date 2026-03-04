# Local Testing with Libvirt

Libvirt manages VMs and containers, typically using `virt-install` for deployment.

## 1. Automated Seed Generation

The `virt-install` tool can automatically generate and attach a seed image:

```bash
virt-install --name cloud-init-vm --memory 4000 --noreboot \
    --os-variant detect=on,name=ubuntunoble \
    --disk=size=10,backing_store="$(pwd)/noble-server-cloudimg-amd64.img" \
    --cloud-init user-data="$(pwd)/user-data,meta-data=$(pwd)/meta-data,network-config=$(pwd)/network-config"
```

## 2. Key Parameters

* `--cloud-init`: Orchestrates the creation of the configuration drive.
* `backing_store`: Uses the cloud image as a read-only base to prevent accidental modification of the original.

## 3. Official Reference

* [Libvirt Project](https://libvirt.org/)
