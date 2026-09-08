---
layout: default
title: Hardening
parent: Tools
permalink: /en/v1.1.0/hardening
---

# Hardening

## Introduction

This role applies secure configurations and hardening measures to a system. It belongs to the `Blue Team` section.

The role is **module-based**, so you can enable only the modules relevant to your use case. Each task and block includes annotations referencing the related Lynis recommendation.

{: .warning }
If you don't know what a specific module changes, don't enable it. The default set of modules is normally enough to provide solid baseline security, but some options can lock you out of the system if misconfigured.

## Implementation

Depending on which modules are enabled, Ansible applies the corresponding changes to the system. Available modules:

- **`hardening_grub`** — Disables GRUB recovery mode and sets a master password required at GRUB startup. Default: `false`.
- **`hardening_coredumps`** — Disables all core dumps on the system. Default: `true`.
- **`hardening_passwords`** — Sets password expiration policy, changes the default UMASK, enables `su` logging, locks the root account password, forces password storage via SHA512, increases hashing rounds, and installs `libpam-passwdqc` and `libpam-pwquality`. Default: `true`.
- **`hardening_ports`** — Disables USB, restricts access to serial ports, disables other physical access ports, and removes `firewire-core` and `firewire-ohci`. Default: `true`.
- **`hardening_protocols`** — Disables the `dccp`, `sctp`, `rds`, and `tipc` network protocols. Default: `true`.
- **`hardening_banners`** — Sets a custom banner in `/etc/issue` and `/etc/issue.net`, shown on system access. Default: `true`.
- **`hardening_antivirus`** — Installs `rkhunter`, `clamav`, and `chkrootkit`. Default: `true`.
- **`hardening_patch_management`** — Installs `debsums`, `unattended-upgrades`, `apt-listchanges`, and `apt-show-versions`, and enables automatic security updates. Default: `true`.
- **`hardening_partitions`** — Moves the `/home`, `/var`, and `/tmp` partitions to a new disk (preserving existing data; requires an empty disk to be available), and creates a LUKS-encrypted `/secrets` partition. Default: `false`.
- **`hardening_auditory`** — Installs AIDE, Sysstat, and AuditD, initializes and starts them, and adds custom audit rules (sourced from Neo23x0). Default: `true`.
- **`hardening_services`** — Applies Systemd unit and AppArmor hardening to specific services. Currently, only the `UFW` service is hardened. Default: `true`.

### Consequences of misconfiguration

{: .warning }
The following modules can cause outages if enabled without understanding their effect:

- **GRUB modification** — Losing the GRUB password locks you out of the system entirely; a broken configuration can also prevent the system from booting.
- **Partition modification** — Data loss is possible; losing the encryption key locks you out of the encrypted partition; a broken configuration can prevent the system from mounting correctly.

## Usage

```yaml
- hosts: example-host
  become: true
  roles:
    - hardening
  vars:
    hardening_grub: false
    hardening_coredumps: false
    hardening_passwords: true
    hardening_ports: true
    hardening_protocols: true
    hardening_banners: true
    hardening_antivirus: true
    hardening_patch_management: true
    hardening_partitions: false
    hardening_auditory: true
    hardening_services: true
```

Once the playbook has run, all selected settings will have been applied to the target host.

## Properties

- `hardening_grub` (boolean, optional): Enables the GRUB hardening module. Default: `false`.
- `hardening_coredumps` (boolean, optional): Enables the core dump hardening module. Default: `true`.
- `hardening_passwords` (boolean, optional): Enables the password hardening module. Default: `true`.
- `hardening_ports` (boolean, optional): Enables the port hardening module (USB and other media). Default: `true`.
- `hardening_protocols` (boolean, optional): Enables the network protocol hardening module. Default: `true`.
- `hardening_banners` (boolean, optional): Enables the banner hardening module. Default: `true`.
- `hardening_antivirus` (boolean, optional): Enables antivirus installation and configuration. Default: `true`.
- `hardening_patch_management` (boolean, optional): Enables the patch management module. Default: `true`.
- `hardening_partitions` (boolean, optional): Enables the partition hardening module. Default: `false`.
- `hardening_auditory` (boolean, optional): Enables the auditory module. Default: `true`.
- `hardening_services` (boolean, optional): Enables the service hardening module. Default: `true`.

## Test suite

This role has been tested with the following host configurations:

### Target hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Manager hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
