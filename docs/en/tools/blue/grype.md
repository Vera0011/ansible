---
layout: default
title: Grype
parent: Tools
grand_parent: English
---

# Grype

## Introduction

Grype is an installable software. It is used to perform vulnerability scans on container images, file systems, and directories, identifying CVEs in system dependencies. </br>
This tool belongs to the `Blue Team` section.

## Implementation

The implementation of this tool in Ansible is as follows:

1. Grype is installed and configured on the specified host
2. A configuration file is set up in `/etc/grype/config.yaml` with the analysis parameters
3. The `GRYPE_CONFIG` environment variable is set at the system level to reference the configuration file

## Usage

1. Run the playbook (instructions can be found [here](../../../../roles/grype/README.md))
2. After installation, run the following command:

```bash
grype <target>
```

3. The report will be generated to standard output. Some usage examples:

```bash
grype .                      # Scans the current directory
grype ubuntu:22.04           # Scans a container image
grype sbom:./sbom.json       # Scans an existing SBOM
```
