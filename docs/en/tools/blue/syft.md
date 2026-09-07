---
layout: default
title: Syft
parent: Tools
grand_parent: English
---

# Syft

## Introduction

Syft is an installable software. It is used to generate an SBOM of a variety of scan targets, that can be ingested in a tool like Grype. </br>
This tool belongs to the `Blue Team` section.

## Implementation

The implementation of this tool in Ansible is as follows:

1. Syft is installed and configured on the specified host
2. A configuration file is set up in `/etc/syft/config.yaml` with the analysis parameters
3. The `SYFT_CONFIG` environment variable is set at the system level to reference the configuration file

## Usage

1. Run the playbook (instructions can be found [here](../../../../roles/syft/README.md))
2. After installation, run the following command:

```bash
syft <target>
```

3. The report will be generated to standard output. Some usage examples:

```bash
syft .                      # Scans the current directory
syft ubuntu:22.04           # Scans a container image
```
