---
layout: default
title: Grype
parent: Tools
permalink: /en/v1.1.0/grype
---

# Grype

## Introduction

Grype is an installable tool used to perform vulnerability scans on container images, file systems, and directories, identifying CVEs in system dependencies. It belongs to the `Blue Team` section.

## Implementation

When installed via this repository's Ansible role, Grype is set up as follows:

1. Grype is installed and configured on the specified host.
2. A configuration file is created at `/etc/grype/config.yaml` with the analysis parameters.
3. The `GRYPE_CONFIG` environment variable is set at the system level, pointing to that configuration file.
4. Optionally, a cron job is configured to run scans automatically on a schedule.

## Ansible role usage

```yaml
- hosts: example-host
  become: true
  roles:
    - grype
  vars:
    grype_package_name: grype
    grype_group: grype
    grype_user: grype
    grype_time:
      weekday: "0"
      hour: "3"
      minute: "0"
```

### Properties

- `grype_package_name` (string, optional): Name of the package to install (default: `grype`)
- `grype_user` (string, optional): Name of the user that can execute the binary and access reports/logs (default: `grype`)
- `grype_group` (string, optional): Name of the group that can execute the binary and access reports/logs (default: `grype`)
- `grype_time` (dictionary, optional): If present, a cron job is scheduled at the specified time. Default: `weekday: "0"`, `hour: "3"`, `minute: "0"` (every Sunday at 3 AM). Available fields:

```yaml
month: "0"
day: "0"
weekday: "0"
hour: "0"
minute: "0"
```

## Command-line usage

Once installed, Grype can be run directly on the host:

```bash
grype <target>
```

The report is printed to standard output. Some usage examples:

```bash
grype .                      # Scans the current directory
grype ubuntu:22.04           # Scans a container image
grype sbom:./sbom.json       # Scans an existing SBOM
```

## Test suite

This role has been tested with the following host configurations:

### Target hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Manager hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
