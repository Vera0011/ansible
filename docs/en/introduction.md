---
layout: default
title: Introduction
nav_order: 2
parent: English
---

# 1. Introduction

EasySec is a repository containing roles, documentation, and tools that help small and medium-sized enterprises (SMEs) implement security measures in their own organizations. It also supports penetration testing and red teaming exercises.

This file serves as an index, making it easier to browse and understand the available tools and documentation.

All tools and workflows in this repository are **idempotent**: running them once or multiple times always produces the same end result.

# 2. Documentation organization

Documentation is organized by software version. New tools, workflows, and instructions are documented under the version in which they were introduced. Unless stated otherwise, each new version also includes all tools from previous versions — so you don't need to check older version docs to find something still in use.

# 3. Roadmap

The list below tracks tools and environments planned for the project. Checked items are already implemented; unchecked items are planned, in no particular priority order unless noted.

## 3.1 Networking & Access

- [x] [Proxychains + Tor](v1.1.0/proxychains)
- [x] [Keycloak](v1.1.0/keycloak)
- [ ] Netmaker
- [ ] Pomerium
- [ ] Netbird
- [ ] Teleport
- [ ] Nftables
- [ ] Iptables
- [ ] UFW
- [ ] Fail2ban

## 3.2 Vulnerability & Compliance Scanning

- [x] [Lynis](v1.1.0/lynis)
- [x] [Grype](v1.1.0/grype)
- [x] [Syft](v1.1.0/syft)
- [x] [Grant](v1.1.0/grant)
- [ ] OpenSCAP
- [ ] InSpec
- [ ] OpenVAS
- [ ] Nessus
- [ ] Trivy
- [ ] Bandit
- [ ] Checkov
- [ ] Gitleaks
- [ ] Betterleaks
- [ ] ScoutSuite

## 3.3 Monitoring, Detection & Response

- [ ] MISP
- [ ] TheHive
- [ ] Suricata
- [ ] Graylog
- [ ] SOC environment — Wazuh
- [ ] SOAR environment — Shuffle

## 3.4 Secrets & Infrastructure Management

- [ ] HashiCorp Vault
- [ ] Aikido Safe-chain
- [ ] Fleet
- [ ] GLPI
- [ ] Jenkins
- [ ] OWASP Dependency-Track

## 3.5 Operating System & Red Teaming

- [ ] NixOS — based on [Sécurix](https://github.com/cloud-gouv/securix)
- [ ] Red Teaming Environment — required tools (TBD)
