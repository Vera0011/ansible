---
layout: default
title: Auditory
parent: Tools
grand_parent: English
---

# Auditory

## Introduction

This role executes multiple tools, gather their reports and sends back to the controller. The following tools are executed and the intention:

- [Lynis](./lynis.md): Gather recommended missing hardening features
- [Syft](./syft.md): Executes Syft to generate an SBOM.
- [Grype](./grype.md): Executes Grype based on the Syft SBOM.
- [Grant](./grant.md): Executes Grant based on the Syft SBOM.

This role does not install any tools. All tools and binaries are located in the controller. They are compressed, sent to the host, executed and then removed from the host.

## Usage

```yaml
- hosts: example-host
  become: true
  roles:
    - audit
```

## Test suite

The role has been tested in the following hosts:

### Target hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Manager hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
