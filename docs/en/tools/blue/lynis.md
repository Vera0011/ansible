---
layout: default
title: Lynis
parent: Tools
grand_parent: English
---

# Lynis

## Introduction

Lynis is an installable software. It is used to perform system security audits, analyzing configurations, vulnerabilities, and the overall health of the system. </br>
This tool belongs to the `Blue Team` section.

## Implementation

The implementation of this tool in Ansible is as follows:

1. Lynis is installed and configured on the specified host
2. A dedicated user and group are used to run Lynis. If they do not exist, they are automatically created (the created user is "system" type and does not have a home path set)
3. A cron job is configured (optionally) for the automatic generation of reports
4. The current activated compliance standards are:
   - `cis`
   - `iso27001`
   - `pci-dss`
5. No license is provided within the script, as the community version is used

## Usage

1. Run the playbook (instructions can be found [here](../../../../roles/lynis/README.md))
2. After installation, run the following command:

```bash
lynis audit system
```

3. The report will be generated and stored in `/var/log/lynis/`. Note that execution requires superuser (`root`) privileges or membership in the group specified in the playbook.
