# MIME Multi-part Archive Format

**Format:** Standard MIME multipart message

Allows the user to specify more than one type of data (e.g., combining a user-data script and a cloud-config file) in a single payload.

## Requirements

- Each part must specify a valid content-type.
- You can list supported types via the command line: `cloud-init devel make-mime --list-types`

## Helper Subcommand

Use the `make-mime` subcommand to generate these files automatically by passing `filename:mimetype` pairs.

**Examples:**

Create user-data containing both cloud-config and a shell script:

```shell-session
cloud-init devel make-mime -a config.yaml:cloud-config -a script.sh:x-shellscript > user-data.mime
```

Create user-data with specific execution frequencies:

```shell-session
cloud-init devel make-mime -a always.sh:x-shellscript-per-boot -a instance.sh:x-shellscript-per-instance -a once.sh:x-shellscript-per-once
```

## Example Raw Message

```text
Content-Type: multipart/mixed; boundary="===============<RANDOM_BOUNDARY_STRING>=="
MIME-Version: 1.0
Number-Attachments: 2

--===============<RANDOM_BOUNDARY_STRING>==
Content-Type: text/cloud-boothook; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="part-001"

#!/bin/sh
echo "this is from a boothook." > /var/tmp/boothook.txt

--===============<RANDOM_BOUNDARY_STRING>==
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="part-002"

bootcmd:
- echo "this is from a cloud-config." > /var/tmp/bootcmd.txt
--===============<RANDOM_BOUNDARY_STRING>==--
```
