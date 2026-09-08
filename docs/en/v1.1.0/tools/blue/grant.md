---
layout: default
title: Grant
parent: Tools
grand_parent: v1.1.0
permalink: /en/v1.1.0/grant
---

# Grant

## Introduction

Grant is an installable tool used to perform license scanning of dependencies. It belongs to the `Blue Team` section.

## Implementation

When installed via this repository's Ansible role, Grant is set up as follows:

1. Grant is installed and configured on the specified host.
2. A configuration file is created at `/etc/grant/config.yaml` with the analysis parameters.
3. The `GRANT_CONFIG` environment variable is set at the system level, pointing to that configuration file.
4. Optionally, a cron job is configured to run scans automatically on a schedule.

## Ansible role usage

```yaml
- hosts: example-host
  become: true
  roles:
    - grant
  vars:
    grant_package_name: grant
    grant_group: grant
    grant_user: grant
    grant_time:
      weekday: "0"
      hour: "3"
      minute: "0"
```

### Properties

- `grant_package_name` (string, optional): Name of the package to install (default: `grant`)
- `grant_user` (string, optional): Name of the user that can execute the binary and access reports/logs (default: `grant`)
- `grant_group` (string, optional): Name of the group that can execute the binary and access reports/logs (default: `grant`)
- `grant_time` (dictionary, optional): If present, a cron job is scheduled at the specified time. Default: `weekday: "0"`, `hour: "3"`, `minute: "0"` (every Sunday at 3 AM). Available fields:

```yaml
month: "0"
day: "0"
weekday: "0"
hour: "0"
minute: "0"
```

## Command-line usage

Once installed, Grant can be run directly on the host:

```bash
grant list <target>
```

The report is printed to standard output. Some usage examples:

```bash
grant list .                      # Scans the current directory
grant list ubuntu:22.04           # Scans a container image
grant list sbom:./sbom.json       # Scans an existing SBOM
```

## Test suite

This role has been tested with the following host configurations:

### Target hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
- Ubuntu Server 24.04 (Noble Numbat)

### Manager hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
