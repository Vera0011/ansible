---
layout: default
title: Hardening
parent: Tools
grand_parent: English
---

# Hardening

## Introduction

This role modifies the system, implementing secure configurations and hardening services. </br>
This role belong to the `Blue Team` section.

## Implementation

The implementation of this role in Ansible is as follows:

1. Depending on the selected options, Ansible will perform changes to the system.
2. Available modules:

- `GRUB`: Deactivates recovery, sets a master password for GRUB.
- `CoreDumps`: Disables coredumps in the system.
- `Passwords`: Sets a policy for password management, changes default UMASK, activates logs, locks root account password, forces the usage of SHA512 for password storage and increases to a safe limit the hashing rounds.
- `Ports`: Disables physical and logical ports (serial, USB).
- `Protocols`: Disables unused or unsafe network protocols.
- `Banners`: Sets a custom banner to display on system access.
- `Antivirus`: Installs and configures multiple software related to malware and viruses.
- `Patch management`: Installs and configures multiple software related to patch management. Enables automatic security updates.
- `Partitions`: Moves critical sections (`/home`, `/var`, `/home`) to separate partitions. The option to create new ones (and encrypted with LUKS) is available.
- `Auditory`: Installs and configures multiple software related to auditory.
- `Services`: Applies Systemd and AppArmor hardening units to specific services.

## Usage

1. Run the playbook (instructions can be found [here](../../../../roles/hardening/README.md))
2. All selected settings should have been applied.
