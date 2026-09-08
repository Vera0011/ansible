---
layout: default
title: Lynis
parent: Tools
permalink: /en/v1.1.0/lynis
---

# Lynis

## Introduction

Lynis is an installable tool used to perform system security audits, analyzing configurations, vulnerabilities, and the overall health of the system. It belongs to the `Blue Team` section.

## Implementation

When installed via this repository's Ansible role, Lynis is set up as follows:

1. Lynis is installed and configured on the specified host.
2. A dedicated user and group are used to run Lynis. If they don't already exist, they are created automatically (the created user is of type "system" and has no home directory).
3. A cron job can optionally be configured for automatic report generation.
4. The following compliance standards are currently enabled:
   - `cis`
   - `iso27001`
   - `pci-dss`
5. No license is included, since this setup uses the community version of Lynis.

## Ansible role usage

```yaml
- hosts: example-host
  become: true
  roles:
    - lynis
  vars:
    lynis_lang: en
    lynis_user: lynis
    lynis_group: lynis
    lynis_time:
      weekday: "0"
      hour: "3"
      minute: "0"
```

### Properties

- `lynis_user` (string, optional): Name of the user that can execute the binary and access reports/logs (default: `lynis`)
- `lynis_group` (string, optional): Name of the group that can execute the binary and access reports/logs (default: `lynis`)
- `lynis_lang` (string, optional): Language of the generated report (default: `en`)
- `lynis_time` (dictionary, optional): If present, a cron job is scheduled at the specified time. Default: `weekday: "0"`, `hour: "3"`, `minute: "0"` (every Sunday at 3 AM). Available fields:

```yaml
month: "0"
day: "0"
weekday: "0"
hour: "0"
minute: "0"
```

## Command-line usage

Once installed, Lynis can be run directly on the host:

```bash
lynis audit system
```

The report is generated and stored in `/var/log/lynis/`. Note that running this command requires superuser (`root`) privileges, or membership in the group configured for Lynis in the playbook.

## Test suite

This role has been tested with the following host configurations:

### Target hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Manager hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
