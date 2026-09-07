---
layout: default
title: Grant
parent: Tools
grand_parent: English
---

# Grant

## Introduction

Grant is an installable software. It is used to perform license scanning of dependencies. </br>
This tool belongs to the `Blue Team` section.

## Implementation

The implementation of this tool in Ansible is as follows:

1. Grant is installed and configured on the specified host
2. A configuration file is set up in `/etc/grant/config.yaml` with the analysis parameters
3. The `GRANT_CONFIG` environment variable is set at the system level to reference the configuration file

## Usage

1. Run the playbook (instructions can be found [here](../../../../roles/grant/README.md))
2. After installation, run the following command:

```bash
grant list <target>
```

3. The report will be generated to standard output. Some usage examples:

```bash
grant list .                      # Scans the current directory
grant list ubuntu:22.04           # Scans a container image
grant list sbom:./sbom.json       # Scans an existing SBOM
```
