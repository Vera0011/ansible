---
layout: default
title: Auditory
parent: Tools
grand_parent: v1.1.0
permalink: /en/v1.1.0/auditory
---

# Auditory

## Introduction

This role runs a set of security auditing tools on the target host, collects their reports, and sends the results back to the controller. This role belongs to the `Blue Team` section.

The following tools are executed, in order, and for the purpose described:

- **[Lynis](/en/v1.1.0/lynis)** — Scans the host and reports recommended hardening measures that are currently missing.
- **[Syft](/en/v1.1.0/syft)** — Generates a Software Bill of Materials (SBOM) for the host.
- **[Grype](/en/v1.1.0/grype)** — Scans the Syft-generated SBOM for known vulnerabilities.
- **[Grant](/en/v1.1.0/grant)** — Checks the Syft-generated SBOM for license compliance issues.

This role does **not install** any tools on the target host. All binaries live on the controller. For each run, the required tools are:

1. Compressed on the controller
2. Transferred to the target host
3. Executed on the target host
4. Removed from the target host once execution finishes

This keeps the target host clean — no auditing tools are left installed after the role completes.

## Usage

```yaml
- hosts: example-host
  become: true
  roles:
    - audit
```

{: .note }
This example uses `become: true` because the role needs elevated privileges to run tools such as Lynis, which inspect system-level configuration.

## Test suite

This role has been tested with the following host configurations:

### Target hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Manager hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
