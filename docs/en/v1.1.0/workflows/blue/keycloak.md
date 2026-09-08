---
layout: default
title: Keycloak
parent: Workflows
grand_parent: v1.1.0
permalink: /en/v1.1.0/keycloak
---

# Workflow - Keycloak

## Introduction

Keycloak is an open-source Identity and Access Management (IAM) platform. With Keycloak, identities can be declared and linked to multiple external services (Google, Microsoft, etc.) to centralize identity management. It belongs to the `Blue Team` section.

This workflow also relies on:

- [PostgreSQL](/en/v1.1.0/postgresql) — used as the database backend for Keycloak.
- [SSL](/en/v1.1.0/ssl) — used to generate certificates for both PostgreSQL and Keycloak.

## Implementation

This workflow runs in two stages:

1. **Database setup** — installs and configures PostgreSQL on the host, with a self-signed SSL certificate. Two users are created (`easysec`, a superuser; and `keycloak`, a standard user), along with a `keycloak` database owned by the `keycloak` user. Access rules (`pg_hba.conf`) are set to only allow the `keycloak` user to connect to the `keycloak` database over SSL, from `localhost` (IPv4 and IPv6); all other connections are rejected.
2. **Keycloak setup** — installs and configures Keycloak, with its own self-signed SSL certificate. Before installation, the workflow automatically retrieves the auto-generated `keycloak` database password from the credentials file produced during the PostgreSQL step, so no manual password entry is required.

Generated credentials — including the auto-generated PostgreSQL passwords — can be found in [`generated/postgresql_users.txt`](../../../../generated/postgresql_users.txt).

## Ansible workflow usage

{% raw %}

```yaml
- name: Installs PostgreSQL on host
  hosts: vagrant-keycloak-1
  become: true
  roles:
    - ssl
    - postgresql
  vars:
    ssl_provider: selfsigned
    ssl_cert_path: /etc/ssl/certs/postgresql.crt
    ssl_key_path: /etc/ssl/private/postgresql.key
    ssl_generate: true
    ssl_domain: "postgresql.easysec.x"

    postgresql_ssl:
      cert_path: /etc/ssl/certs/postgresql.crt
      key_path: /etc/ssl/private/postgresql.key

    postgresql_users:
      - { name: "easysec", password: "", superuser: true } # Auto-generated password
      - { name: "keycloak", password: "", superuser: false } # Auto-generated password

    postgresql_databases:
      - { name: "keycloak", owner: "keycloak", encoding: "UTF-8" }

    postgresql_hba_entries:
      - {
          type: "local",
          database: "all",
          user: "postgres",
          address: "",
          method: "peer",
        }
      - {
          type: "hostssl",
          database: "keycloak",
          user: "keycloak",
          address: "127.0.0.1/32",
          method: "scram-sha-256",
        }
      - {
          type: "hostssl",
          database: "keycloak",
          user: "keycloak",
          address: "::1/128",
          method: "scram-sha-256",
        }
      - {
          type: "hostssl",
          database: "all",
          user: "all",
          address: "0.0.0.0/0",
          method: "reject",
        }
      - {
          type: "host",
          database: "all",
          user: "all",
          address: "0.0.0.0/0",
          method: "reject",
        }

- name: Installs Keycloak on test host (Vagrant)
  hosts: vagrant-keycloak-1
  become: true
  roles:
    - ssl
    - keycloak
  vars:
    ssl_provider: "selfsigned"
    ssl_domain: "{{ keycloak_hostname }}"
    ssl_cert_path: /etc/ssl/certs/keycloak.pem
    ssl_key_path: /etc/ssl/private/keycloak.key

    keycloak_database_host: localhost
    keycloak_database_port: 5432
    keycloak_database_name: keycloak
    keycloak_database_user: keycloak
  pre_tasks:
    - name: Sets the generated password for Keycloak
      when: keycloak_database_password is not defined
      ansible.builtin.set_fact:
        keycloak_database_password: "{{ (lookup('file', '{{ playbook_dir }}/../generated/postgresql_users.txt') | from_yaml).keycloak }}"
```

{% endraw %}

### Properties

**Database setup (`ssl` + `postgresql` roles)**

- `ssl_provider`: Provider used for certificate generation. Set to `selfsigned` in this workflow.
- `ssl_cert_path` / `ssl_key_path`: Destination paths for the PostgreSQL certificate and key.
- `ssl_generate`: Whether to generate the certificate. Set to `true`.
- `ssl_domain`: Domain used for the certificate. Set to `postgresql.easysec.x`.
- `postgresql_ssl.cert_path` / `postgresql_ssl.key_path`: Certificate and key paths PostgreSQL should use — matches the `ssl_cert_path` / `ssl_key_path` above.
- `postgresql_users`: Creates the `easysec` (superuser) and `keycloak` (standard) users, both with auto-generated passwords.
- `postgresql_databases`: Creates the `keycloak` database, owned by the `keycloak` user.
- `postgresql_hba_entries`: Restricts database access so only the `keycloak` user can connect to the `keycloak` database, over SSL, from localhost; all other connections are rejected.

**Keycloak setup (`ssl` + `keycloak` roles)**

- `ssl_provider`, `ssl_domain`, `ssl_cert_path`, `ssl_key_path`: Same purpose as above, generating a dedicated self-signed certificate for Keycloak. `ssl_domain` is set dynamically via `keycloak_hostname`.
- `keycloak_database_host` / `keycloak_database_port` / `keycloak_database_name` / `keycloak_database_user`: Connection details for the PostgreSQL database set up in the previous play.
- `keycloak_database_password`: Not set manually — a `pre_tasks` step automatically reads the auto-generated `keycloak` user password from `generated/postgresql_users.txt` and uses it, unless a password has already been defined.

For the full list of available properties on each individual role, see [SSL](/en/v1.1.0/ssl), [PostgreSQL](/en/v1.1.0/postgresql), and this documentation.

## Usage

1. Run the workflow.
2. Once installation and configuration are complete, access Keycloak at `https://your_domain:8443`.
