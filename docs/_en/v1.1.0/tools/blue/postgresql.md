---
layout: default
title: PostgreSQL
parent: Tools
permalink: /en/v1.1.0/postgresql
---

# PostgreSQL

## Introduction

PostgreSQL is a relational database system used to store information and data, managed using SQL. It belongs to the `Blue Team` section.

The version of PostgreSQL implemented by this role is **v18**.

{: .warning }
This role modifies `sysctl` parameters to configure `hugepages` and protection against OOM (out-of-memory) kills. Be careful when installing on a system that already overrides these values, as they may be changed.

{: .warning }
This role does **not** handle SSL. Make sure to run the SSL role before using this role.

## Implementation

When installed via this repository's Ansible role, PostgreSQL is set up as follows:

1. PostgreSQL is installed and configured on the specified host.
2. A dedicated user and group are used to run PostgreSQL. These are configured automatically as part of package installation.
3. Several optional modules can be enabled:
   - **User creation**
   - **Database creation**
   - **OAuth authentication** (planned for future implementations; not currently active)
   - **WAL and replication configuration**
4. If users are created, their credentials are written to a generated file (see [Properties](#properties) below).

## Ansible role usage

```yaml
- hosts: example-host
  become: true
  roles:
    - postgresql
  vars:
    postgresql_port: 5432
    postgresql_address: "'*'"

    postgresql_user_enable: true
    postgresql_database_enable: true
    postgresql_oauth_enable: false
    postgresql_wal_enable: false

    postgresql_users:
      - { name: "easysec", password: "", superuser: true }
      - { name: "manager-easysec", password: "", superuser: false }

    postgresql_databases:
      - { name: "easysec", owner: "manager-easysec", encoding: "UTF-8" }

    postgresql_oauth_provider: kc_validator
    postgresql_oauth_endpoint: https://<keycloak>/realms/<realm>/protocol/openid-connect/token
    postgresql_oauth_audience: postgres-resource
    postgresql_oauth_resource_name: appdb
    postgresql_oauth_client_id: postgres-resource
    postgresql_oauth_http_timeout: 2000
    postgresql_oauth_issuer: https://<keycloak>/realms/<realm>

    postgresql_wal_level: "replica"
    postgresql_wal_max_size: "1GB"
    postgresql_wal_min_size: "80MB"
    postgresql_wal_max_senders: 10
    postgresql_wal_max_replicas: 10

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
          database: "all",
          user: "all",
          address: "0.0.0.0/0",
          method: "scram-sha-256",
        }
      - {
          type: "host",
          database: "all",
          user: "all",
          address: "0.0.0.0/0",
          method: "reject",
        }
```

Once the playbook has run, the database will be installed, configured, and ready to use.

### Properties

- `postgresql_port` (int, optional): Port the server listens on. Default: `5432`.
- `postgresql_address` (string, optional): Address the server listens on. Default: `'*'` (all addresses).
- `postgresql_user_enable` (boolean, optional): Whether the role should create users. If `true`, configure `postgresql_users` accordingly. Default: `true`.
- `postgresql_database_enable` (boolean, optional): Whether the role should create databases. If `true`, configure `postgresql_databases` accordingly. Default: `true`.
- `postgresql_oauth_enable` (boolean, optional): Whether the role should configure OAuth connections. If `true`, configure the `postgresql_oauth_*` variables accordingly. Default: `false`.
- `postgresql_wal_enable` (boolean, optional): Whether the role should configure WAL and replication. If `true`, configure the `postgresql_wal_*` variables accordingly. Default: `false`.

- `postgresql_users` (list of dicts, optional): Users to be created. Available fields:
  - `name` (string): Name of the user.
  - `password` (string): Password in clear text. If left empty, a password is auto-generated and shown in the Ansible logs.
  - `superuser` (boolean): Whether the user should be a superuser. If `false`, the user is created with `NOSUPERUSER, NOCREATEDB, NOCREATEROLE`.

- `postgresql_databases` (list of dicts, optional): Databases to be created. Available fields:
  - `name` (string): Name of the database.
  - `owner` (string): Owner of the database (must match the name of an existing user).
  - `encoding` (string): Character encoding. This should normally be `UTF-8`.

{: .warning }
The OAuth module is only available in PostgreSQL `18+`.

- `postgresql_oauth_provider` (string, optional): Name of the OAuth provider. Default: `kc_validator`.
- `postgresql_oauth_endpoint` (string, optional): URL of the provider's token endpoint. Default: `https://<keycloak>/realms/<realm>/protocol/openid-connect/token`.
- `postgresql_oauth_audience` (string, optional): Audience name from the provider. Default: `postgres-resource`.
- `postgresql_oauth_resource_name` (string, optional): Resource name from the provider. Default: `appdb`.
- `postgresql_oauth_client_id` (string, optional): Client ID from the provider. Default: `postgres-resource`.
- `postgresql_oauth_http_timeout` (int, optional): HTTP timeout, in milliseconds. Default: `2000`.
- `postgresql_oauth_issuer` (string, optional): URL of the realm/issuer. Default: `https://<keycloak>/realms/<realm>`.

- `postgresql_wal_level` (string, optional): Replication level. See the [PostgreSQL WAL documentation](https://www.postgresql.org/docs/18/runtime-config-wal.html) for available options. Default: `replica`.
- `postgresql_wal_max_size` (string, optional): Maximum size the WAL is allowed to grow to during checkpoints. See the [PostgreSQL WAL documentation](https://www.postgresql.org/docs/18/runtime-config-wal.html). Default: `1GB`.
- `postgresql_wal_min_size` (string, optional): Minimum disk space reserved for WAL files. See the [PostgreSQL WAL documentation](https://www.postgresql.org/docs/18/runtime-config-wal.html). Default: `80MB`.
- `postgresql_wal_max_senders` (int, optional): Maximum number of concurrent connections from standby servers. See the [PostgreSQL replication documentation](https://www.postgresql.org/docs/18/runtime-config-replication.html). Default: `10`.
- `postgresql_wal_max_replicas` (int, optional): Maximum number of replication slots. See the [PostgreSQL replication documentation](https://www.postgresql.org/docs/18/runtime-config-replication.html). Default: `10`.

- `postgresql_hba_entries` (list of dicts, optional): Entries written to `pg_hba.conf`. Available fields:
  - `type` (string): Connection type (`local`, `hostssl`, `host`).
  - `database` (string): Database name, or `all`.
  - `user` (string): Specific user name, or `all`.
  - `address` (string): Specific IP address, or `""`.
  - `method` (string): Authentication method (`peer`, `reject`, `scram-sha-256`).

{: .note }
If `postgresql_users` is used, the generated credentials are written to `generated/postgresql_users.txt`.

## Test suite

{: .warning }
This role has only been tested as a single-node instance, without OAuth. The OAuth module is included for future implementations and is not currently active.

This role has been tested with the following host configurations:

### Target hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Manager hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
