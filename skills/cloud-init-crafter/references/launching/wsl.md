# Using Cloud-init with WSL

Ubuntu 24.04 and later versions support `cloud-init` within Windows Subsystem for Linux (WSL).

## 1. Configuration Path

User-data must be placed in a specific Windows directory for the WSL datasource to pick it up.

* **Directory**: `%USERPROFILE%\.cloud-init\`
* **Filename**: `Ubuntu-24.04.user-data` (Matches the distribution name).
* **Extension**: Must be `.user-data` (not `.txt`).

## 2. Example Setup (PowerShell)

```powershell
# Create the directory
mkdir ~/.cloud-init
# Save your config to: ~/.cloud-init/Ubuntu-24.04.user-data
```

## 3. Deployment

Install the distribution via the Microsoft Store or CLI:

```powershell
wsl --install --distribution Ubuntu-24.04
```

## 4. Verification (Inside WSL)

```bash
cloud-init status --wait
cloud-id # Expected output: wsl
cat /var/tmp/hello-world.txt # Check file results
```

## 5. Official Reference

* [WSL Datasource Reference](https://docs.cloud-init.io/en/latest/reference/datasources/wsl.html)
