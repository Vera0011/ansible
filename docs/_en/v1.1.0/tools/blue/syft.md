---
layout: default
title: Syft
parent: Tools
permalink: /en/v1.1.0/syft
---

# Syft

## Introduction

Syft is an installable tool used to generate a Software Bill of Materials (SBOM) from a variety of scan targets. The resulting SBOM can be ingested by tools like Grype. It belongs to the `Blue Team` section.

## Implementation

When installed via this repository's Ansible role, Syft is set up as follows:

1. Syft is installed and configured on the specified host.
2. A configuration file is created at `/etc/syft/config.yaml` with the analysis parameters.
3. The `SYFT_CONFIG` environment variable is set at the system level, pointing to that configuration file.
4. Optionally, a cron job is configured to run report generation automatically on a schedule.

## Ansible role usage

```yaml
- hosts: example-host
  become: true
  roles:
    - syft
  vars:
    syft_user: syft
    syft_group: syft
    syft_time:
      weekday: "0"
      hour: "3"
      minute: "0"
```

### Properties

- `syft_user` (string, optional): Name of the user that can execute the binary and access reports/logs (default: `syft`)
- `syft_group` (string, optional): Name of the group that can execute the binary and access reports/logs (default: `syft`)
- `syft_time` (dictionary, optional): If present, a cron job is scheduled at the specified time. Default: `weekday: "0"`, `hour: "3"`, `minute: "0"` (every Sunday at 3 AM). Available fields:

```yaml
month: "0"
day: "0"
weekday: "0"
hour: "0"
minute: "0"
```

## Command-line usage

Once installed, Syft can be run directly on the host:

```bash
syft <target>
```

The report is printed to standard output. Some usage examples:

```bash
syft .                      # Scans the current directory
syft ubuntu:22.04           # Scans a container image
```

## Test suite

This role has been tested with the following host configurations:

### Target hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Manager hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
