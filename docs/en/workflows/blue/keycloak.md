---
layout: default
title: Keycloak
parent: Workflows
grand_parent: English
---

# Keycloak

## Introduction

Keycloak is an opensource IAM (Identity Access Managenent) platform. With this software, identities can be declared and linked to multiple different services (Google, Microsoft...) to centralize identities.</br>
This tool belongs to the `Blue Team` section.</br>
This workflow also involves these tools:

- [PostgreSQL](../../tools/blue/postgresql.md)

## Implementation

The implementation of this workflow in Ansible is as follows:

1. Installs and configures PostgreSQL is the specified host.
2. Downloads and configures Keycloak.
3. Generates SSL certificates.
4. Creates a default (and temporary) user to manage the instance. Credentials generated can be found [here](../../../../generated/keycloak_admin.txt).

## Usage

1. Run the playbook (instructions can be found [here](../../../../workflows/keycloak.yml))
2. After the installation and configuration, access to https[://]your_domain:8443 to interact with Keycloak.
