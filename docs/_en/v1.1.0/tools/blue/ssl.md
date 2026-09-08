---
layout: default
title: SSL
parent: Tools
permalink: /en/v1.1.0/ssl
---

# SSL

## Introduction

SSL is a set of tools that work together to generate SSL certificates. These include `certbot`, `python3-certbot-dns-digitalocean`, `python3-certbot-dns-ovh`, and `python3-certbot-dns-cloudflare`. This role can also generate self-signed certificates using `OpenSSL`.

{: .warning }
This role creates the `ssl-cert` group so services can access their private keys. If you use this role alongside other role-managed services (for example, PostgreSQL), make sure the relevant service user is also a member of this group.

## Implementation

When installed via this repository's Ansible role, SSL certificate generation is set up as follows:

1. The required tools are installed based on the selected configuration (DNS-01 challenge or not, self-signed or not).
2. Certbot directories are configured.
3. The `ssl-cert` group is created, so services that need to read private keys can be granted access.
4. Credentials for the DNS provider are stored, if specified.
5. An SSL certificate is generated.
6. A cron job is added to renew the certificate automatically, unless it is self-signed.

## Ansible role usage

```yaml
- hosts: example-host
  become: true
  roles:
    - ssl
  vars:
    # -- DNS-related configuration --#
    ssl_dns: false
    ssl_provider: "cloudflare"
    ssl_credentials:
      token: "token1234"
      secret: "secret1234"
      consumer: "consumer1234"

    # -- Certificate generation --#
    ssl_generate: true
    ssl_move_cert: true
    ssl_move_key: true

    ssl_cert_path: "/etc/ssl/certs/easysec.pem"
    ssl_key_path: "/etc/ssl/private/easysec.key"

    ssl_domain: "easysec.x"
```

Once the playbook has run:

- If certificate generation was enabled, the certificate will be available at the specified output paths.
- Renewal works the same way as generation: the newly generated certificate is sent to the same configured paths.

### Properties

#### Configuration

- `ssl_dns` (boolean, optional): Whether the certificate should be generated via a DNS-01 challenge. Default: `false`.
- `ssl_provider` (enum, optional): The provider used to generate the certificate. Available options:
  - `ovh` — requires `ssl_credentials`. [Documentation](https://certbot-dns-ovh.readthedocs.io/en/stable/).
  - `digitalocean` — requires `ssl_credentials`. [Documentation](https://certbot-dns-digitalocean.readthedocs.io/en/stable/).
  - `cloudflare` — requires `ssl_credentials`. [Documentation](https://certbot-dns-cloudflare.readthedocs.io/en/stable/).
  - `selfsigned` — no credentials required.
- `ssl_credentials` (dict, optional): Credentials used for the selected provider. Required fields:
  - `token` (string) — required for the `ovh`, `digitalocean`, and `cloudflare` providers.
  - `secret` (string) — required for the `ovh` provider.
  - `consumer` (string) — required for the `ovh` provider.

#### Generation

- `ssl_generate` (boolean, optional): Whether the role should generate a certificate. Default: `true`.
- `ssl_domain` (string, optional): The domain name to generate the certificate for. Default: `easysec.x`.
- `ssl_move_cert` (boolean, optional): Whether the generated certificate should be moved to a specific location. Default: `false`.
- `ssl_move_key` (boolean, optional): Whether the generated key should be moved to a specific location. Default: `false`.
- `ssl_move_csr` (boolean, optional): Whether the generated CSR should be moved to a specific location. Default: `false`.
- `ssl_cert_path` (string, optional): Destination path for the generated certificate. Default: `/tmp/{{ ssl_domain }}.crt`.
- `ssl_key_path` (string, optional): Destination path for the generated key. Default: `/tmp/{{ ssl_domain }}.key`.
- `ssl_csr_path` (string, optional): Destination path for the generated CSR. Default: `/tmp/{{ ssl_domain }}.csr`.
- `ssl_csr_config` (dict, optional): Information required to generate a valid CSR. Fields:
  - `country` (string): Country of the CA. Default: `ES`.
  - `organization_name` (string): Organization name of the CA. Default: `EasySec`.
  - `unit_name` (string): Unit name of the CA. Default: `Security`.
- `ssl_email` (string, optional): Contact email used during certificate generation. Default: `whoami@easysec.x`.
- `ssl_new_owner` (string, optional): New owner to set on the certificate/key if moved. Defaults to the role's configured owner.
- `ssl_new_group` (string, optional): New group to set on the certificate/key if moved. Defaults to the role's configured group.

## Test suite

{: .warning }
This role has only been tested with the `selfsigned` provider. Since no domain is currently used for this project, the other provider options have not been tested.

This role has been tested with the following host configurations:

### Target hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Manager hosts

- Ubuntu Server 22.04 (Jammy Jellyfish)
