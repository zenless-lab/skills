# Cloud-Config API & Modules Reference

Table of Contents (with line numbers):

- [Ansible](#ansible): Ansible integration and ansible-pull setup(L71 - L176)
- [APK Configure](#apk-configure): Alpine APK repository configuration(L177 - L231)
- [Apt Configure](#apt-configure): APT sources and proxy configuration(L232 - L364)
- [Apt Pipelining](#apt-pipelining): APT HTTP pipeline-depth settings(L365 - L406)
- [Bootcmd](#bootcmd): Early boot command execution(L407 - L434)
- [Byobu](#byobu): System/user Byobu enablement options(L435 - L470)
- [CA Certificates](#ca-certificates): CA trust store management(L471 - L510)
- [Chef](#chef): Chef installation and runtime configuration(L511 - L588)
- [Disable EC2 Instance Metadata Service](#disable-ec2-instance-metadata-service): Disable EC2 metadata route(L589 - L610)
- [Disk Setup](#disk-setup): Partition and filesystem provisioning(L611 - L664)
- [Fan](#fan): Ubuntu fan networking configuration(L665 - L699)
- [Final Message](#final-message): Cloud-init completion message template(L700 - L732)
- [Growpart](#growpart): Partition growth configuration(L733 - L775)
- [GRUB dpkg](#grub-dpkg): GRUB install-device debconf settings(L776 - L814)
- [Install Hotplug](#install-hotplug): Network hotplug enablement(L815 - L854)
- [Keyboard](#keyboard): Keyboard layout/model/variant settings(L855 - L901)
- [Keys to Console](#keys-to-console): SSH key/fingerprint console output control(L902 - L946)
- [Landscape](#landscape): Landscape client install and config(L947 - L1017)
- [Locale](#locale): System locale configuration(L1018 - L1054)
- [LXD](#lxd): LXD init, bridge, and preseed config(L1055 - L1206)
- [MCollective](#mcollective): MCollective install and certificate setup(L1207 - L1251)
- [Mounts](#mounts): fstab mounts and swap file settings(L1252 - L1299)
- [NTP](#ntp): NTP client and time-source configuration(L1300 - L1389)
- [Package Update Upgrade Install](#package-update-upgrade-install): Package update/upgrade/install behavior(L1390 - L1442)
- [Phone Home](#phone-home): Post-boot callback data posting(L1443 - L1482)
- [Power State Change](#power-state-change): Shutdown/reboot policy after cloud-init(L1483 - L1529)
- [Puppet](#puppet): Puppet install and agent configuration(L1530 - L1609)
- [Raspberry Pi Configuration](#raspberry-pi-configuration): Raspberry Pi interfaces and USB gadget mode(L1610 - L1684)
- [Resizefs](#resizefs): Root filesystem resize behavior(L1685 - L1718)
- [Resolv Conf](#resolv-conf): resolv.conf DNS management(L1719 - L1752)
- [Red Hat Subscription](#red-hat-subscription): RHEL subscription registration options(L1753 - L1841)
- [Rsyslog](#rsyslog): Remote logging and rsyslog config(L1842 - L1914)
- [Runcmd](#runcmd): Final-stage command execution(L1915 - L1945)
- [Salt Minion](#salt-minion): Salt Minion install and configuration(L1946 - L2006)
- [Scripts Per Boot](#scripts-per-boot): Scripts executed on every boot(L2007 - L2022)
- [Scripts Per Instance](#scripts-per-instance): Scripts executed once per instance(L2023 - L2040)
- [Scripts Per Once](#scripts-per-once): Scripts executed exactly once(L2041 - L2056)
- [Scripts User](#scripts-user): User-provided script execution(L2057 - L2072)
- [Scripts Vendor](#scripts-vendor): Vendor-data script execution controls(L2073 - L2111)
- [Seed Random](#seed-random): Random seed injection options(L2112 - L2156)
- [Set Hostname](#set-hostname): Hostname and FQDN settings(L2157 - L2204)
- [Set Passwords](#set-passwords): Password and SSH password-auth settings(L2205 - L2265)
- [Snap](#snap): snapd assertions and command execution(L2266 - L2340)
- [Spacewalk](#spacewalk): Spacewalk install and basic registration(L2341 - L2370)
- [SSH](#ssh): SSH host key and authorized key settings(L2371 - L2410)
- [SSH AuthKey Fingerprints](#ssh-authkey-fingerprints): Authorized key fingerprint logging(L2411 - L2439)
- [SSH Import ID](#ssh-import-id): Import keys from Launchpad/GitHub(L2440 - L2462)
- [Timezone](#timezone): System timezone setting(L2463 - L2484)
- [Ubuntu Drivers](#ubuntu-drivers): Ubuntu third-party driver installation(L2485 - L2505)
- [Ubuntu Autoinstall](#ubuntu-autoinstall): Ubuntu autoinstall validation section(L2506 - L2533)
- [Ubuntu Pro](#ubuntu-pro): Ubuntu Pro attach and service control(L2534 - L2642)
- [Update Etc Hosts](#update-etc-hosts): /etc/hosts management behavior(L2643 - L2691)
- [Update Hostname](#update-hostname): Per-boot hostname update behavior(L2692 - L2757)
- [Users and Groups](#users-and-groups): User/group creation and defaults(L2758 - L2866)
- [Wireguard](#wireguard): WireGuard interfaces and readiness probes(L2867 - L2934)
- [Write Files](#write-files): File write/append/defer options(L2935 - L3045)
- [Yum Add Repo](#yum-add-repo): Yum repository file definitions(L3046 - L3121)
- [Zypper Add Repo](#zypper-add-repo): Zypper repo and zypp.conf settings(L3122 - L3161)

This document serves as the comprehensive reference for all `cloud-config` modules executed by cloud-init. A `cloud-config` document must be valid YAML 1.1 and the first line must be exactly `#cloud-config`.

Modules are processed in a specific order defined in `/etc/cloud/cloud.cfg` across different boot stages (`init`, `config`, `final`).

> Keys can be documented as `deprecated`, `new`, or `changed`. This allows cloud-init to evolve as requirements change, and to adopt better practices without maintaining design decisions indefinitely.
> Keys marked as `deprecated` or `changed` may be removed or changed 5 years from the deprecation date. For example, if a key is deprecated in version `22.1` (the first release in 2022) it is scheduled to be removed in `27.1` (first release in 2027). Use of deprecated keys may cause warnings in the logs. If a key’s expected value changes, the key will be marked changed with a date. A 5 year timeline also applies to changed keys.

## Ansible

This module provides Ansible integration for augmenting cloud-init’s configuration of the local node. This module installs `ansible` during boot and then uses `ansible-pull` to run the playbook repository at the remote URL.

**Internal name:** `cc_ansible`

**Module frequency:** once-per-instance

**Supported distros:** all

**Activate only on keys:** `ansible`

### Config Schema

- **ansible:** (object) Each object in **ansible** list supports the following keys:
  - **install_method:** (`distro`/`pip`) The type of installation for ansible. It can be one of the following values:
    - `distro`
    - `pip`
  - **run_user:** (string) User to run module commands as. If install_method: pip, the pip install runs as this user as well.
  - **ansible_config:** (string) Sets the ANSIBLE_CONFIG environment variable. If set, overrides default config.
  - **setup_controller:** (object) Each object in **setup_controller** list supports the following keys:
    - **repositories:** (array of object) Each object in **repositories** list supports the following keys:
      - **path:** (string)
      - **source:** (string)
    - **run_ansible:** (array of object) Each object in **run_ansible** list supports the following keys:
      - **playbook_name:** (string)
      - **playbook_dir:** (string)
      - **become_password_file:** (string)
      - **connection_password_file:** (string)
      - **list_hosts:** (boolean)
      - **syntax_check:** (boolean)
      - **timeout:** (number)
      - **vault_id:** (string)
      - **vault_password_file:** (string)
      - **background:** (number)
      - **check:** (boolean)
      - **diff:** (boolean)
      - **module_path:** (string)
      - **poll:** (number)
      - **args:** (string)
      - **extra_vars:** (string)
      - **forks:** (number)
      - **inventory:** (string)
      - **scp_extra_args:** (string)
      - **sftp_extra_args:** (string)
      - **private_key:** (string)
      - **connection:** (string)
      - **module_name:** (string)
      - **sleep:** (string)
      - **tags:** (string)
      - **skip_tags:** (string)
  - **galaxy:** (object) Each object in **galaxy** list supports the following keys:
    - **actions:** (array of array of string)
  - **package_name:** (string)
  - **pull:** (array of object/object) pull playbooks from a VCS repo and run them on the host. Each object in **pull** list supports the following keys:
    *Deprecated in version 25.2: Expect ansible.pull as list of objects instead of a single object.*
    - **accept_host_key:** (boolean)
    - **clean:** (boolean)
    - **full:** (boolean)
    - **diff:** (boolean)
    - **ssh_common_args:** (string)
    - **scp_extra_args:** (string)
    - **sftp_extra_args:** (string)
    - **private_key:** (string)
    - **checkout:** (string)
    - **module_path:** (string)
    - **timeout:** (string)
    - **url:** (string)
    - **connection:** (string)
    - **vault_id:** (string)
    - **vault_password_file:** (string)
    - **verify_commit:** (boolean)
    - **inventory:** (string)
    - **module_name:** (string)
    - **sleep:** (string)
    - **tags:** (string)
    - **skip_tags:** (string)
    - **playbook_name:** (string) Single playbook_name to run with ansible-pull. *Deprecated in version 25.2: Use playbook_names key instead.*
    - **playbook_names:** (array of string) List of playbook_names to run with ansible-pull

### Examples

Example 1:

```yaml
#cloud-config
ansible:
  package_name: ansible-core
  install_method: distro
  pull:
    - url: [https://github.com/<REDACTED_GITHUB_USER>/vmboot.git](https://github.com/<REDACTED_GITHUB_USER>/vmboot.git)
      playbook_names: [ubuntu.yml]
```

Example 2: Multiple ansible-pull URLs can be provided by providing a list of pull objects. Additionally, multiple playbooks can be provided as a space-separated playbook_name value.

```yaml
#cloud-config
ansible:
  package_name: ansible-core
  install_method: pip
  pull:
    - url: [https://github.com/<REDACTED_GITHUB_USER>/vmboot.git](https://github.com/<REDACTED_GITHUB_USER>/vmboot.git)
      playbook_names: [ubuntu.yml, watermark.yml]
```

## APK Configure

This module handles configuration of the Alpine Package Keeper (APK) `/etc/apk/repositories` file.

**Note:** To ensure that APK configuration is valid YAML, any strings containing special characters, especially colons, should be quoted (“:”).

- **Internal name:** `cc_apk_configure`
- **Module frequency:** once-per-instance
- **Supported distros:** alpine
- **Activate only on keys:** `apk_repos`

### Config Schema

- **apk_repos:** (object) Each object in **apk_repos** list supports the following keys:
  - **preserve_repositories:** (boolean) By default, cloud-init will generate a new repositories file `/etc/apk/repositories` based on any valid configuration settings specified within a apk_repos section of cloud config. To disable this behavior and preserve the repositories file from the pristine image, set **preserve_repositories** to `true`. The **preserve_repositories** option overrides all other config keys that would alter `/etc/apk/repositories`.
  - **alpine_repo:** (object/null) Each object in **alpine_repo** list supports the following keys:
    - **base_url:** (string) The base URL of an Alpine repository, or mirror, to download official packages from. If not specified then it defaults to `https://alpine.global.ssl.fastly.net/alpine`.
    - **community_enabled:** (boolean) Whether to add the Community repo to the repositories file. By default the Community repo is not included.
    - **testing_enabled:** (boolean) Whether to add the Testing repo to the repositories file. By default the Testing repo is not included. It is only recommended to use the Testing repo on a machine running the `Edge` version of Alpine as packages installed from Testing may have dependencies that conflict with those in non-Edge Main or Community repos.
    - **version:** (string) The Alpine version to use (e.g. `v3.12` or `edge`).
  - **local_repo_base_url:** (string) The base URL of an Alpine repository containing unofficial packages.

### Examples

Example 1: Keep the existing `/etc/apk/repositories` file unaltered.

```yaml
#cloud-config
apk_repos:
  preserve_repositories: true
```

Example 2: Create repositories file for Alpine v3.12 main and community using default mirror site.

```yaml
#cloud-config
apk_repos:
  alpine_repo:
    community_enabled: true
    version: 'v3.12'
```

Example 3: Create repositories file for Alpine Edge main, community, and testing using a specified mirror site and also a local repo.

```yaml
#cloud-config
apk_repos:
  alpine_repo:
    base_url: https://some-alpine-mirror/alpine
    community_enabled: true
    testing_enabled: true
    version: edge
  local_repo_base_url: https://my-local-server/local-alpine
```

## Apt Configure

This module handles configuration of advanced package tool (APT) options and adding source lists. There are configuration options such as `apt_get_wrapper` and `apt_get_command` that control how cloud-init invokes `apt-get`. These configuration options are handled on a per-distro basis, so consult documentation for cloud-init’s distro support for instructions on using these config options.

By default, cloud-init will generate default APT sources information in `deb822` format at `/etc/apt/sources.list.d/<distro>.sources`. When the value of `sources_list` does not appear to be `deb822` format, or stable distribution releases disable `deb822` format, `/etc/apt/sources.list` will be written instead.

**Note:** To ensure that APT configuration is valid YAML, any strings containing special characters, especially colons, should be quoted (":").

**Internal name:** `cc_apt_configure`
**Module frequency:** once-per-instance
**Supported distros:** ubuntu, debian, raspberry-pi-os

### Config Schema

- **apt:** (object) Each object in apt list supports the following keys:
  - **preserve_sources_list:** (boolean) By default, cloud-init will generate a new sources list in `/etc/apt/sources.list.d` based on any changes specified in cloud config. To disable this behavior and preserve the sources list from the pristine image, set **preserve_sources_list** to `true`.
  - **disable_suites:** (array of string) Entries in the sources list can be disabled using **disable_suites**, which takes a list of suites to be disabled.
    - `updates` => `$RELEASE-updates`
    - `backports` => `$RELEASE-backports`
    - `security` => `$RELEASE-security`
    - `proposed` => `$RELEASE-proposed`
    - `release` => `$RELEASE`
  - **primary:** (array of object) The primary archive mirrors. Each object supports:
    - **arches:** (array of string)
    - **uri:** (string)
    - **search:** (array of string)
    - **search_dns:** (boolean)
    - **keyid:** (string)
    - **key:** (string)
    - **keyserver:** (string)
  - **security:** (array of object) The security archive mirrors. Same keys as **primary**.
  - **add_apt_repo_match:** (string) Regex to match source entries for `add-apt-repository`. Defaults to `^[\w-]+:\w`.
  - **debconf_selections:** (object) Debconf configurations passed to `debconf-set-selections`.
    - **^.+$:** (string) The debconf configuration string in format: `pkgname question type answer`.
  - **sources_list:** (string) Custom template for rendering `sources.list`. Supports variables like `$MIRROR`, `$RELEASE`, `$PRIMARY`, `$SECURITY`, and `$KEY_FILE`.
  - **conf:** (string) Custom APT configuration (e.g., proxy settings).
  - **https_proxy:** (string) HTTPS APT proxy URL.
  - **http_proxy:** (string) HTTP APT proxy URL.
  - **proxy:** (string) Alias for http APT proxy.
  - **ftp_proxy:** (string) FTP APT proxy URL.
  - **sources:** (object) Dictionary of additional source files.
    - **^.+$:** (object) Source file definition.
      - **source:** (string) A sources.list entry.
      - **keyid:** (string) Key shortid or fingerprint.
      - **key:** (string) Raw PGP key.
      - **keyserver:** (string) Alternate keyserver.
      - **filename:** (string) Specific name for the list file.
      - **append:** (boolean) If true, append to the file; otherwise, overwrite.

### Examples

Example 1:

```yaml
#cloud-config
apt:
  preserve_sources_list: false
  disable_suites:
    - $RELEASE-updates
    - backports
    - $RELEASE
    - mysuite
  primary:
    - arches:
        - amd64
        - i386
        - default
      uri: [http://us.archive.ubuntu.com/ubuntu](http://us.archive.ubuntu.com/ubuntu)
      search:
        - [http://cool.but-sometimes-unreachable.com/ubuntu](http://cool.but-sometimes-unreachable.com/ubuntu)
        - [http://us.archive.ubuntu.com/ubuntu](http://us.archive.ubuntu.com/ubuntu)
      search_dns: false
    - arches:
        - s390x
        - arm64
      uri: [http://archive-to-use-for-arm64.example.com/ubuntu](http://archive-to-use-for-arm64.example.com/ubuntu)

  security:
    - arches:
        - default
      search_dns: true
  sources_list: |
      deb $MIRROR $RELEASE main restricted
      deb-src $MIRROR $RELEASE main restricted
      deb $PRIMARY $RELEASE universe restricted
      deb $SECURITY $RELEASE-security multiverse
  debconf_selections:
      set1: the-package the-package/some-flag boolean true
  conf: |
      APT {
          Get {
              Assume-Yes 'true';
              Fix-Broken 'true';
          }
      }
  proxy: http://[[user][:pass]@]host[:port]/
  http_proxy: http://[[user][:pass]@]host[:port]/
  ftp_proxy: ftp://[[user][:pass]@]host[:port]/
  https_proxy: https://[[user][:pass]@]host[:port]/
  sources:
      source1:
          keyid: keyid
          keyserver: keyserverurl
          source: deb [signed-by=$KEY_FILE] http://<url>/ bionic main
      source2:
          source: ppa:<ppa-name>
      source3:
          source: deb $MIRROR $RELEASE multiverse
          key: |
              ------BEGIN PGP PUBLIC KEY BLOCK-------
              <key data>
              ------END PGP PUBLIC KEY BLOCK-------
      source4:
          source: deb $MIRROR $RELEASE multiverse
          append: false
          key: |
              ------BEGIN PGP PUBLIC KEY BLOCK-------
              <key data>
              ------END PGP PUBLIC KEY BLOCK-------
```

Example 2: Cloud-init version 23.4 will generate a `deb822`-formatted `sources` file at `/etc/apt/sources.list.d/<distro>.sources` instead of `/etc/apt/sources.list` when `sources_list` content is in `deb822` format.

```yaml
#cloud-config
apt:
    sources_list: |
      Types: deb
      URIs: [http://archive.ubuntu.com/ubuntu/](http://archive.ubuntu.com/ubuntu/)
      Suites: $RELEASE
      Components: main
```

## Apt Pipelining

This module configures APT’s `Acquire::http::Pipeline-Depth` option, which controls how APT handles HTTP pipelining. It may be useful for pipelining to be disabled, because some web servers (such as S3) do not pipeline properly (LP: #948461).

Value configuration options for this module are:

- `os`: (Default) use distro default
- `false`: Disable pipelining altogether
- `<number>`: Manually specify pipeline depth. This is not recommended.

**Internal name:** `cc_apt_pipelining`
**Module frequency:** once-per-instance
**Supported distros:** ubuntu, debian, raspberry-pi-os
**Activate only on keys:** `apt_pipelining`

### Config Schema

- **apt_pipelining**: (integer/boolean/string)

### Examples

Example 1:

```yaml
#cloud-config
apt_pipelining: false
```

Example 2:

```yaml
#cloud-config
apt_pipelining: os
```

Example 3:

```yaml
#cloud-config
apt_pipelining: 3
```

## Bootcmd

This module runs arbitrary commands very early in the boot process, only slightly after a boothook would run. This is very similar to a boothook, but more user friendly. Commands can be specified either as lists or strings. For invocation details, see `runcmd`.

> **Note:** `bootcmd` should only be used for things that could not be done later in the boot process.
>
> **Note:** When writing files, do not use `/tmp` dir as it races with `systemd-tmpfiles-clean` (LP: #1707222). Use `/run/somedir` instead.
>
> **Warning:** Use of `INSTANCE_ID` variable within this module is deprecated. Use jinja templates with `v1.instance_id` instead.

- **Internal name:** `cc_bootcmd`
- **Module frequency:** always
- **Supported distros:** all
- **Activate only on keys:** `bootcmd`

### Config Schema

- **bootcmd:** (array of array of string/string)

### Examples

```yaml
#cloud-config
bootcmd:
- echo 192.0.2.10 us.archive.ubuntu.com > /etc/hosts
- [cloud-init-per, once, mymkfs, mkfs, /dev/vdb]
```

## Byobu

Enable/disable Byobu system-wide and for the default user. This module controls whether Byobu is enabled or disabled system-wide and for the default system user. If Byobu is to be enabled, this module will ensure it is installed. Likewise, if Byobu is to be disabled, it will be removed (if installed).

**Internal name:** `cc_byobu`
**Module frequency:** once-per-instance
**Supported distros:** ubuntu, debian, raspberry-pi-os

### Config Schema

- **byobu_by_default**: (`enable-system` / `enable-user` / `disable-system` / `disable-user` / `enable` / `disable` / `user` / `system`)
  - `enable-system`: enable Byobu system-wide
  - `enable-user`: enable Byobu for the default user
  - `disable-system`: disable Byobu system-wide
  - `disable-user`: disable Byobu for the default user
  - `enable`: enable Byobu both system-wide and for the default user
  - `disable`: disable Byobu for all users
  - `user`: alias for `enable-user`
  - `system`: alias for `enable-system`

### Examples

Example 1:

```yaml
#cloud-config
byobu_by_default: enable-user
```

Example 2:

```yaml
#cloud-config
byobu_by_default: disable-system
```

## CA Certificates

This module adds CA certificates to the system’s CA store and updates any related files using the appropriate OS-specific utility. The default CA certificates can be disabled/deleted from use by the system with the configuration option `remove_defaults`.

**Notes:**
    - Certificates must be specified using valid YAML. To specify a multi-line certificate, the YAML multi-line list syntax must be used.
    - Alpine Linux requires the `ca-certificates` package to be installed in order to provide the `update-ca-certificates` command.

**Internal name:** `cc_ca_certs`
**Module frequency:** once-per-instance
**Supported distros:** almalinux, aosc, centos, cloudlinux, alpine, debian, fedora, raspberry-pi-os, rhel, rocky, opensuse, opensuse-microos, opensuse-tumbleweed, opensuse-leap, sle_hpc, sle-micro, sles, ubuntu, photon

### Config Schema

- **ca_certs:** (object) Each object in **ca_certs** list supports the following keys:
  - **remove-defaults:** (boolean) *Deprecated in version 22.3:* Use **remove_defaults** instead.
  - **remove_defaults:** (boolean) Remove default CA certificates if true. Default: `false`.
  - **trusted:** (array of string) List of trusted CA certificates to add.
- **ca-certs:** (object) Each object in **ca-certs** list supports the following keys:
  *Deprecated in version 22.3:* Use **ca_certs** instead.
  - **remove-defaults:** (boolean) *Deprecated in version 22.3:* Use **remove_defaults** instead.
  - **remove_defaults:** (boolean) Remove default CA certificates if true. Default: `false`.
  - **trusted:** (array of string) List of trusted CA certificates to add.

### Examples

Example 1:

```yaml
#cloud-config
ca_certs:
  remove_defaults: true
  trusted:
  - single_line_cert
  - |
    -----BEGIN CERTIFICATE-----
    YOUR-ORGS-TRUSTED-CA-CERT-HERE
    -----END CERTIFICATE-----
```

## Chef

Module that installs, configures, and starts Chef.

This module enables Chef to be installed (from packages, gems, or from omnibus). Before this occurs, Chef configuration is written to disk (`validation.pem`, `client.pem`, `firstboot.json`, `client.rb`), and required directories are created (`/etc/chef` and `/var/log/chef` and so on).

If configured, Chef will be installed and started in either daemon or non-daemon mode. If run in non-daemon mode, post-run actions are executed to do finishing activities such as removing `validation.pem`.

**Internal name:** `cc_chef`
**Module frequency:** always
**Supported distros:** all
**Activate only on keys:** `chef`

### Config Schema

- **chef:** (object) Each object in **chef** list supports the following keys:
  - **directories:** (array of string) Create the necessary directories for chef to run. By default, it creates the following directories:
    - `/etc/chef`
    - `/var/log/chef`
    - `/var/lib/chef`
    - `/var/chef/backup`
    - `/var/chef/cache`
    - `/var/run/chef`
  - **config_path:** (string) Optional path for Chef configuration file. Default: `/etc/chef/client.rb`
  - **validation_cert:** (string) Optional string to be written to file validation_key. Special value `system` means set use existing file.
  - **validation_key:** (string) Optional path for validation_cert. Default: `/etc/chef/validation.pem`.
  - **firstboot_path:** (string) Path to write run_list and initial_attributes keys that should also be present in this configuration. Default: `/etc/chef/firstboot.json`.
  - **exec:** (boolean) Set true if we should run or not run chef (defaults to false, unless a gem installed is requested where this will then default to true).
  - **client_key:** (string) Optional path for client_cert. Default: `/etc/chef/client.pem`.
  - **encrypted_data_bag_secret:** (string) Specifies the location of the secret key used by chef to encrypt data items. By default, this path is set to null, meaning that chef will have to look at the path `/etc/chef/encrypted_data_bag_secret` for it.
  - **environment:** (string) Specifies which environment chef will use. By default, it will use the `_default` configuration.
  - **file_backup_path:** (string) Specifies the location in which backup files are stored. By default, it uses the `/var/chef/backup` location.
  - **file_cache_path:** (string) Specifies the location in which chef cache files will be saved. By default, it uses the `/var/chef/cache` location.
  - **json_attribs:** (string) Specifies the location in which some chef json data is stored. By default, it uses the `/etc/chef/firstboot.json` location.
  - **log_level:** (string) Defines the level of logging to be stored in the log file. By default this value is set to `:info`.
  - **log_location:** (string) Specifies the location of the chef log file. By default, the location is specified at `/var/log/chef/client.log`.
  - **node_name:** (string) The name of the node to run. By default, we will use th instance id as the node name.
  - **omnibus_url:** (string) Omnibus URL if chef should be installed through Omnibus. By default, it uses the `https://www.chef.io/chef/install.sh`.
  - **omnibus_url_retries:** (integer) The number of retries that will be attempted to reach the Omnibus URL. Default: `5`.
  - **omnibus_version:** (string) Optional version string to require for omnibus install.
  - **pid_file:** (string) The location in which a process identification number (pid) is saved. By default, it saves in the `/var/run/chef/client.pid` location.
  - **server_url:** (string) The URL for the chef server.
  - **show_time:** (boolean) Show time in chef logs.
  - **ssl_verify_mode:** (string) Set the verify mode for HTTPS requests. Possible values:
    - `:verify_none`: No validation of SSL certificates.
    - `:verify_peer`: Validate all SSL certificates.
    - Default: `:verify_none`.
  - **validation_name:** (string) The name of the chef-validator key that Chef Infra Client uses to access the Chef Infra Server during the initial Chef Infra Client run.
  - **force_install:** (boolean) If set to `true`, forces chef installation, even if it is already installed.
  - **initial_attributes:** (object of string) Specify a list of initial attributes used by the cookbooks.
  - **install_type:** (`packages`/`gems`/`omnibus`) The type of installation for chef.
  - **run_list:** (array of string) A run list for a first boot json.
  - **chef_license:** (`accept`/`accept-silent`/`accept-no-persist`) string that indicates if user accepts or not license related to some of chef products.

### Examples

Example 1:

```yaml
#cloud-config
chef:
  directories: [/etc/chef, /var/log/chef]
  encrypted_data_bag_secret: /etc/chef/encrypted_data_bag_secret
  environment: _default
  initial_attributes:
    apache:
      keepalive: false
      prefork: {maxclients: 100}
  install_type: omnibus
  log_level: :auto
  omnibus_url_retries: 2
  run_list: ['recipe[apache2]', 'role[db]']
  server_url: [https://chef.yourorg.com:4000](https://chef.yourorg.com:4000)
  ssl_verify_mode: :verify_peer
  validation_cert: system
  validation_name: yourorg-validator
```

## Disable EC2 Instance Metadata Service

This module can disable the EC2 datasource by rejecting the route to `169.254.169.254`, the usual route to the datasource. This module is disabled by default.

**Internal name:** `cc_disable_ec2_metadata`
**Module frequency:** always
**Supported distros:** all
**Activate only on keys:** `disable_ec2_metadata`

### Config Schema

- **disable_ec2_metadata:** (boolean) Set true to disable IPv4 routes to EC2 metadata. Default: `false`.

### Examples

**Example 1:**

```yaml
#cloud-config
disable_ec2_metadata: true
```

## Disk Setup

This module configures simple partition tables and filesystems. It allows for the definition of device aliases for convenience (e.g., `swap` or `ephemeral<X>`), disk partitioning using the `disk_setup` directive, and filesystem creation via the `fs_setup` directive. It supports both MBR and GPT partition tables and provides options to control whether existing data should be overwritten.

### Config Schema

- **device_aliases:** (object) A dictionary of `alias: path` mappings.
  - **<alias_name>:** (string) Path to the disk to be aliased by this name.
- **disk_setup:** (object) Configuration for disk partitioning, keyed by device path or alias.
  - **<alias name/path>:** (object) Configuration options for a specific device:
    - **table_type:** (`mbr`/`gpt`) Specifies the partition table type. Default: `mbr`.
    - **layout:** (`remove`/boolean/array) Defines the partition layout. `true` creates a single partition; `false` creates none; `remove` purges existing tables. A list can specify custom sizes (in percentage) and partition types. Default: `false`.
    - **overwrite:** (boolean) If `true`, skips safety checks for existing partition tables or filesystems. Use with caution. Default: `false`.
- **fs_setup:** (array of object) A list of filesystem configurations.
  - **label:** (string) Label for the filesystem.
  - **filesystem:** (string) Filesystem type (e.g., `ext4`, `btrfs`, `swap`).
  - **device:** (string) Path or alias (format `<alias name>.<partition_number>`) where the filesystem will be created.
  - **partition:** (string/integer) Specifies the partition number. Can be `auto` (searches for existing FS), `any` (skips if any FS exists), or `none` (writes directly to the device).
  - **overwrite:** (boolean) If `true`, overwrites any existing filesystem. Default: `false`.
  - **replace_fs:** (string) Ignored unless partition is `auto` or `any`. Default: `false`.
  - **extra_opts:** (array or string) Optional flags for the filesystem creation command.
  - **cmd:** (array or string) Optional custom command to run for filesystem creation, overriding the default.

### Examples

Example 1:

```yaml
#cloud-config
device_aliases: {my_alias: /dev/sdb, swap_disk: /dev/sdc}
disk_setup:
  /dev/sdd: {layout: true, overwrite: true, table_type: mbr}
  my_alias:
    layout: [50, 50]
    overwrite: true
    table_type: gpt
  swap_disk:
    layout:
    - [100, 82]
    overwrite: true
    table_type: gpt
fs_setup:
- {cmd: mkfs -t %(filesystem)s -L %(label)s %(device)s, device: my_alias.1, filesystem: ext4,
  label: fs1}
- {device: my_alias.2, filesystem: ext4, label: fs2}
- {device: swap_disk.1, filesystem: swap, label: swap}
- {device: /dev/sdd1, filesystem: ext4, label: fs3}
mounts:
- [my_alias.1, /mnt1]
- [my_alias.2, /mnt2]
- [swap_disk.1, none, swap, sw, '0', '0']
- [/dev/sdd1, /mnt3]
```

## Fan

This module installs, configures and starts the Ubuntu fan network system. If cloud-init sees a `fan` entry in cloud-config it will:

- Write `config_path` with the contents of the `config` key
- Install the package `ubuntu-fan` if it is not installed
- Ensure the service is started (or restarted if was previously running)

**Internal name:** `cc_fan`
**Module frequency:** once-per-instance
**Supported distros:** ubuntu
**Activate only on keys:** `fan`

### Config Schema

- **fan:** (object) Each object in **fan** list supports the following keys:
  - **config:** (string) The fan configuration to use as a single multi-line string.
  - **config_path:** (string) The path to write the fan configuration to. Default: `/etc/network/fan`.

### Examples

Example 1:

```yaml
#cloud-config
fan:
  config: |
    # fan 240
    10.x.x.x/8 eth0/16 dhcp
    10.x.x.x/8 eth1/16 dhcp off
    # fan 241
    192.0.2.0/24 eth0/24 dhcp
  config_path: /etc/network/fan
```

## Final Message

Output final message when cloud-init has finished. This module configures the final message that cloud-init writes. The message is specified as a Jinja template with the following variables set:

- `version`: cloud-init version
- `timestamp`: time at cloud-init finish
- `datasource`: cloud-init data source
- `uptime`: system uptime

This message is written to the cloud-init log (usually `/var/log/cloud-init.log`) as well as stderr (which usually redirects to `/var/log/cloud-init-output.log`). Upon exit, this module writes the system uptime, timestamp, and cloud-init version to `/var/lib/cloud/instance/boot-finished` independent of any user data specified for this module.

- **Internal name:** `cc_final_message`
- **Module frequency:** always
- **Supported distros:** all

### Config Schema

- **final_message:** (string) The message to display at the end of the run.

### Examples

Example 1:

```yaml
#cloud-config
final_message: |
  cloud-init has finished
  version: $version
  timestamp: $timestamp
  datasource: $datasource
  uptime: $uptime
```

## Growpart

Growpart resizes partitions to fill the available disk space. This is useful for cloud instances with a larger amount of disk space available than the pristine image uses, as it allows the instance to automatically make use of the extra space.

Note that this only works if the partition to be resized is the last one on a disk with classic partitioning scheme (MBR, BSD, GPT). LVM, Btrfs and ZFS have no such restrictions.

**Internal name:** `cc_growpart`
**Module frequency:** always
**Supported distros:** all

### Config Schema

- **growpart**: (object) Each object in **growpart** list supports the following keys:
  - **mode**: (`auto`/`growpart`/`gpart`/`off`/`False`) The utility to use for resizing. Default: `auto`.
    - `auto`: Use any available utility.
    - `growpart`: Use growpart utility.
    - `gpart`: Use BSD gpart utility.
    - `'off'`: Take no action.
  - **devices**: (array of string) The devices to resize. Each entry can either be the path to the device’s mountpoint in the filesystem or a path to the block device in ‘/dev’. Default: `[/]`.
  - **ignore_growroot_disabled**: (boolean) If `true`, ignore the presence of `/etc/growroot-disabled`. If `false` and the file exists, then don’t resize. Default: `false`.

### Examples

Example 1:

```yaml
#cloud-config
growpart:
  devices: [/]
  ignore_growroot_disabled: false
  mode: auto
```

Example 2:

```yaml
#cloud-config
growpart:
  devices: [/, /dev/vdb1]
  ignore_growroot_disabled: true
  mode: growpart
```

## GRUB dpkg

Configure GRUB debconf installation device.

Configure which device is used as the target for GRUB installation. This module can be enabled/disabled using the `enabled` config key in the `grub_dpkg` config dict. This module automatically selects a disk using `grub-probe` if no installation device is specified.

The value placed into the debconf database is in the format expected by the GRUB post-install script expects. Normally, this is a `/dev/disk/by-id/` value, but we do fallback to the plain disk name if a `by-id` name is not present.

If this module is executed inside a container, then the debconf database is seeded with empty values, and `install_devices_empty` is set to `true`.

**Internal name:** `cc_grub_dpkg`
**Module frequency:** once-per-instance
**Supported distros:** ubuntu, debian
**Activate only on keys:** `grub_dpkg`, `grub-dpkg`

### Config Schema

- **grub_dpkg:** (object) Each object in **grub_dpkg** list supports the following keys:
  - **enabled:** (boolean) Whether to configure which device is used as the target for grub installation. Default: `false`.
  - **grub-pc/install_devices:** (string) Device to use as target for grub installation. If unspecified, `grub-probe` of `/boot` will be used to find the device.
  - **grub-pc/install_devices_empty:** (boolean/string) Sets values for **grub-pc/install_devices_empty**. If unspecified, will be set to `true` if **grub-pc/install_devices** is empty, otherwise `false`. *Changed in version 22.3. Use a boolean value instead.*
  - **grub-efi/install_devices:** (string) Partition to use as target for grub installation. If unspecified, `grub-probe` of `/boot/efi` will be used to find the partition.
- **grub-dpkg:** (object) *Deprecated in version 22.2:* Use **grub_dpkg** instead.

### Examples

Example 1:

```yaml
#cloud-config
grub_dpkg:
  enabled: true
  # BIOS mode (install_devices needs disk)
  grub-pc/install_devices: /dev/sda
  grub-pc/install_devices_empty: false
  # EFI mode (install_devices needs partition)
  grub-efi/install_devices: /dev/sda
```

## Install Hotplug

This module will install the udev rules to enable hotplug if supported by the datasource and enabled in the user-data. The udev rules will be installed as `/etc/udev/rules.d/90-cloud-init-hook-hotplug.rules`.

When hotplug is enabled, newly added network devices will be added to the system by cloud-init. After udev detects the event, cloud-init will refresh the instance metadata from the datasource, detect the device in the updated metadata, then apply the updated network configuration.

Udev rules are installed while cloud-init is running, which means that devices which are added during boot might not be configured. To work around this limitation, one can wait until cloud-init has completed before hotplugging devices.

Currently supported datasources: Openstack, EC2, Hetzner

- **Internal name:** `cc_install_hotplug`
- **Module frequency:** once-per-instance
- **Supported distros:** all

### Config Schema

- **updates:** (object) Each object in **updates** list supports the following keys:
  - **network:** (object) Each object in **network** list supports the following keys:
    - **when:** (array of `boot-new-instance`/`boot-legacy`/`boot`/`hotplug`)

### Examples

**Example 1: Enable hotplug of network devices**

```yaml
#cloud-config
updates:
  network:
    when: [hotplug]
```

**Example 2: Enable network hotplug alongside boot event**

```yaml
#cloud-config
updates:
  network:
    when: [boot, hotplug]
```

## Keyboard

Handle keyboard configuration.

**Internal name:** `cc_keyboard`
**Module frequency:** once-per-instance
**Supported distros:** alpine, arch, debian, ubuntu, raspberry-pi-os, almalinux, amazon, azurelinux, centos, cloudlinux, eurolinux, fedora, mariner, miraclelinux, openmandriva, photon, rhel, rocky, virtuozzo, opensuse, opensuse-leap, opensuse-microos, opensuse-tumbleweed, sle_hpc, sle-micro, sles, suse
**Activate only on keys:** `keyboard`

### Config Schema

- **keyboard:** (object) Each object in **keyboard** list supports the following keys:
  - **layout:** (string) Required. Keyboard layout. Corresponds to XKBLAYOUT.
  - **model:** (string) Optional. Keyboard model. Corresponds to XKBMODEL. Default: `pc105`.
  - **variant:** (string) Required for Alpine Linux, optional otherwise. Keyboard variant. Corresponds to XKBVARIANT.
  - **options:** (string) Optional. Keyboard options. Corresponds to XKBOPTIONS.

### Examples

Example 1: Set keyboard layout to “us”

```yaml
#cloud-config
keyboard:
  layout: us
```

Example 2: Set specific keyboard layout, model, variant, options

```yaml
#cloud-config
keyboard:
  layout: de
  model: pc105
  variant: nodeadkeys
  options: compose:rwin
```

Example 3: For Alpine Linux, set specific keyboard layout and variant, as used by `setup-keymap`. Model and options are ignored.

```yaml
#cloud-config
keyboard:
  layout: gb
  variant: gb-extd
```

## Keys to Console

For security reasons it may be desirable not to write SSH host keys and their fingerprints to the console. To avoid either of them being written to the console, the `emit_keys_to_console` config key under the main `ssh` config key can be used.

To avoid the fingerprint of types of SSH host keys being written to console the `ssh_fp_console_blacklist` config key can be used. By default, all types of keys will have their fingerprints written to console.

To avoid host keys of a key type being written to console the `ssh_key_console_blacklist` config key can be used. By default, all supported host keys are written to console.

**Internal name:** `cc_keys_to_console`
**Module frequency:** once-per-instance
**Supported distros:** all

### Config Schema

- **ssh:** (object) Each object in **ssh** list supports the following keys:
  - **emit_keys_to_console:** (boolean) Set false to avoid printing SSH keys to system console. Default: `true`.
- **ssh_key_console_blacklist:** (array of string) Avoid printing matching SSH key types to the system console.
- **ssh_fp_console_blacklist:** (array of string) Avoid printing matching SSH fingerprints to the system console.

### Examples

Example 1: Do not print any SSH keys to system console

```yaml
#cloud-config
ssh:
  emit_keys_to_console: false
```

Example 2: Do not print certain SSH key types to console

```yaml
#cloud-config
ssh_key_console_blacklist: [rsa]
```

Example 3: Do not print specific SSH key fingerprints to console

```yaml
#cloud-config
ssh_fp_console_blacklist:
- E25451E0221B5773DEBFF178ECDACB160995AA89
- FE76292D55E8B28EE6DB2B34B2D8A784F8C0AAB0
```

## Landscape

Install and configure Landscape client. This module installs and configures `landscape-client`. The Landscape client will only be installed if the key `landscape` is present in config.

Landscape client configuration is given under the `client` key under the main `landscape` config key. The config parameters are not interpreted by cloud-init, but rather are converted into a `ConfigObj`-formatted file and written out to the `[client]` section in `/etc/landscape/client.conf`.

- **Internal name:** `cc_landscape`
- **Module frequency:** once-per-instance
- **Supported distros:** ubuntu
- **Activate only on keys:** `landscape`

### Config Schema

- **landscape:** (object) Each object in **landscape** list supports the following keys:
  - **client:** (object) Each object in **client** list supports the following keys:
    - **url:** (string) The Landscape server URL to connect to. Default: `https://landscape.canonical.com/message-system`.
    - **ping_url:** (string) The URL to perform lightweight exchange initiation with. Default: `https://landscape.canonical.com/ping`.
    - **data_path:** (string) The directory to store data files in. Default: `/var/lib/landscape/client/`.
    - **log_level:** (`debug`/`info`/`warning`/`error`/`critical`) The log level for the client. Default: `info`.
    - **computer_title:** (string) The title of this computer.
    - **account_name:** (string) The account this computer belongs to.
    - **registration_key:** (string) The account-wide key used for registering clients.
    - **tags:** (string) Comma separated list of tag names to be sent to the server.
    - **http_proxy:** (string) The URL of the HTTP proxy, if one is needed.
    - **https_proxy:** (string) The URL of the HTTPS proxy, if one is needed.

### Examples

To discover additional supported client keys, run `man landscape-config`.

Example 1:

```yaml
#cloud-config
landscape:
  client:
    url: [https://landscape.canonical.com/message-system](https://landscape.canonical.com/message-system)
    ping_url: [http://landscape.canonical.com/ping](http://landscape.canonical.com/ping)
    data_path: /var/lib/landscape/client
    http_proxy: [http://my.proxy.com/foobar](http://my.proxy.com/foobar)
    https_proxy: [https://my.proxy.com/foobar](https://my.proxy.com/foobar)
    tags: server,cloud
    computer_title: footitle
    registration_key: <REDACTED_REGISTRATION_KEY>
    account_name: fooaccount
```

Example 2: Minimum viable config requires `account_name` and `computer_title`.

```yaml
#cloud-config
landscape:
  client:
    computer_title: kiosk 1
    account_name: <REDACTED_ACCOUNT_NAME>
```

Example 3: To install `landscape-client` from a PPA, specify `apt.sources`.

```yaml
#cloud-config
apt:
  sources:
    trunk-testing-ppa:
      source: ppa:landscape/self-hosted-beta
landscape:
  client:
    account_name: myaccount
    computer_title: himom
```

## Locale

Configure the system locale and apply it system-wide. By default, use the locale specified by the datasource.

**Internal name:** `cc_locale`
**Module frequency:** once-per-instance
**Supported distros:** all

### Config Schema

- **locale:** (boolean/string) The locale to set as the system’s locale (e.g. ar_PS).
- **locale_configfile:** (string) The file in which to write the locale configuration (defaults to the distro’s default location).

### Examples

Example 1: Set the locale to `"ar_AE"`

```yaml
#cloud-config
locale: ar_AE
```

Example 2: Set the locale to `"fr_CA"` in `/etc/alternate_path/locale`

```yaml
#cloud-config
locale: fr_CA
locale_configfile: /etc/alternate_path/locale
```

Example 3: Skip performing any locale setup or generation

```yaml
#cloud-config
locale: false
```

## LXD

This module configures LXD with user-specified options using `lxd init`.

- If `lxd` is not present on the system but LXD configuration is provided, then `lxd` will be installed.
- If the selected storage backend userspace utility is not installed, it will be installed.
- If network bridge configuration is provided, then `lxd-bridge` will be configured accordingly.

**Internal name:** `cc_lxd`

**Module frequency:** once-per-instance

**Supported distros:** ubuntu

**Activate only on keys:** `lxd`

### Config Schema

- **lxd:** (object) Each object in **lxd** list supports the following keys:
  - **init:** (object) LXD init configuration values to provide to `lxd init –auto` command. Can not be combined with **lxd.preseed**. Each object in **init** list supports the following keys:
    - **network_address:** (string) IP address for LXD to listen on.
    - **network_port:** (integer) Network port to bind LXD to.
    - **storage_backend:** (`zfs`/`dir`/`lvm`/`btrfs`) Storage backend to use. Default: `dir`.
    - **storage_create_device:** (string) Setup device based storage using DEVICE.
    - **storage_create_loop:** (integer) Setup loop based storage with SIZE in GB.
    - **storage_pool:** (string) Name of storage pool to use or create.
    - **trust_password:** (string) The password required to add new clients.
  - **bridge:** (object) LXD bridge configuration provided to setup the host lxd bridge. Can not be combined with **lxd.preseed**. Each object in **bridge** list supports the following keys:
    - **mode:** (`none`/`existing`/`new`) Whether to setup LXD bridge, use an existing bridge by **name** or create a new bridge. `none` will avoid bridge setup, `existing` will configure lxd to use the bring matching **name** and `new` will create a new bridge.
    - **name:** (string) Name of the LXD network bridge to attach or create. Default: `lxdbr0`.
    - **mtu:** (integer) Bridge MTU, defaults to LXD’s default value.
    - **ipv4_address:** (string) IPv4 address for the bridge. If set, **ipv4_netmask** key required.
    - **ipv4_netmask:** (integer) Prefix length for the **ipv4_address** key. Required when **ipv4_address** is set.
    - **ipv4_dhcp_first:** (string) First IPv4 address of the DHCP range for the network created. This value will combined with **ipv4_dhcp_last** key to set LXC **ipv4.dhcp.ranges**.
    - **ipv4_dhcp_last:** (string) Last IPv4 address of the DHCP range for the network created. This value will combined with **ipv4_dhcp_first** key to set LXC **ipv4.dhcp.ranges**.
    - **ipv4_dhcp_leases:** (integer) Number of DHCP leases to allocate within the range. Automatically calculated based on `ipv4_dhcp_first` and `ipv4_dhcp_last` when unset.
    - **ipv4_nat:** (boolean) Set `true` to NAT the IPv4 traffic allowing for a routed IPv4 network. Default: `false`.
    - **ipv6_address:** (string) IPv6 address for the bridge (CIDR notation). When set, **ipv6_netmask** key is required. When absent, no IPv6 will be configured.
    - **ipv6_netmask:** (integer) Prefix length for **ipv6_address** provided. Required when **ipv6_address** is set.
    - **ipv6_nat:** (boolean) Whether to NAT. Default: `false`.
    - **domain:** (string) Domain to advertise to DHCP clients and use for DNS resolution.
  - **preseed:** (string) Opaque LXD preseed YAML config passed via stdin to the command: `lxd init –preseed`. See: [LXD non-interactive configuration](https://documentation.ubuntu.com/lxd/en/latest/howto/initialize/#non-interactive-configuration) or `lxd init –dump` for viable config. Can not be combined with either **lxd.init** or **lxd.bridge**.

### Examples

Example 1: Simplest working directory-backed LXD configuration.

```yaml
#cloud-config
lxd:
  init:
    storage_backend: dir
```

Example 2: `lxd-init` showcasing cloud-init’s LXD config options.

```yaml
#cloud-config
lxd:
  init:
    network_address: 0.0.0.0
    network_port: 8443
    storage_backend: zfs
    storage_pool: datapool
    storage_create_loop: 10
  bridge:
    mode: new
    mtu: 1500
    name: lxdbr0
    ipv4_address: 192.0.2.10
    ipv4_netmask: 24
    ipv4_dhcp_first: 192.0.2.20
    ipv4_dhcp_last: 192.0.2.30
    ipv4_dhcp_leases: 250
    ipv4_nat: true
    ipv6_address: 2001:db8::1
    ipv6_netmask: 64
    ipv6_nat: true
    domain: lxd
```

Example 3: For more complex non-interactive LXD configuration of networks, storage pools, profiles, projects, clusters and core config, `lxd:preseed` config will be passed as stdin to the command: `lxd init --preseed`.

See the [LXD non-interactive configuration](https://documentation.ubuntu.com/lxd/en/latest/howto/initialize/#non-interactive-configuration) or run `lxd init --dump` to see viable preseed YAML allowed.

Preseed settings configuring the LXD daemon for HTTPS connections on 192.0.2.10 port 9999, a nested profile which allows for LXD nesting on containers and a limited project allowing for RBAC approach when defining behavior for sub-projects.

```yaml
#cloud-config
lxd:
  preseed: |
    config:
      core.https_address: 192.0.2.10:9999
    networks:
      - config:
          ipv4.address: 192.0.2.1/24
          ipv4.nat: true
          ipv6.address: 2001:db8:1::1/64
          ipv6.nat: true
        description: ""
        name: lxdbr0
        type: bridge
        project: default
    storage_pools:
      - config:
          size: 5GiB
          source: /var/snap/lxd/common/lxd/disks/default.img
        description: ""
        name: default
        driver: zfs
    profiles:
      - config: {}
        description: Default LXD profile
        devices:
          eth0:
            name: eth0
            network: lxdbr0
            type: nic
          root:
            path: /
            pool: default
            type: disk
        name: default
      - config: {}
        security.nesting: true
        devices:
          eth0:
            name: eth0
            network: lxdbr0
            type: nic
          root:
            path: /
            pool: default
            type: disk
        name: nested
    projects:
      - config:
          features.images: true
          features.networks: true
          features.profiles: true
          features.storage.volumes: true
        description: Default LXD project
        name: default
      - config:
          features.images: false
          features.networks: true
          features.profiles: false
          features.storage.volumes: false
        description: Limited Access LXD project
        name: limited
```

## MCollective

This module installs, configures and starts MCollective. If the `mcollective` key is present in config, then MCollective will be installed and started.

Configuration for `mcollective` can be specified in the `conf` key under `mcollective`. Each config value consists of a key-value pair and will be written to `/etc/mcollective/server.cfg`. The `public-cert` and `private-cert` keys, if present in conf may be used to specify the public and private certificates for MCollective. Their values will be written to `/etc/mcollective/ssl/server-public.pem` and `/etc/mcollective/ssl/server-private.pem`.

> **Warning**
> The EC2 metadata service is a network service and thus is readable by non-root users on the system (i.e., `ec2metadata --user-data`). If security is a concern, use `include-once` and SSL URLS.

**Internal name:** `cc_mcollective`

**Module frequency:** once-per-instance

**Supported distros:** all

**Activate only on keys:** `mcollective`

### Config Schema

- **mcollective:** (object) Each object in **mcollective** list supports the following keys:
  - **conf:** (object) Each object in **conf** list supports the following keys:
    - **^.+$:** (boolean/integer/string) Optional config key: value pairs which will be appended to `/etc/mcollective/server.cfg`.
    - **public-cert:** (string) Optional value of server public certificate which will be written to `/etc/mcollective/ssl/server-public.pem`.
    - **private-cert:** (string) Optional value of server private certificate which will be written to `/etc/mcollective/ssl/server-private.pem`.

### Examples

Example 1: Provide server private and public key, and provide the `loglevel: debug` and `plugin.stomp.host: dbhost` config settings in `/etc/mcollective/server.cfg:`

```yaml
#cloud-config
mcollective:
  conf:
    loglevel: debug
    plugin.stomp.host: server.example.com
    public-cert: |
      -------BEGIN CERTIFICATE--------
      <cert data>
      -------END CERTIFICATE--------
    private-cert: |
      -------BEGIN CERTIFICATE--------
      <cert data>
      -------END CERTIFICATE--------
```

## Mounts

This module configures mount points and swap files by adding or removing entries from `/etc/fstab`. It allows for the specification of devices, mount points, file system types, and options. If a device name starts with `xvd`, `sd`, `hd`, or `vd`, the `/dev` prefix can be omitted. Cloud-init automatically attempts to mount ephemeral storage and swap if available and not already configured.

Additionally, this module supports the creation of swap files with configurable filenames, sizes (including `auto`), and maximum sizes.

**Note:** When mounting nested directories (e.g., `/abc` and `/abc/def`), ensure the parent is mounted or use the `X-mount.mkdir` option in systems using `util-linux` to ensure sub-directories are created correctly.

- **Internal name:** `cc_mounts`
- **Module frequency:** once-per-instance
- **Supported distros:** all

### Config Schema

- **mounts:** (array of array of string) List of lists. Each inner list entry is a list of `/etc/fstab` mount declarations of the format: `[ fs_spec, fs_file, fs_vfstype, fs_mntops, fs_freq, fs_passno ]`. A mount declaration with less than 6 items will get remaining values from **mount_default_fields**. A mount declaration with only `fs_spec` and no `fs_file` mountpoint will be skipped.
- **mount_default_fields:** (array of string/null) Default mount configuration for any mount entry with less than 6 options provided. When specified, 6 items are required and represent `/etc/fstab` entries. Default: `defaults,nofail,x-systemd.after=cloud-init-network.service,_netdev`.
- **swap:** (object) Each object in **swap** list supports the following keys:
  - **filename:** (string) Path to the swap file to create.
  - **size:** (`auto`/integer/string) The size in bytes of the swap file, ‘auto’ or a human-readable size abbreviation (B, K, M, G, T). *Warning: For cloud-init versions prior to 23.1, assume 1KB == 1024B.*
  - **maxsize:** (integer/string) The maxsize in bytes of the swap file.

### Examples

Example 1: Mount `ephemeral0` with `noexec` flag, `/dev/sdc` with `mount_default_fields`, and `/dev/xvdh` with custom `fs_passno "0"`. Also provide an automatically-sized swap with a max size of 10485760 bytes.

```yaml
#cloud-config
mounts:
- [ /dev/ephemeral0, /mnt, auto, "defaults,noexec" ]
- [ sdc, /opt/data ]
- [ xvdh, /opt/data, auto, "defaults,nofail", "0", "0" ]
mount_default_fields: [None, None, auto, "defaults,nofail", "0", "2"]
swap:
  filename: /my/swapfile
  size: auto
  maxsize: 10485760
```

Example 2: Create a 2 GB swap file at `/swapfile` using human-readable values.

```yaml
#cloud-config
swap:
  filename: /swapfile
  size: 2G
  maxsize: 2G
```

## NTP

Handle Network Time Protocol (NTP) configuration. If `ntp` is not installed on the system and NTP configuration is specified, `ntp` will be installed.

If there is a default NTP config file in the image or one is present in the distro’s `ntp` package, it will be copied to a file with `.dist` appended to the filename before any changes are made.

A list of NTP pools and NTP servers can be provided under the `ntp` config key.

If no NTP `servers` or `pools` are provided, 4 pools will be used in the format: `{0-3}.{distro}.pool.ntp.org`

**Internal name:** `cc_ntp`

**Module frequency:** once-per-instance

**Supported distros:** almalinux, alpine, aosc, azurelinux, centos, cloudlinux, cos, debian, eurolinux, fedora, freebsd, mariner, miraclelinux, openbsd, openeuler, OpenCloudOS, openmandriva, opensuse, opensuse-microos, opensuse-tumbleweed, opensuse-leap, photon, raspberry-pi-os, rhel, rocky, sle_hpc, sle-micro, sles, TencentOS, ubuntu, virtuozzo

**Activate only on keys:** `ntp`

### Config Schema

- **ntp:** (null/object) Each object in **ntp** list supports the following keys:
  - **pools:** (array of string) List of ntp pools. If both pools and servers are empty, 4 default pool servers will be provided of the format `{0-3}.{distro}.pool.ntp.org`. NOTE: for Alpine Linux when using the Busybox NTP client this setting will be ignored due to the limited functionality of Busybox’s ntpd.
  - **servers:** (array of string) List of ntp servers. If both pools and servers are empty, 4 default pool servers will be provided with the format `{0-3}.{distro}.pool.ntp.org`.
  - **peers:** (array of string) List of ntp peers.
  - **allow:** (array of string) List of CIDRs to allow.
  - **ntp_client:** (string) Name of an NTP client to use to configure system NTP. When unprovided or ‘auto’ the default client preferred by the distribution will be used. The following built-in client names can be used to override existing configuration defaults: chrony, ntp, openntpd, ntpdate, systemd-timesyncd.
  - **enabled:** (boolean) Attempt to enable ntp clients if set to True. If set to `false`, ntp client will not be configured or installed.
  - **config:** (object) Configuration settings or overrides for the **ntp_client** specified. Each object in **config** list supports the following keys:
    - **confpath:** (string) The path to where the **ntp_client** configuration is written.
    - **check_exe:** (string) The executable name for the **ntp_client**. For example, ntp service **check_exe** is ‘ntpd’ because it runs the ntpd binary.
    - **packages:** (array of string) List of packages needed to be installed for the selected **ntp_client**.
    - **service_name:** (string) The systemd or sysvinit service name used to start and stop the **ntp_client** service.
    - **template:** (string) Inline template allowing users to customize their **ntp_client** configuration with the use of the Jinja templating engine. The template content should start with `## template:jinja`. Within the template, you can utilize any of the following ntp module config keys: **servers**, **pools**, **allow**, and **peers**. Each cc_ntp schema config key and expected value type is defined above.

### Examples

Example 1: Override NTP with chrony configuration on Ubuntu.

```yaml
#cloud-config
ntp:
  enabled: true
  ntp_client: chrony  # Uses cloud-init default chrony configuration
```

Example 2: Provide a custom NTP client configuration.

```yaml
#cloud-config
ntp:
  enabled: true
  ntp_client: myntpclient
  config:
    confpath: /etc/myntpclient/myntpclient.conf
    check_exe: myntpclientd
    packages:
    - myntpclient
    service_name: myntpclient
    template: |
      ## template:jinja
      # My NTP Client config
      {% if pools -%}# pools{% endif %}
      {% for pool in pools -%}
      pool {{pool}} iburst
      {% endfor %}
      {%- if servers %}# servers
      {% endif %}
      {% for server in servers -%}
      server {{server}} iburst
      {% endfor %}
      {% if peers -%}# peers{% endif %}
      {% for peer in peers -%}
      peer {{peer}}
      {% endfor %}
      {% if allow -%}# allow{% endif %}
      {% for cidr in allow -%}
      allow {{cidr}}
      {% endfor %}
  pools: [0.int.pool.ntp.org, 1.int.pool.ntp.org, ntp.myorg.org]
  servers:
  - server.example.com
  - ntp.ubuntu.com
  - 192.0.2.20
  allow:
  - 192.0.2.0/24
  peers:
  - ntp-peer-1.example.com
  - ntp-peer-2.example.com
```

## Package Update Upgrade Install

This module allows packages to be updated, upgraded, or installed during boot using any available package manager present on a system such as apt, pkg, snap, yum, or zypper. If any packages are to be installed or an upgrade is to be performed, the package cache will be updated first. If a package installation or upgrade requires a reboot, then a reboot can be performed if `package_reboot_if_required` is specified.

**Internal name:** `cc_package_update_upgrade_install`
**Module frequency:** once-per-instance
**Supported distros:** all
**Activate only on keys:** `apt_update`, `package_update`, `apt_upgrade`, `package_upgrade`, `packages`

### Config Schema

- **packages:** (array of object/array of string/string) An array containing either a package specification, or an object consisting of a package manager key having a package specification value. A package specification can be either a package name or a list with two entries, the first being the package name and the second being the specific package version to install. Each object in **packages** list supports the following keys:
  - **apt:** (array of array of string/string)
  - **snap:** (array of array of string/string)
- **package_update:** (boolean) Set `true` to update packages. Happens before upgrade or install. Default: `false`.
- **package_upgrade:** (boolean) Set `true` to upgrade packages. Happens before install. Default: `false`.
- **package_reboot_if_required:** (boolean) Set `true` to reboot the system if required by presence of `/var/run/reboot-required`. Default: `false`.
- **apt_update:** (boolean) *Deprecated in version 22.2:* Use **package_update** instead.
- **apt_upgrade:** (boolean) *Deprecated in version 22.2:* Use **package_upgrade** instead.
- **apt_reboot_if_required:** (boolean) *Deprecated in version 22.2:* Use **package_reboot_if_required** instead.

### Examples

**Example 1:**

```yaml
#cloud-config
package_reboot_if_required: true
package_update: true
package_upgrade: true
packages:
- pwgen
- pastebinit
- [libpython3.8, 3.8.10-0ubuntu1~20.04.2]
- snap:
  - certbot
  - [juju, --edge]
  - [lxd, --channel=5.15/stable]
- apt: [mg]
```

By default, `package_upgrade: true` performs upgrades on any installed package manager. To avoid calling `snap refresh` in images with snap installed, set `snap refresh.hold` to `forever` will prevent cloud-init’s snap interaction during any boot:

```yaml
#cloud-config
package_update: true
package_upgrade: true
snap:
  commands:
    00: snap refresh --hold=forever
package_reboot_if_required: true
```

## Phone Home

This module can be used to post data to a remote host after boot is complete. Either all data can be posted, or a specific list of keys including `pub_key_rsa`, `pub_key_ecdsa`, `pub_key_ed25519`, `instance_id`, `hostname`, and `fqdn`.

Data is sent as `x-www-form-urlencoded` arguments.

> **Warning**: Use of the `INSTANCE_ID` variable within this module is deprecated. Use jinja templates with `v1.instance_id` instead.

- **Internal name:** `cc_phone_home`
- **Module frequency:** once-per-instance
- **Supported distros:** all

### Config Schema

- **phone_home:** (object) Each object in **phone_home** list supports the following keys:
  - **url:** (string) The URL to send the phone home data to.
  - **post:** (`all`/array of keys) A list of keys to post (`pub_key_rsa`, `pub_key_ecdsa`, `pub_key_ed25519`, `instance_id`, `hostname`, `fqdn`) or `all`. Default: `all`.
  - **tries:** (integer) The number of times to try sending the phone home data. Default: `10`.

### Examples

Example 1:

```yaml
## template: jinja
#cloud-config
phone_home: {post: all, url: '[http://example.com/](http://example.com/){{ v1.instance_id }}/'}
```

Example 2:

```yaml
## template: jinja
#cloud-config
phone_home:
  post: [pub_key_rsa, pub_key_ecdsa, pub_key_ed25519, instance_id, hostname, fqdn]
  tries: 5
  url: [http://example.com/](http://example.com/){{ v1.instance_id }}/
```

## Power State Change

This module handles shutdown/reboot after all config modules have been run. By default it will take no action, and the system will keep running unless a package installation/upgrade requires a system reboot (e.g. installing a new kernel) and `package_reboot_if_required` is `true`.

Using this module ensures that cloud-init is entirely finished with modules that would be executed.

**Note for Alpine Linux:** Any message value specified is ignored as Alpine’s `halt`, `poweroff`, and `reboot` commands do not support broadcasting a message.

- **Internal name:** `cc_power_state_change`
- **Module frequency:** once-per-instance
- **Supported distros:** all
- **Activate only on keys:** `power_state`

### Config Schema

- **power_state:** (object) Each object in **power_state** list supports the following keys:
  - **delay:** (integer/string/`now`) Time in minutes to delay after cloud-init has finished. Can be `now` or an integer specifying the number of minutes to delay. Default: `now`. *Changed in version 22.3. Use of type string for this value is deprecated. Use `now` or integer type.*
  - **mode:** (`poweroff`/`reboot`/`halt`) Must be one of `poweroff`, `halt`, or `reboot`.
  - **message:** (string) Optional message to display to the user when the system is powering off or rebooting.
  - **timeout:** (integer) Time in seconds to wait for the cloud-init process to finish before executing shutdown. Default: `30`.
  - **condition:** (string/boolean/array) Apply state change only if condition is met. May be boolean true (always met), false (never met), or a command string or list to be executed. If exit code is 0, condition is met, otherwise not. Default: `true`.

### Examples

Example 1:

```yaml
#cloud-config
power_state:
  delay: now
  mode: poweroff
  message: Powering off
  timeout: 2
  condition: true
```

Example 2:

```yaml
#cloud-config
power_state:
  delay: 30
  mode: reboot
  message: Rebooting machine
  condition: test -f /var/tmp/reboot_me
```

## Puppet

This module handles Puppet installation and configuration. If the `puppet` key does not exist in global configuration, no action will be taken. If a config entry for `puppet` is present, then by default the latest version of Puppet will be installed. If the `puppet` config key exists in the config archive, this module will attempt to start puppet even if no installation was performed.

The module also provides keys for configuring the new Puppet 4 paths and installing the `puppet` package from the puppetlabs repositories. The keys are `package_name`, `conf_file`, `ssl_dir` and `csr_attributes_path`. If unset, their values will default to ones that work with Puppet 3.X, and with distributions that ship modified Puppet 4.X, that use the old paths.

**Internal name:** `cc_puppet`
**Module frequency:** once-per-instance
**Supported distros:** all
**Activate only on keys:** `puppet`

### Config Schema

- **puppet:** (object) Each object in **puppet** list supports the following keys:
  - **install:** (boolean) Whether or not to install puppet. Setting to `false` will result in an error if puppet is not already present on the system. Default: `true`.
  - **version:** (string) Optional version to pass to the installer script or package manager. If unset, the latest version from the repos will be installed.
  - **install_type:** (`packages`/`aio`) Valid values are `packages` and `aio`. Agent packages from the puppetlabs repositories can be installed by setting `aio`. Based on this setting, the default config/SSL/CSR paths will be adjusted accordingly. Default: `packages`.
  - **collection:** (string) Puppet collection to install if **install_type** is `aio`. This can be set to one of `puppet` (rolling release), `puppet6`, `puppet7` (or their nightly counterparts) in order to install specific release streams.
  - **aio_install_url:** (string) If **install_type** is `aio`, change the url of the install script.
  - **cleanup:** (boolean) Whether to remove the puppetlabs repo after installation if **install_type** is `aio` Default: `true`.
  - **conf_file:** (string) The path to the puppet config file. Default depends on **install_type**.
  - **ssl_dir:** (string) The path to the puppet SSL directory. Default depends on **install_type**.
  - **csr_attributes_path:** (string) The path to the puppet csr attributes file. Default depends on **install_type**.
  - **package_name:** (string) Name of the package to install if **install_type** is `packages`. Default: `puppet`.
  - **exec:** (boolean) Whether or not to run puppet after configuration finishes. A single manual run can be triggered by setting **exec** to `true`, and additional arguments can be passed to `puppet agent` via the **exec_args** key (by default the agent will execute with the `--test` flag). Default: `false`.
  - **exec_args:** (array of string) A list of arguments to pass to ‘puppet agent’ if ‘exec’ is true Default: `['--test']`.
  - **start_service:** (boolean) By default, the puppet service will be automatically enabled after installation and set to automatically start on boot. To override this in favor of manual puppet execution set **start_service** to `false`.
  - **conf:** (object) Every key present in the conf object will be added to puppet.conf. Section names should be one of: `main`, `server`, `agent` or `user`. The `certname` key supports string substitutions for `%i` and `%f`. `ca_cert` is a special case holding the puppetserver certificate in pem format.
    - **main:** (object)
    - **server:** (object)
    - **agent:** (object)
    - **user:** (object)
    - **ca_cert:** (string)
  - **csr_attributes:** (object) Create a `csr_attributes.yaml` file for CSR attributes and certificate extension requests.
    - **custom_attributes:** (object)
    - **extension_requests:** (object)

### Examples

Example 1:

```yaml
#cloud-config
puppet:
  install: true
  version: "7.7.0"
  install_type: "aio"
  collection: "puppet7"
  aio_install_url: '[https://git.io/JBhoQ](https://git.io/JBhoQ)'
  cleanup: true
  conf_file: "/etc/puppet/puppet.conf"
  ssl_dir: "/var/lib/puppet/ssl"
  csr_attributes_path: "/etc/puppet/csr_attributes.yaml"
  exec: true
  exec_args: ['--test']
  conf:
    agent:
      server: "puppetserver.example.org"
      certname: "%i.%f"
    ca_cert: |
      <REDACTED_CA_CERTIFICATE>
  csr_attributes:
    custom_attributes:
      1.2.840.113549.1.9.7: <REDACTED_CUSTOM_ATTRIBUTE>
    extension_requests:
      pp_uuid: <REDACTED_UUID>
      pp_image_name: my_ami_image
      pp_preshared_key: <REDACTED_PRESHARED_KEY>
```

Example 2:

```yaml
#cloud-config
puppet:
  install_type: "packages"
  package_name: "puppet"
  exec: false
```

## Raspberry Pi Configuration

Configure Raspberry Pi ARM interfaces and enable Raspberry Pi USB Gadget mode. This module handles ARM interface configuration for Raspberry Pi and USB Gadget setup. The USB Gadget mode will be enabled to auto-start on boot. Make sure you read the documentation on it carefully before enabling it. This only works on Raspberry Pi OS (trixie and later).

**Internal name:** `cc_raspberry_pi`
**Module frequency:** once-per-instance
**Supported distros:** raspberry-pi-os
**Activate only on keys:** `rpi`

### Config Schema

- **rpi:** (object) Each object in **rpi** list supports the following keys:
  - **interfaces:** (object) Each object in **interfaces** list supports the following keys:
    - **spi:** (boolean) Enable SPI interface. Default: `false`.
    - **i2c:** (boolean) Enable I2C interface. Default: `false`.
    - **serial:** (boolean/object) Enable serial console. Default: `false`. Each object in **serial** list supports the following keys:
      - **console:** (boolean) Enable login shell to be accessible over serial. Default: `false`.
      - **hardware:** (boolean) Enable serial port hardware. Default: `false`.
    - **onewire:** (boolean) Enable 1-Wire interface. Default: `false`.
  - **enable_usb_gadget:** (boolean) Enable Raspberry Pi USB Gadget mode. Default: `false`.

### Examples

This example will enable the SPI and I2C interfaces on Raspberry Pi.

```yaml
#cloud-config
rpi:
  interfaces:
    spi: true
    i2c: true
```

This example will enable the serial console (login shell) on Raspberry Pi. On models prior to Pi 5, enabling the console also enables the UART hardware.

```yaml
#cloud-config
rpi:
  interfaces:
    serial: true
```

This example will enable the serial console on Raspberry Pi 5 while disabling the UART hardware (only Pi 5 allows this combination).

```yaml
#cloud-config
rpi:
  interfaces:
    serial:
      # Pi 5 only | disabling hardware while enabling console
      console: true
      hardware: false
```

This example will enable the UART hardware without binding it to the serial console, allowing applications to use the port directly.

```yaml
#cloud-config
rpi:
  interfaces:
    # works on all Pi models
    # only enables the UART hardware without binding it to the console
    serial:
      console: false
      hardware: true
```

This example will enable the Raspberry Pi USB Gadget mode.

```yaml
#cloud-config
rpi:
  enable_usb_gadget: true
```

## Resizefs

Resize a filesystem to use all available space on partition. This module is useful along with `cc_growpart` and will ensure that if the root partition has been resized, the root filesystem will be resized along with it.

By default, `cc_resizefs` will resize the root partition and will block the boot process while the `resize` command is running.

Optionally, the resize operation can be performed in the background while cloud-init continues running modules. This can be enabled by setting `resize_rootfs` to `noblock`.

This module can be disabled altogether by setting `resize_rootfs` to `false`.

**Internal name:** `cc_resizefs`
**Module frequency:** always
**Supported distros:** all

### Config Schema

- **resize_rootfs:** (`True`/`False`/`noblock`) Whether to resize the root partition. `noblock` will resize in the background. Default: `true`.

### Examples

Example 1: Disable root filesystem resize operation.

```yaml
#cloud-config
resize_rootfs: false
```

Example 2: Runs resize operation in the background.

```yaml
#cloud-config
resize_rootfs: noblock
```

## Resolv Conf

Configure `resolv.conf`. You should not use this module unless manually editing `/etc/resolv.conf` is the correct way to manage nameserver information on your operating system. Many distros have moved away from manually editing this file, so verify your distro's preferred method (Network configuration is often preferred). This module is intended for environments where early configuration is necessary for bootstrapping or where configuration management tools own DNS configuration.

For Red Hat with `sysconfig`, set `PEERDNS=no` for all DHCP-enabled NICs.

**Internal name:** `cc_resolv_conf`
**Module frequency:** once-per-instance
**Supported distros:** alpine, azurelinux, fedora, mariner, opensuse, opensuse-leap, opensuse-microos, opensuse-tumbleweed, photon, rhel, sle_hpc, sle-micro, sles, openeuler
**Activate only on keys:** `manage_resolv_conf`

### Config Schema

- **manage_resolv_conf:** (boolean) Whether to manage the resolv.conf file. **resolv_conf** block will be ignored unless this is set to `true`. Default: `false`.
- **resolv_conf:** (object) Each object in **resolv_conf** list supports the following keys:
  - **nameservers:** (array) A list of nameservers to use to be added as `nameserver` lines.
  - **searchdomains:** (array) A list of domains to be added `search` line.
  - **domain:** (string) The domain to be added as `domain` line.
  - **sortlist:** (array) A list of IP addresses to be added to `sortlist` line.
  - **options:** (object) Key/value pairs of options to go under `options` heading. A unary option should be specified as `true`.

### Examples

```yaml
#cloud-config
manage_resolv_conf: true
resolv_conf:
  domain: example.com
  nameservers: [192.0.2.53, 192.0.2.54]
  options: {rotate: true, timeout: 1}
  searchdomains: [foo.example.com, bar.example.com]
  sortlist: [192.0.2.0/24, 192.0.2.10]
```

## Red Hat Subscription

Register a Red Hat system, either by username and password **or** by activation and org.

Following a successful registration, you can:

- auto_attach subscriptions
- set the service level
- add subscriptions based on pool ID
- enable/disable yum repositories based on repo ID
- alter the `rhsm_baseurl` and `server_hostname` in `/etc/rhsm/rhs.conf`.

**Internal name:** `cc_rh_subscription`
**Module frequency:** once-per-instance
**Supported distros:** fedora, rhel
**Activate only on keys:** `rh_subscription`

### Config Schema

- **rh_subscription:** (object) Each object in **rh_subscription** list supports the following keys:
  - **username:** (string) The username to use. Must be used with password. Should not be used with **activation_key** or **org**.
  - **password:** (string) The password to use. Must be used with username. Should not be used with **activation_key** or **org**.
  - **activation_key:** (string) The activation key to use. Must be used with **org**. Should not be used with **username** or **password**.
  - **activation-key:** (string) The activation key to use. Must be used with **org**. Should not be used with **username** or **password**. *Deprecated in version 25.3:* Use **activation_key** instead.
  - **org:** (string/integer) The organization to use. Must be used with **activation_key**. Should not be used with **username** or **password**. *Deprecated in version 24.2:* Use of type integer for this value is deprecated. Use a string instead.
  - **auto_attach:** (boolean) Whether to attach subscriptions automatically.
  - **auto-attach:** (boolean) Whether to attach subscriptions automatically. *Deprecated in version 25.3:* Use **auto_attach** instead.
  - **service_level:** (string) The service level to use when subscribing to RH repositories. `auto_attach` must be true for this to be used.
  - **service-level:** (string) The service level to use when subscribing to RH repositories. `auto_attach` must be true for this to be used. *Deprecated in version 25.3:* Use **service_level** instead.
  - **add_pool:** (array of string) A list of pool IDs add to the subscription.
  - **add-pool:** (array of string) A list of pool IDs add to the subscription. *Deprecated in version 25.3:* Use **add_pool** instead.
  - **enable_repo:** (array of string) A list of repositories to enable.
  - **enable-repo:** (array of string) A list of repositories to enable. *Deprecated in version 25.3:* Use **enable_repo** instead.
  - **disable_repo:** (array of string) A list of repositories to disable.
  - **disable-repo:** (array of string) A list of repositories to disable. *Deprecated in version 25.3:* Use **disable_repo** instead.
  - **release_version:** (string) Sets the release_version via `subscription-manager release –set=<release_version>` then deletes the package manager cache `/var/cache/{dnf,yum}`.
  - **rhsm_baseurl:** (string) Sets the baseurl in `/etc/rhsm/rhsm.conf`.
  - **rhsm-baseurl:** (string) Sets the baseurl in `/etc/rhsm/rhsm.conf`. *Deprecated in version 25.3:* Use **rhsm_baseurl** instead.
  - **server_hostname:** (string) Sets the serverurl in `/etc/rhsm/rhsm.conf`.
  - **server-hostname:** (string) Sets the serverurl in `/etc/rhsm/rhsm.conf`. *Deprecated in version 25.3:* Use **server_hostname** instead.

### Examples

Example 1:

```yaml
#cloud-config
rh_subscription:
  username: <REDACTED_EMAIL>
  ## Quote your password if it has symbols to be safe
  password: '<REDACTED_PASSWORD>'
```

Example 2:

```yaml
#cloud-config
rh_subscription:
  activation_key: <REDACTED_ACTIVATION_KEY>
  org: "ABC"
```

Example 3:

```yaml
#cloud-config
rh_subscription:
  activation_key: <REDACTED_ACTIVATION_KEY>
  org: 12345
  auto_attach: true
  service_level: self-support
  add_pool:
    - 1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a
    - 2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b
  enable_repo:
    - repo-id-to-enable
    - other-repo-id-to-enable
  disable_repo:
    - repo-id-to-disable
    - other-repo-id-to-disable
  # Alter the baseurl in /etc/rhsm/rhsm.conf
  rhsm_baseurl: http://url
  # Alter the server hostname in /etc/rhsm/rhsm.conf
  server_hostname: foo.bar.com
  # Set `subscription-manager release --set=6Server` then
  # delete /var/cache/{dnf,yum}
  release_version: 6Server
```

## Rsyslog

This module configures remote system logging using rsyslog.

Configuration for remote servers can be specified in `configs`, but for convenience it can be specified as key-value pairs in `remotes`.

This module can install rsyslog if not already present on the system using the `install_rsyslog`, `packages`, and `check_exe` options. Installation may not work on systems where this module runs before networking is up.

> **Note:** On BSD, cloud-init will attempt to disable and stop the base system syslogd. This may fail on a first run. We recommend creating images with `service syslogd disable`.

**Internal name:** `cc_rsyslog`
**Module frequency:** once-per-instance
**Supported distros:** all
**Activate only on keys:** `rsyslog`

### Config Schema

- **rsyslog:** (object) Each object in **rsyslog** list supports the following keys:
  - **config_dir:** (string) The directory where rsyslog configuration files will be written. Default: `/etc/rsyslog.d`.
  - **config_filename:** (string) The name of the rsyslog configuration file. Default: `20-cloud-config.conf`.
  - **configs:** (array of string/object) Each entry in **configs** is either a string or an object. Each config entry contains a configuration string and a file to write it to. For config entries that are an object, **filename** sets the target filename and **content** specifies the config string to write. For config entries that are only a string, the string is used as the config string to write. If the filename to write the config to is not specified, the value of the **config_filename** key is used. A file with the selected filename will be written inside the directory specified by **config_dir**. Each object in **configs** list supports the following keys:
    - **filename:** (string)
    - **content:** (string)
  - **remotes:** (object) Each key is the name for an rsyslog remote entry. Each value holds the contents of the remote config for rsyslog. The config consists of the following parts:
    - filter for log messages (defaults to `*.*`)
    - optional leading `@` or `@@`, indicating udp and tcp respectively (defaults to `@`, for udp)
    - ipv4 or ipv6 hostname or address. ipv6 addresses must be in `[::1]` format, (e.g. `@[fd00::1]:514`)
    - optional port number (defaults to `514`)
    - This module will provide sane defaults for any part of the remote entry that is not specified, so in most cases remote hosts can be specified just using `<name>: <address>`.
  - **service_reload_command:** (`auto`/array of string) The command to use to reload the rsyslog service after the config has been updated. If this is set to `auto`, then an appropriate command for the distro will be used. This is the default behavior. To manually set the command, use a list of command args (e.g. `[systemctl, restart, rsyslog]`).
  - **install_rsyslog:** (boolean) Install rsyslog. Default: `false`.
  - **check_exe:** (string) The executable name for the rsyslog daemon. For example, `rsyslogd`, or `/opt/sbin/rsyslogd` if the rsyslog binary is in an unusual path. This is only used if `install_rsyslog` is `true`. Default: `rsyslogd`.
  - **packages:** (array of string) List of packages needed to be installed for rsyslog. This is only used if **install_rsyslog** is `true`. Default: `[rsyslog]`.

### Examples

Example 1:

```yaml
#cloud-config
rsyslog:
  remotes: {juju: 192.0.2.40, maas: 192.0.2.41}
  service_reload_command: auto
```

Example 2:

```yaml
#cloud-config
rsyslog:
  config_dir: /opt/etc/rsyslog.d
  config_filename: 99-late-cloud-config.conf
  configs:
  - '*.* @@192.0.2.50'
  - {content: '*.* @@192.0.2.1:10514', filename: 01-example.conf}
  - {content: '*.* @@syslogd.example.com

      '}
  remotes: {juju: 192.0.2.40, maas: 192.0.2.41}
  service_reload_command: [your, syslog, restart, command]
```

Example 3: Default (no) configuration with package installation on FreeBSD.

```yaml
#cloud-config
rsyslog:
  check_exe: rsyslogd
  config_dir: /usr/local/etc/rsyslog.d
  install_rsyslog: true
  packages: [rsyslogd]
```

## Runcmd

Run arbitrary commands at a `rc.local`-like time-frame with output to the console. Each item can be either a list or a string. The item type affects how it is executed:

- **String:** The command will be interpreted by `sh`.
- **List:** The items will be executed as if passed to `execve(3)` (the first argument is the command).

The `runcmd` module writes the script to be run later; the actual execution is handled by the `scripts_user` module during the **Final boot stage**.

> **Note:** All commands must be valid YAML. Quote characters that YAML might misinterpret (like `:`). Additionally, avoid using `/tmp` for file writing to avoid races with `systemd-tmpfiles-clean`; use `/run/somedir` instead.

- **Internal name:** `cc_runcmd`
- **Module frequency:** once-per-instance
- **Supported distros:** all
- **Activate only on keys:** `runcmd`

### Config Schema

- **runcmd:** (array of array of string/string/null)

### Examples

```yaml
#cloud-config
runcmd:
- [ls, -l, /]
- [sh, -xc, 'echo $(date) '': hello world!''']
- [sh, -c, echo "=========hello world'========="]
- ls -l /root
```

## Salt Minion

This module installs, configures and starts Salt Minion. If the `salt_minion` key is present in the config parts, then Salt Minion will be installed and started.

Configuration for Salt Minion can be specified in the `conf` key under `salt_minion`. Any config values present there will be assigned in `/etc/salt/minion`. The public and private keys to use for Salt Minion can be specified with `public_key` and `private_key` respectively.

If you have a custom package name, service name, or config directory, you can specify them with `pkg_name`, `service_name`, and `config_dir` respectively.

Salt keys can be manually generated by `salt-key --gen-keys=GEN_KEYS`, where `GEN_KEYS` is the name of the keypair, e.g. "minion". The keypair will be copied to `/etc/salt/pki` on the Minion instance.

**Internal name:** `cc_salt_minion`
**Module frequency:** once-per-instance
**Supported distros:** all
**Activate only on keys:** `salt_minion`

### Config Schema

- **salt_minion:** (object) Each object in **salt_minion** list supports the following keys:
  - **pkg_name:** (string) Package name to install. Default: `salt-minion`.
  - **service_name:** (string) Service name to enable. Default: `salt-minion`.
  - **config_dir:** (string) Directory to write config files to. Default: `/etc/salt`.
  - **conf:** (object) Configuration to be written to `config_dir`/minion.
  - **grains:** (object) Configuration to be written to `config_dir`/grains.
  - **public_key:** (string) Public key to be used by the salt minion.
  - **private_key:** (string) Private key to be used by salt minion.
  - **pki_dir:** (string) Directory to write key files. Default: `config_dir`/pki/minion.

### Examples

Example 1:

```yaml
#cloud-config
salt_minion:
  conf:
    file_client: local
    fileserver_backend: [gitfs]
    gitfs_remotes: ['[https://github.com/_user_/_repo_.git](https://github.com/_user_/_repo_.git)']
    master: salt.example.com
  config_dir: /etc/salt
  grains:
    role: [web]
  pkg_name: salt-minion
  pki_dir: /etc/salt/pki/minion
  private_key: <private_ssh_key>
  public_key: '------BEGIN PUBLIC KEY-------

    <key data>

    ------END PUBLIC KEY-------

    '
  service_name: salt-minion
```

## Scripts Per Boot

Any scripts in the `scripts/per-boot` directory on the datasource will be run every time the system boots. Scripts will be run in alphabetical order. This module does not accept any config keys.

**Internal name:** `cc_scripts_per_boot`
**Module frequency:** always
**Supported distros:** all

### Config Schema

- No schema definitions for this module

### Examples

No examples for this module

## Scripts Per Instance

Any scripts in the `scripts/per-instance` directory on the datasource will be run when a new instance is first booted. Scripts will be run in alphabetical order. This module does not accept any config keys.

Some cloud platforms change `instance-id` if a significant change was made to the system. As a result, per-instance scripts will run again.

- **Internal name:** `cc_scripts_per_instance`
- **Module frequency:** once-per-instance
- **Supported distros:** all

### Config Schema

- No schema definitions for this module

### Examples

No examples for this module

## Scripts Per Once

Any scripts in the `scripts/per-once` directory on the datasource will be run only once. Changes to the instance will not force a re-run. The only way to re-run these scripts is to run the `clean` subcommand and reboot. Scripts will be run in alphabetical order. This module does not accept any config keys.

- **Internal name:** `cc_scripts_per_once`
- **Module frequency:** once
- **Supported distros:** all

### Config Schema

No schema definitions for this module

### Examples

No examples for this module

## Scripts User

This module runs all user scripts present in the `scripts` directory in the instance configuration. Any cloud-config parts with a `#!` will be treated as a script and run. Scripts specified as cloud-config parts will be run in the order they are specified in the configuration. This module does not accept any config keys.

**Internal name:** `cc_scripts_user`
**Module frequency:** once-per-instance
**Supported distros:** all

### Config Schema

- No schema definitions for this module

### Examples

No examples for this module

## Scripts Vendor

On select Datasources, vendors have a channel for the consumption of all supported user data types via a special channel called vendor data. Any scripts in the `scripts/vendor` directory in the datasource will be run when a new instance is first booted. Scripts will be run in alphabetical order. This module allows control over the execution of vendor data.

**Internal name:** `cc_scripts_vendor`
**Module frequency:** once-per-instance
**Supported distros:** all

### Config Schema

- **vendor_data:** (object) Each object in **vendor_data** list supports the following keys:
  - **enabled:** (boolean/string) Whether vendor-data is enabled or not. Default: `true`. *Deprecated in version 22.3:* Use of type string for this value is deprecated. Use a boolean instead.
  - **prefix:** (['array', 'string'] of string/integer) The command to run before any vendor scripts. Its primary use case is for profiling a script, not to prevent its run.

### Examples

Example 1:

```yaml
#cloud-config
vendor_data: {enabled: true, prefix: /usr/bin/ltrace}
```

Example 2:

```yaml
#cloud-config
vendor_data:
  enabled: true
  prefix: [timeout, 30]
```

Example 3: Vendor data will not be processed.

```yaml
#cloud-config
vendor_data: {enabled: false}
```

## Seed Random

All cloud instances started from the same image will produce similar data when they are first booted as they are all starting with the same seed for the kernel’s entropy keyring. To avoid this, random seed data can be provided to the instance, either as a string or by specifying a command to run to generate the data.

Configuration for this module is under the `random_seed` config key. If the cloud provides its own random seed data, it will be appended to `data` before it is written to `file`.

If the `command` key is specified, the given command will be executed. This will happen after `file` has been populated. That command’s environment will contain the value of the `file` key as `RANDOM_SEED_FILE`. If a command is specified that cannot be run, no error will be reported unless `command_required` is set to `true`.

**Internal name:** `cc_seed_random`
**Module frequency:** once-per-instance
**Supported distros:** all

### Config Schema

- **random_seed:** (object) Each object in **random_seed** list supports the following keys:
  - **file:** (string) File to write random data to. Default: `/dev/urandom`.
  - **data:** (string) This data will be written to **file** before data from the datasource. When using a multi-line value or specifying binary data, be sure to follow YAML syntax and use the `|` and `!binary` YAML format specifiers when appropriate.
  - **encoding:** (`raw`/`base64`/`b64`/`gzip`/`gz`) Used to decode **data** provided. Allowed values are `raw`, `base64`, `b64`, `gzip`, or `gz`. Default: `raw`.
  - **command:** (array of string) Execute this command to seed random. The command will have RANDOM_SEED_FILE in its environment set to the value of **file** above.
  - **command_required:** (boolean) If true, and **command** is not available to be run then an exception is raised and cloud-init will record failure. Otherwise, only debug error is mentioned. Default: `false`.

### Examples

Example 1:

```yaml
#cloud-config
random_seed:
  command: [sh, -c, dd if=/dev/urandom of=$RANDOM_SEED_FILE]
  command_required: true
  data: my random string
  encoding: raw
  file: /dev/urandom
```

Example 2: Use `pollinate` to gather data from a remote entropy server and write it to `/dev/urandom`:

```yaml
#cloud-config
random_seed:
  command: [pollinate, '--server=[http://local.pollinate.server](http://local.pollinate.server)']
  command_required: true
  file: /dev/urandom
```

## Set Hostname

This module handles setting the system hostname and fully qualified domain name (FQDN). If `preserve_hostname` is set, then the hostname will not be altered.

A hostname and FQDN can be provided by specifying a full domain name under the `fqdn` key. Alternatively, a hostname can be specified using the `hostname` key, and the FQDN of the cloud will be used. If a FQDN is specified with the `hostname` key, it will be handled properly, although it is better to use the `fqdn` config key. If both `fqdn` and `hostname` are set, then `prefer_fqdn_over_hostname` will force use of FQDN in all distros when true, and when false it will force the short hostname. Otherwise, the hostname to use is distro-dependent.

> **Note:** Cloud-init performs no hostname input validation before sending the hostname to distro-specific tools, and most tools will not accept a trailing dot on the FQDN.

This module will run in the init-local stage before networking is configured if the hostname is set by metadata or user data on the local system. This ensures that the desired hostname is applied before any DHCP requests are performed on platforms like NoCloud and OVF where dynamic DNS is based on initial hostname.

**Internal name:** `cc_set_hostname`
**Module frequency:** once-per-instance
**Supported distros:** all

### Config Schema

- **preserve_hostname:** (boolean) If true, the hostname will not be changed. Default: `false`.
- **hostname:** (string) The hostname to set.
- **fqdn:** (string) The fully qualified domain name to set.
- **prefer_fqdn_over_hostname:** (boolean) If true, the fqdn will be used if it is set. If false, the hostname will be used. If unset, the result is distro-dependent.
- **create_hostname_file:** (boolean) If `false`, the hostname file (e.g. /etc/hostname) will not be created if it does not exist. On systems that use systemd, setting create_hostname_file to `false` will set the hostname transiently. If `true`, the hostname file will always be created and the hostname will be set statically on systemd systems. Default: `true`.

### Examples

Example 1:

```yaml
#cloud-config
preserve_hostname: true
```

Example 2:

```yaml
#cloud-config
hostname: myhost
create_hostname_file: true
fqdn: myhost.example.com
prefer_fqdn_over_hostname: true
```

Example 3: On a machine without an `/etc/hostname` file, don’t create it. In most clouds, this will result in a DHCP-configured hostname provided by the cloud.

```yaml
#cloud-config
create_hostname_file: false
```

## Set Passwords

Set user passwords and enable/disable SSH password auth. This module consumes three top-level config keys: `ssh_pwauth`, `chpasswd` and `password`.

The `ssh_pwauth` config key determines whether or not sshd will be configured to accept password authentication. The `chpasswd` config key accepts a dictionary containing `users` (to assign passwords to existing users) and `expire` (to force a password reset on the next login). The `password` config key sets the default user's password.

**Internal name:** `cc_set_passwords`
**Module frequency:** once-per-instance
**Supported distros:** all

### Config Schema

- **ssh_pwauth**: (boolean/string) Sets whether or not to accept password authentication. `true` will enable password auth, `false` will disable.
- **chpasswd**: (object) Each object in the **chpasswd** list supports the following keys:
  - **expire**: (boolean) Whether to expire all user passwords such that a password will need to be reset on the user’s next login. Default: `true`.
  - **users**: (array of object) A list of existing users to set passwords for. Each item requires **name** and **password** (or **name** and **type** for random passwords). **type** defaults to `hash`, but can be `text` or `RANDOM`.
  - **list**: (string/array of string) *Deprecated in version 22.2:* Use **users** instead.
- **password**: (string) Set the default user’s password. Ignored if **chpasswd** `users` (or the deprecated `list`) is used.

### Examples

**Example 1: Set a default password, to be changed at first login.**

```yaml
#cloud-config
{password: <REDACTED_PASSWORD>, ssh_pwauth: true}
```

**Example 2: Complex password configuration.**

- Disable SSH password authentication.
- Don’t require users to change their passwords on next login.
- Set the password for user1 to be ‘<REDACTED_PASSWORD>’ (OS does hashing).
- Set the password for user2 to a pre-hashed password.
- Set the password for user3 to be a randomly generated password.

```yaml
#cloud-config
chpasswd:
  expire: false
  users:
  - {name: user1, password: <REDACTED_PASSWORD>, type: text}
  - {name: user2, password: <REDACTED_HASHED_PASSWORD>}
  - {name: user3, type: RANDOM}
ssh_pwauth: false
```

**Example 3: Disable SSH password authentication and PAM interactive password authentication.**

```yaml
#cloud-config
ssh_pwauth: false
# Supplement sshd_config part with overrides for images using PAM
# for authentication on distributions which default to
# KbdInteractiveAuthentication yes in sshd_config.
write_files:
- path: /etc/ssh/sshd_config.d/70-no-pam-password-auth.conf
  content: 'KbdInteractiveAuthentication no'
  permissions: '0500'
```

## Snap

This module provides a simple configuration namespace in cloud-init for setting up snapd and installing snaps.

Both `assertions` and `commands` values can be either a dictionary or a list. If these configs are provided as a dictionary, the keys are only used to order the execution of the assertions or commands and the dictionary is merged with any vendor data the snap configuration provided. If a list is provided by the user instead of a dict, any vendor data snap configuration is ignored.

The `assertions` configuration option is a dictionary or list of properly-signed snap assertions, which will run before any snap commands. They will be added to snapd’s `assertion` database by invoking `snap ack <aggregate_assertion_file>`.

Snap `commands` is a dictionary or list of individual snap commands to run on the target system. These commands can be used to create snap users, install snaps, and provide snap configuration.

> **Note:** If ‘side-loading’ private/unpublished snaps on an instance, it is best to create a snap seed directory and `seed.yaml` manifest in `/var/lib/snapd/seed/` which snapd automatically installs on startup.

- **Internal name:** `cc_snap`
- **Module frequency:** once-per-instance
- **Supported distros:** ubuntu
- **Activate only on keys:** `snap`

### Config Schema

- **snap:** (object) Each object in **snap** list supports the following keys:
  - **assertions:** (['object', 'array'] of string) Properly-signed snap assertions which will run before and snap **commands**.
  - **commands:** (['object', 'array'] of string/array of string) Snap commands to run on the target system.

### Examples

Example 1:

```yaml
#cloud-config
snap:
  assertions:
    00: |
      signed_assertion_blob_here
    02: |
      signed_assertion_blob_here
  commands:
    00: snap create-user --sudoer --known <snap-user>@mydomain.com
    01: snap install canonical-livepatch
    02: canonical-livepatch enable <AUTH_TOKEN>
```

Example 2: For convenience, the `snap` command can be omitted when specifying commands as a list - `snap` will be automatically prepended. The following commands are all equivalent:

```yaml
#cloud-config
snap:
  commands:
    0: [install, vlc]
    1: [snap, install, vlc]
    2: snap install vlc
    3: snap install vlc
```

Example 3: You can use a list of commands.

```yaml
#cloud-config
snap:
  assertions:
    - signed_assertion_blob_here
    - |
      signed_assertion_blob_here
```

Example 4: You can also use a list of assertions.

```yaml
#cloud-config
snap:
  assertions:
    - signed_assertion_blob_here
    - |
      signed_assertion_blob_here
```

## Spacewalk

This module installs Spacewalk and applies basic configuration. If the Spacewalk config key is present, Spacewalk will be installed. The server to connect to after installation must be provided in the `server` in Spacewalk configuration. A proxy to connect through and an activation key may optionally be specified.

For more details about spacewalk see the [Fedora documentation](https://fedorahosted.org/spacewalk/).

**Internal name:** `cc_spacewalk`

**Module frequency:** once-per-instance

**Supported distros:** rhel, fedora, openeuler

**Activate only on keys:** `spacewalk`

### Config Schema

- **spacewalk:** (object) Each object in **spacewalk** list supports the following keys:
  - **server:** (string) The Spacewalk server to use.
  - **proxy:** (string) The proxy to use when connecting to Spacewalk.
  - **activation_key:** (string) The activation key to use when registering with Spacewalk.

### Examples

Example 1:

```yaml
#cloud-config
spacewalk: {activation_key: <key>, proxy: <proxy host>, server: <url>}
```

## SSH

This module handles the configuration for SSH, including both host keys and authorized keys. It allows for managing public keys for the default user, generating or deleting host keys, and controlling root login access.

- **Internal name:** `cc_ssh`
- **Module frequency:** once-per-instance
- **Supported distros:** all

### Config Schema

- **ssh_keys:** (object) A dictionary containing entries for public and private host keys (e.g., `rsa_private`, `rsa_public`, `rsa_certificate`). If specified, keys will not be automatically generated.
  - **<key_type>:** (string) The specific key content.
- **ssh_authorized_keys:** (array of string) List of SSH public keys to add to the default user's `.ssh/authorized_keys`.
- **ssh_deletekeys:** (boolean) Whether to remove existing host SSH keys to prevent re-use from an image. Default: `true`.
- **ssh_genkeytypes:** (array of `ecdsa`/`ed25519`/`rsa`) The types of SSH host keys to generate. Default: `[rsa, ecdsa, ed25519]`.
- **disable_root:** (boolean) Whether to disable root login. Default: `true`.
- **disable_root_opts:** (string) Options used when root login is disabled. Supports the `$USER` variable.
- **allow_public_ssh_keys:** (boolean) If true, imports public SSH keys from the datasource metadata. Default: `true`.
- **ssh_quiet_keygen:** (boolean) If true, suppresses `ssh-keygen` output on the console. Default: `false`.
- **ssh_publish_hostkeys:** (object) Configuration for publishing host keys to the datasource.
  - **enabled:** (boolean) Whether to read and publish keys from `/etc/ssh/*.pub`. Default: `true`.
  - **blacklist:** (array of string) SSH key types to ignore when publishing. Default: `[]`.

### Examples

```yaml
#cloud-config
allow_public_ssh_keys: true
disable_root: true
disable_root_opts: no-port-forwarding,no-agent-forwarding,no-X11-forwarding
ssh_authorized_keys: [<REDACTED_SSH_PUBLIC_KEY_1>, <REDACTED_SSH_PUBLIC_KEY_2>]
ssh_deletekeys: true
ssh_genkeytypes: [rsa, ecdsa, ed25519]
ssh_keys: {rsa_certificate: '<REDACTED_SSH_CERTIFICATE>', rsa_private: '<REDACTED_RSA_PRIVATE_KEY>', rsa_public: <REDACTED_SSH_PUBLIC_KEY>}
ssh_publish_hostkeys:
  blacklist: [rsa]
  enabled: true
ssh_quiet_keygen: true
```

## SSH AuthKey Fingerprints

Write fingerprints of authorized keys for each user to log. This is enabled by default, but can be disabled using `no_ssh_fingerprints`. The hash type for the keys can be specified, but defaults to `sha256`.

**Internal name:** `cc_ssh_authkey_fingerprints`
**Module frequency:** once-per-instance
**Supported distros:** all

### Config Schema

- **no_ssh_fingerprints:** (boolean) If true, SSH fingerprints will not be written. Default: `false`.
- **authkey_hash:** (string) The hash type to use when generating SSH fingerprints. Default: `sha256`.

### Examples

Example 1:

```yaml
#cloud-config
no_ssh_fingerprints: true
```

Example 2:

```yaml
#cloud-config
authkey_hash: sha512
```

## SSH Import ID

This module imports SSH keys from either a public keyserver (usually Launchpad), or GitHub, using `ssh-import-id`. Keys are referenced by the username they are associated with on the keyserver. The keyserver can be specified by prepending either `lp:` for Launchpad or `gh:` for GitHub to the username.

**Internal name:** `cc_ssh_import_id`

**Module frequency:** once-per-instance

**Supported distros:** alpine, cos, debian, raspberry-pi-os, ubuntu

### Config Schema

- **ssh_import_id:** (array of string)

### Examples

Example 1:

```yaml
#cloud-config
ssh_import_id: [user, 'gh:user', 'lp:user']
```

## Timezone

Sets the [system timezone](https://www.iana.org/time-zones) based on the value provided.

- **Internal name:** `cc_timezone`
- **Module frequency:** once-per-instance
- **Supported distros:** all
- **Activate only on keys:** `timezone`

### Config Schema

- **timezone:** (string) The timezone to use as represented in /usr/share/zoneinfo.

### Examples

Example 1:

```yaml
#cloud-config
timezone: America/New_York
```

## Ubuntu Drivers

This module interacts with the `ubuntu-drivers` command to install third party driver packages.

### Config Schema

- **drivers:** (object) Each object in **drivers** list supports the following keys:
  - **nvidia:** (object) Each object in **nvidia** list supports the following keys:
    - **license-accepted:** (boolean) Do you accept the NVIDIA driver license?
    - **version:** (string) The version of the driver to install (e.g. “390”, “410”). Default: latest version.

### Examples

Example 1:

```yaml
#cloud-config
drivers:
  nvidia: {license-accepted: true}
```

## Ubuntu Autoinstall

Autoinstall configuration is ignored (but validated) by cloud-init. Cloud-init is used by the Ubuntu installer in two stages. The `autoinstall` key may contain a configuration for the Ubuntu installer.

Cloud-init verifies that an `autoinstall` key contains a `version` key and that the installer package is present on the system.

> **Note**: The Ubuntu installer might pass part of this configuration to cloud-init during a later boot as part of the install process. See [the Ubuntu installer documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html#user-data) for more information. Please direct Ubuntu installer questions to their IRC channel (#ubuntu-server on Libera).

- **Internal name:** `cc_ubuntu_autoinstall`
- **Module frequency:** once
- **Supported distros:** ubuntu
- **Activate only on keys:** `autoinstall`

### Config Schema

- **autoinstall**: (object) Cloud-init ignores this key and its values. It is used by Subiquity, the Ubuntu Autoinstaller. See: <https://ubuntu.com/server/docs/install/autoinstall-reference>. Each object in **autoinstall** list supports the following keys:
  - **version**: (integer)

### Examples

Example 1:

```yaml
#cloud-config
autoinstall:
  version: 1
```

## Ubuntu Pro

Attach machine to an existing Ubuntu Pro support contract and enable or disable support services such as Livepatch, ESM, FIPS and FIPS Updates.

When attaching a machine to Ubuntu Pro, one can also specify services to enable. When the `enable` list is present, only named services will be activated. If the `enable` list is not present, the contract’s default services will be enabled.

On Pro instances, when `ubuntu_pro` config is provided to cloud-init, Pro’s auto-attach feature will be disabled and cloud-init will perform the Pro auto-attach, ignoring the `token` key. The `enable` and `enable_beta` values will strictly determine what services will be enabled, ignoring contract defaults.

Note that when enabling FIPS or FIPS updates you will need to schedule a reboot to ensure the machine is running the FIPS-compliant kernel.

**Internal name:** `cc_ubuntu_pro`
**Module frequency:** once-per-instance
**Supported distros:** ubuntu

### Config Schema

- **ubuntu_pro:** (object) Supports the following keys:
  - **enable:** (array of string) Optional list of Ubuntu Pro services to enable (e.g., cc-eal, cis, esm-infra, fips, fips-updates, livepatch).
  - **enable_beta:** (array of string) Optional list of Ubuntu Pro beta services to enable.
  - **token:** (string) Contract token obtained from <https://ubuntu.com/pro>. Required for non-Pro instances.
  - **features:** (object) Ubuntu Pro features:
    - **disable_auto_attach:** (boolean) Controls if `ua-auto-attach.service` is attempted each boot. Default: `false`.
  - **config:** (object) Configuration settings or overrides:
    - **http_proxy:** (string/null) Ubuntu Pro HTTP Proxy URL.
    - **https_proxy:** (string/null) Ubuntu Pro HTTPS Proxy URL.
    - **global_apt_http_proxy:** (string/null) HTTP Proxy URL for all APT repositories.
    - **global_apt_https_proxy:** (string/null) HTTPS Proxy URL for all APT repositories.
    - **ua_apt_http_proxy:** (string/null) HTTP Proxy URL used only for Ubuntu Pro APT repositories.
    - **ua_apt_https_proxy:** (string/null) HTTPS Proxy URL used only for Ubuntu Pro APT repositories.
- **ubuntu_advantage:** (object) *Deprecated in version 24.1:* Use **ubuntu_pro** instead. Supports the same keys as `ubuntu_pro`.

### Examples

**Example 1: Attach with token**
Attach the machine to an Ubuntu Pro support contract with a Pro contract token.

```yaml
#cloud-config
ubuntu_pro: {token: <ubuntu_pro_token>}
```

**Example 2: Enable specific services**
Attach the machine and enable only FIPS and ESM services.

```yaml
#cloud-config
ubuntu_pro:
  enable: [fips, esm]
  token: <ubuntu_pro_token>
```

**Example 3: Enable FIPS and reboot**
Attach the machine, enable FIPS, and perform a reboot once cloud-init completes.

```yaml
#cloud-config
power_state: {mode: reboot}
ubuntu_pro:
  enable: [fips]
  token: <ubuntu_pro_token>
```

**Example 4: Proxy configuration**
Set HTTP(s) proxies before attaching to Ubuntu Pro and enabling FIPS.

```yaml
#cloud-config
ubuntu_pro:
  token: <ubuntu_pro_token>
  config:
    http_proxy: 'http://some-proxy:8088'
    https_proxy: 'https://some-proxy:8088'
    global_apt_https_proxy: 'https://some-global-apt-proxy:8088/'
    global_apt_http_proxy: 'http://some-global-apt-proxy:8088/'
    ua_apt_http_proxy: '[http://192.0.2.60:3128](http://192.0.2.60:3128)'
    ua_apt_https_proxy: '[https://192.0.2.60:3128](https://192.0.2.60:3128)'
  enable:
  - fips
```

**Example 5: Auto-attach without extra services**
On Ubuntu Pro instances, auto-attach but don’t enable any additional services.

```yaml
#cloud-config
ubuntu_pro:
  enable: []
  enable_beta: []
```

**Example 6: Enable ESM and Beta services**
Enable ESM and beta Real-time Ubuntu services in Ubuntu Pro instances.

```yaml
#cloud-config
ubuntu_pro:
  enable: [esm]
  enable_beta: [realtime-kernel]
```

**Example 7: Disable auto-attach**
Disable auto-attach in Ubuntu Pro instances.

```yaml
#cloud-config
ubuntu_pro:
  features: {disable_auto_attach: true}
```

## Update Etc Hosts

This module will update the contents of the local hosts database (hosts file, usually `/etc/hosts`) based on the hostname/FQDN specified in config. Management of the hosts file is controlled using `manage_etc_hosts`. If this is set to `false`, cloud-init will not manage the hosts file at all. This is the default behavior.

If set to `true`, cloud-init will generate the hosts file using the template located in `/etc/cloud/templates/hosts.tmpl`. In the `/etc/cloud/templates/hosts.tmpl` template, the strings `$hostname` and `$fqdn` will be replaced with the hostname and FQDN respectively.

If `manage_etc_hosts` is set to `localhost`, then cloud-init will not rewrite the hosts file entirely, but rather will ensure that an entry for the FQDN with a distribution-dependent IP is present (i.e., `ping <hostname>` will ping `127.0.0.1` or `127.0.1.1` or other IP).

> **Note:** If `manage_etc_hosts` is set to `true`, the contents of the `hosts` file will be updated every boot. To make any changes to the `hosts` file persistent they must be made in `/etc/cloud/templates/hosts.tmpl`.
>
> **Note:** For instructions on specifying hostname and FQDN, see documentation for the `cc_set_hostname` module.

**Internal name:** `cc_update_etc_hosts`
**Module frequency:** always
**Supported distros:** all
**Activate only on keys:** `manage_etc_hosts`

### Config Schema

- **manage_etc_hosts:** (`True`/`False`/`localhost`/`template`) Whether to manage `/etc/hosts` on the system. If `true`, render the hosts file using `/etc/cloud/templates/hosts.tmpl` replacing `$hostname` and `$fqdn`. If `localhost`, append a `127.0.1.1` entry that resolves from FQDN and hostname every boot. Default: `false`. *Changed in version 22.3. Use of **template** is deprecated, use `true` instead.*
- **fqdn:** (string) Optional fully qualified domain name to use when updating `/etc/hosts`. Preferred over **hostname** if both are provided. In absence of **hostname** and **fqdn** in cloud-config, the `local-hostname` value will be used from datasource metadata.
- **hostname:** (string) Hostname to set when rendering `/etc/hosts`. If **fqdn** is set, the hostname extracted from **fqdn** overrides **hostname**.

### Examples

**Example 1: Do not update or manage `/etc/hosts` at all.**
This is the default behavior. Whatever is present at instance boot time will be present after boot. User changes will not be overwritten.

```yaml
#cloud-config
manage_etc_hosts: false
```

**Example 2: Manage `/etc/hosts` with cloud-init.**
On every boot, `/etc/hosts` will be re-written from `/etc/cloud/templates/hosts.tmpl`. The strings `$hostname` and `$fqdn` are replaced in the template with the appropriate values, either from the config-config `fqdn` or `hostname` if provided. When absent, the meta-data will be checked for `local-hostname` which can be split into `<hostname>.<fqdn>`. To make modifications persistent across a reboot, you must modify `/etc/cloud/templates/hosts.tmpl`.

```yaml
#cloud-config
manage_etc_hosts: true
```

**Example 3: Update `/etc/hosts` every boot with "localhost" entry.**
Providing a “localhost” `127.0.1.1` entry with the latest hostname and FQDN as provided by either IMDS or cloud-config. All other entries will be left alone. `ping hostname` will ping `127.0.1.1`.

```yaml
#cloud-config
manage_etc_hosts: localhost
```

## Update Hostname

This module will update the system hostname and FQDN. If `preserve_hostname` is set to `true`, then the hostname will not be altered.

> **Note**
> For instructions on specifying hostname and FQDN, see documentation for the `cc_set_hostname` module.

**Internal name:** `cc_update_hostname`
**Module frequency:** always
**Supported distros:** all

### Config Schema

- **preserve_hostname:** (boolean) Do not update system hostname when `true`. Default: `false`.
- **prefer_fqdn_over_hostname:** (boolean) By default, it is distro-dependent whether cloud-init uses the short hostname or fully qualified domain name when both `local-hostname` and `fqdn` are both present in instance metadata. When set `true`, use fully qualified domain name if present as hostname instead of short hostname. When set `false`, use **hostname** config value if present, otherwise fallback to **fqdn**.
- **create_hostname_file:** (boolean) If `false`, the hostname file (e.g. /etc/hostname) will not be created if it does not exist. On systems that use systemd, setting create_hostname_file to `false` will set the hostname transiently. If `true`, the hostname file will always be created and the hostname will be set statically on systemd systems. Default: `true`.

### Examples

Example 1: By default, when `preserve_hostname` is not specified, cloud-init updates `/etc/hostname` per-boot based on the cloud provided `local-hostname` setting. If you manually change `/etc/hostname` after boot cloud-init will no longer modify it.

This default cloud-init behavior is equivalent to this cloud-config:

```yaml
#cloud-config
preserve_hostname: false
```

Example 2: Prevent cloud-init from updating the system hostname.

```yaml
#cloud-config
preserve_hostname: true
```

Example 3: Prevent cloud-init from updating `/etc/hostname`.

```yaml
#cloud-config
preserve_hostname: true
```

Example 4: Set hostname to `external.fqdn.me` instead of `myhost`.

```yaml
#cloud-config
fqdn: external.fqdn.me
hostname: myhost
prefer_fqdn_over_hostname: true
create_hostname_file: true
```

Example 5: Set hostname to `external` instead of `external.fqdn.me` when meta-data provides the `local-hostname`: `external.fqdn.me`.

```yaml
#cloud-config
prefer_fqdn_over_hostname: false
```

Example 6: On a machine without an `/etc/hostname` file, don’t create it. In most clouds, this will result in a DHCP-configured hostname provided by the cloud.

```yaml
#cloud-config
create_hostname_file: false
```

## Users and Groups

This module configures users and groups on the system. Groups can be specified as a string of comma-separated names or a list of dictionaries to define members. Users are specified under the `users` key; the reserved string `default` represents the primary admin user defined in the system configuration. If no `users` key is provided, the default behavior is to create the default user. Note that groups are created before users, and security-sensitive options like plain-text passwords should be avoided in favor of SSH keys.

**Internal name:** `cc_users_groups`
**Module frequency:** once-per-instance
**Supported distros:** all

### Config Schema

- **groups**: (string, object, or array) List of groups to create.
  - **<group_name>**: (string or array) Optional list of usernames to add to the group.
- **user**: (dictionary) Overrides the `default_user` configuration in `/etc/cloud/cloud.cfg`. Supports the same keys as the `users` schema.
- **users**: (string, array, or object) List of users to be created. Each user object supports:
  - **name**: (string) Login name. Required.
  - **doas**: (array of strings) List of doas rules.
  - **expiredate**: (string) Date to disable the account.
  - **gecos**: (string) User comment (real name, etc.).
  - **groups**: (string, array, or object) Groups to add the user to.
  - **homedir**: (string) Path to home directory.
  - **inactive**: (string) Days until user is disabled.
  - **lock_passwd**: (boolean) Disable password login. Default: `true`.
  - **no_create_home**: (boolean) Skip home directory creation. Default: `false`.
  - **no_log_init**: (boolean) Do not initialize lastlog/faillog. Default: `false`.
  - **no_user_group**: (boolean) Do not create a group named after the user. Default: `false`.
  - **passwd**: (string) Hashed password for new users only.
  - **hashed_passwd**: (string) Hashed password applied even if user exists.
  - **plain_text_passwd**: (string) Clear text password (not recommended).
  - **create_groups**: (boolean) Enable/disable group creation for the user. Default: `true`.
  - **primary_group**: (string) Primary group name.
  - **selinux_user**: (string) SELinux user context.
  - **shell**: (string) Path to login shell.
  - **snapuser**: (string) Email for Snappy user creation.
  - **ssh_authorized_keys**: (array of strings) List of public SSH keys.
  - **ssh_import_id**: (array of strings) IDs to import SSH keys from.
  - **ssh_redirect_user**: (boolean) Disable SSH for this user and redirect to default user. Default: `false`.
  - **system**: (boolean) Create as a system user. Default: `false`.
  - **sudo**: (string, array, or boolean) Sudo rules for the user.
  - **uid**: (integer) Specific User ID.

### Examples

**Example 1: Add the default user**

```yaml
#cloud-config
users: [default]
```

**Example 2: Define groups and members**

```yaml
#cloud-config
groups:
- admingroup: [root, sys]
- cloud-users
```

**Example 3: Create a specific user with a custom shell**

```yaml
#cloud-config
users:
- name: newsuper
  shell: /bin/bash
```

**Example 4: User with doas rules**

```yaml
#cloud-config
users:
- doas: [permit nopass newsuper, deny newsuper as root]
  name: newsuper
```

**Example 5: Set SELinux user**

```yaml
#cloud-config
users:
- default
- {name: youruser, selinux_user: staff_u}
```

**Example 6: Redirect SSH logins**

```yaml
#cloud-config
users:
- default
- {name: nosshlogins, ssh_redirect_user: true}
```

**Example 7: Override default user configuration**

```yaml
#cloud-config
ssh_import_id: [<REDACTED_USERNAME>]
user: {name: mynewdefault, sudo: null}
```

**Example 8: Prevent default user creation**

```yaml
#cloud-config
users: []
```

## Wireguard

The WireGuard module provides a dynamic interface for configuring WireGuard (as a peer or server) in a straightforward way.

This module takes care of:

- Writing interface configuration files
- Enabling and starting interfaces
- Installing wireguard-tools package
- Loading WireGuard kernel module
- Executing readiness probes

**What is a readiness probe?**
The idea behind readiness probes is to ensure WireGuard connectivity before continuing the cloud-init process. This could be useful if you need access to specific services like an internal APT Repository Server (e.g., Landscape) to install/update packages.

**Example**
An edge device can’t access the internet but uses cloud-init modules which will install packages (e.g. `landscape`, `packages`, `ubuntu_advantage`). Those modules will fail due to missing internet connection. The `wireguard` module fixes that problem as it waits until all readiness probes (which can be arbitrary commands, e.g. checking if a proxy server is reachable over WireGuard network) are finished, before continuing the cloud-init `config` stage.

> **Note:** In order to use DNS with WireGuard you have to install the `resolvconf` package or symlink it to systemd’s `resolvectl`, otherwise `wg-quick` commands will throw an error message that executable `resolvconf` is missing, which leads the `wireguard` module to fail.

- **Internal name:** `cc_wireguard`
- **Module frequency:** once-per-instance
- **Supported distros:** ubuntu
- **Activate only on keys:** `wireguard`

### Config Schema

- **wireguard:** (null/object) Each object in **wireguard** list supports the following keys:
  - **interfaces:** (array of object) Each object in **interfaces** list supports the following keys:
    - **name:** (string) Name of the interface. Typically wgx (example: wg0).
    - **config_path:** (string) Path to configuration file of Wireguard interface.
    - **content:** (string) Wireguard interface configuration. Contains key, peer, ...
  - **readinessprobe:** (array of string) List of shell commands to be executed as probes.

### Examples

Configure one or more WireGuard interfaces and provide optional readiness probes.

```yaml
#cloud-config
wireguard:
  interfaces:
    - name: wg0
      config_path: /etc/wireguard/wg0.conf
      content: |
        [Interface]
        PrivateKey = <private_key>
        Address = <address>
        [Peer]
        PublicKey = <public_key>
        Endpoint = <endpoint_ip>:<endpoint_ip_port>
        AllowedIPs = <allowedip1>, <allowedip2>, ...
    - name: wg1
      config_path: /etc/wireguard/wg1.conf
      content: |
        [Interface]
        PrivateKey = <private_key>
        Address = <address>
        [Peer]
        PublicKey = <public_key>
        Endpoint = <endpoint_ip>:<endpoint_ip_port>
        AllowedIPs = <allowedip1>
  readinessprobe:
    - 'systemctl restart service'
    - 'curl [https://webhook.endpoint/example](https://webhook.endpoint/example)'
    - 'nc -zv some-service-fqdn 443'
```

## Write Files

Write out arbitrary content to files, optionally setting permissions. Parent folders in the path are created if absent. Content can be specified in plain text or binary. Data encoded with either base64 or binary gzip data can be specified and will be decoded before being written. Data can also be loaded from an arbitrary URI. For empty file creation, content can be omitted.

**Internal name:** `cc_write_files`
**Module frequency:** once-per-instance
**Supported distros:** all
**Activate only on keys:** `write_files`

> [!NOTE]
> If multi-line data is provided, care should be taken to ensure it follows YAML formatting standards. To specify binary data, use the YAML option `!!binary`.

> [!NOTE]
> Do not write files under `/tmp` during boot because of a race with `systemd-tmpfiles-clean` that can cause temporary files to be cleaned during the early boot process. Use `/run/somedir` instead to avoid a race (LP: #1707222).

> [!WARNING]
> Existing files will be overridden.

### Config Schema

- **write_files:** (array of object) Each object in **write_files** list supports the following keys:
  - **path:** (string) Path of the file to which **content** is decoded and written.
  - **content:** (string) Optional content to write to the provided **path**. When content is present and encoding is not ‘text/plain’, decode the content prior to writing. Default: `''`.
  - **source:** (object) Optional specification for content loading from an arbitrary URI. Each object in **source** list supports the following keys:
    - **uri:** (string) URI from which to load file content. If loading fails repeatedly, **content** is used instead.
    - **headers:** (object) Optional HTTP headers to accompany load request, if applicable.
  - **owner:** (string) Optional owner:group to chown on the file and new directories. Default: `root:root`.
  - **permissions:** (string) Optional file permissions to set on **path** represented as an octal string ‘0###’. Default: `0o644`.
  - **encoding:** (`gz`/`gzip`/`gz+base64`/`gzip+base64`/`gz+b64`/`gzip+b64`/`b64`/`base64`/`text/plain`) Optional encoding type of the content. Default: `text/plain`. Supported encoding types are: gz, gzip, gz+base64, gzip+base64, gz+b64, gzip+b64, b64, base64.
  - **append:** (boolean) Whether to append **content** to existing file if **path** exists. Default: `false`.
  - **defer:** (boolean) Defer writing the file until ‘final’ stage, after users were created, and packages were installed. Default: `false`.

### Examples

Example 1: Write out base64-encoded content to `/etc/sysconfig/selinux`.

```yaml
#cloud-config
write_files:
- encoding: b64
  content: <REDACTED_BASE64_CONTENT>
  owner: root:root
  path: /etc/sysconfig/selinux
  permissions: '0644'
```

Example 2: Appending content to an existing file.

```yaml
#cloud-config
write_files:
- content: |
    15 * * * * root ship_logs
  path: /etc/crontab
  append: true
```

Example 3: Provide gzipped binary content

```yaml
#cloud-config
write_files:
- encoding: gzip
  content: !!binary |
      <REDACTED_GZIP_BASE64_CONTENT>
  path: /usr/bin/hello
  permissions: '0755'
```

Example 4: Create an empty file on the system

```yaml
#cloud-config
write_files:
- path: /root/CLOUD_INIT_WAS_HERE
```

Example 5: Defer writing the file until after the package (Nginx) is installed and its user is created.

```yaml
#cloud-config
write_files:
- path: /etc/nginx/conf.d/example.com.conf
  content: |
    server {
        server_name example.com;
        listen 80;
        root /var/www;
        location / {
            try_files $uri $uri/ $uri.html =404;
        }
    }
  owner: 'nginx:nginx'
  permissions: '0640'
  defer: true
```

Example 6: Retrieve file contents from a URI source, rather than inline. Especially useful with an external config-management repo, or for large binaries.

```yaml
#cloud-config
write_files:
- source:
    uri: [https://gitlab.example.com/some_ci_job/artifacts/hello](https://gitlab.example.com/some_ci_job/artifacts/hello)
    headers:
      Authorization: Basic <REDACTED_BASE64_CREDENTIAL>
      User-Agent: cloud-init on myserver.example.com
  path: /usr/bin/hello
  permissions: '0755'
```

## Yum Add Repo

Add yum repository configuration to `/etc/yum.repos.d`. Configuration files are named based on the opaque dictionary key under the `yum_repos` they are specified with. If a config file already exists with the same name as a config entry, the config entry will be skipped.

- **Internal name:** `cc_yum_add_repo`
- **Module frequency:** once-per-instance
- **Supported distros:** almalinux, azurelinux, centos, cloudlinux, eurolinux, fedora, mariner, openeuler, OpenCloudOS, openmandriva, photon, rhel, rocky, TencentOS, virtuozzo
- **Activate only on keys:** `yum_repos`

### Config Schema

- **yum_repo_dir:** (string) The repo parts directory where individual yum repo config files will be written. Default: `/etc/yum.repos.d`.
- **yum_repos:** (object) Each object in **yum_repos** list supports the following keys:
  - **<repo_name>:** (object) Object keyed on unique yum repo IDs. The key used will be used to write yum repo config files in `yum_repo_dir`/<repo_key_id>.repo. Each object in **<repo_name>** list supports the following keys:
    - **<yum_config_option>:** (integer/boolean/string) Any supported yum repository configuration options will be written to the yum repo config file. See: man yum.conf.
    - **baseurl:** (string) URL to the directory where the yum repository’s ‘repodata’ directory lives.
    - **metalink:** (string) Specifies a URL to a metalink file for the repomd.xml.
    - **mirrorlist:** (string) Specifies a URL to a file containing a baseurls list.
    - **name:** (string) Optional human-readable name of the yum repo.
    - **enabled:** (boolean) Whether to enable the repo. Default: `true`.

### Examples

Example 1:

```yaml
#cloud-config
yum_repos:
  my_repo:
    baseurl: [http://blah.org/pub/epel/testing/5/$basearch/](http://blah.org/pub/epel/testing/5/$basearch/)
yum_repo_dir: /store/custom/yum.repos.d
```

Example 2: Enable cloud-init upstream’s daily testing repo for EPEL 8 to install the latest cloud-init from tip of `main` for testing.

```yaml
#cloud-config
yum_repos:
  cloud-init-daily:
    name: Copr repo for cloud-init-dev owned by @cloud-init
    baseurl: [https://download.copr.fedorainfracloud.org/results/@cloud-init/cloud-init-dev/epel-8-$basearch/](https://download.copr.fedorainfracloud.org/results/@cloud-init/cloud-init-dev/epel-8-$basearch/)
    type: rpm-md
    skip_if_unavailable: true
    gpgcheck: true
    gpgkey: [https://download.copr.fedorainfracloud.org/results/@cloud-init/cloud-init-dev/pubkey.gpg](https://download.copr.fedorainfracloud.org/results/@cloud-init/cloud-init-dev/pubkey.gpg)
    enabled_metadata: 1
```

Example 3: Add the file `/etc/yum.repos.d/epel_testing.repo` which can then subsequently be used by yum for later operations.

```yaml
#cloud-config
yum_repos:
# The name of the repository
 epel-testing:
   baseurl: [https://download.copr.fedorainfracloud.org/results/@cloud-init/cloud-init-dev/pubkey.gpg](https://download.copr.fedorainfracloud.org/results/@cloud-init/cloud-init-dev/pubkey.gpg)
   enabled: false
   failovermethod: priority
   gpgcheck: true
   gpgkey: file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL
   name: Extra Packages for Enterprise Linux 5 - Testing
```

Example 4: Any yum repo configuration can be passed directly into the repository file created. See `man yum.conf` for supported config keys. Write `/etc/yum.conf.d/my-package-stream.repo` with `gpgkey` checks on the repo data of the repository enabled.

```yaml
#cloud-config
yum_repos:
  my package stream:
    baseurl: [http://blah.org/pub/epel/testing/5/$basearch/](http://blah.org/pub/epel/testing/5/$basearch/)
    mirrorlist: http://some-url-to-list-of-baseurls
    repo_gpgcheck: 1
    enable_gpgcheck: true
    gpgkey: [https://url.to.ascii-armored-gpg-key](https://url.to.ascii-armored-gpg-key)
```

## Zypper Add Repo

Configure Zypper behavior and add Zypper repositories.

Zypper behavior can be configured using the `config` key, which will modify `/etc/zypp/zypp.conf`. The configuration writer will only append the provided configuration options to the configuration file. Any duplicate options will be resolved by the way the `zypp.conf` INI file is parsed.

**Note:** Setting `configdir` is not supported and will be skipped.

The `repos` key may be used to add repositories to the system. Beyond the required `id` and `baseurl` attributions, no validation is performed on the `repos` entries.

It is assumed the user is familiar with the Zypper repository file format. This configuration is also applicable for systems with transactional-updates.

**Internal name:** `cc_zypper_add_repo`
**Module frequency:** always
**Supported distros:** opensuse, opensuse-microos, opensuse-tumbleweed, opensuse-leap, sle_hpc, sle-micro, sles
**Activate only on keys:** `zypper`

### Config Schema

- **zypper:** (object) Each object in **zypper** list supports the following keys:
  - **repos:** (array of object) Each object in **repos** list supports the following keys:
    - **id:** (string) The unique id of the repo, used when writing /etc/zypp/repos.d/<id>.repo.
    - **baseurl:** (string) The base repository URL.
  - **config:** (object) Any supported zypp.conf key is written to `/etc/zypp/zypp.conf`.

### Examples

Example 1:

```yaml
#cloud-config
zypper:
  config: {download.use_deltarpm: true, reposdir: /etc/zypp/repos.dir, servicesdir: /etc/zypp/services.d}
  repos:
  - {autorefresh: 1, baseurl: '[http://dl.opensuse.org/dist/leap/v/repo/oss/](http://dl.opensuse.org/dist/leap/v/repo/oss/)', enabled: 1,
    id: opensuse-oss, name: os-oss}
  - {baseurl: '[http://dl.opensuse.org/dist/leap/v/update](http://dl.opensuse.org/dist/leap/v/update)', id: opensuse-oss-update,
    name: os-oss-up}
```
