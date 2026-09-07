---
layout: default
title: Proxychains
parent: Tools
grand_parent: English
permalink: /en/tools/proxychains
---

# Proxychains
## Introduction
Proxychains is a package available in Linux kernel distributions (Ubuntu, Kali Linux, etc.). It is used to route traffic through multiple machines to mask your traffic. </br>
This tool belongs to the `Red Team` section.

## Implementation
The implementation of this tool in Ansible is as follows:
1. Multiple proxies (self-hosted, using service units) are created using Tor
2. Proxychains is configured to use them
3. Traffic generated during use will be redirected to Tor services.

## Usage
1. Run the playbook (instructions can be found [here](../../../../roles/proxychains/README.md))
2. After installation, run the following command:
```bash
proxychains -q <service>
proxychains4 -q <service>
```
3. Traffic will be redirected through the specified service. Note that “service” refers to an application (such as `firefox`) or to commands (`nmap`, `dirsearch`...)
