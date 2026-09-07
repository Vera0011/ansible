---
layout: default
title: SSL
parent: Tools
grand_parent: English
---

# SSL

## Introduction

SSL is a set of tools that work together to generate SSL certificates. These include: `certbot`, `python3-certbot-dns-digitalocean`, `python3-certbot-dns-ovh` and `python3-certbot-dns-cloudflare`. This role can also generate self-signed certificates using `OpenSSL`.

## Implementation

The implementation of this tool in Ansible is as follows:

1. Tools are installed based on the requirements (using DNS or nor, self-signed or not)
2. Configures certbot directories
3. Creates the group `ssl-cert` for services that require reading private keys.
4. Stores credentials from DNS providers (if specified)
5. Generates an SSL certificate
6. Adds a cronjob to renew the certificate (if it is not self-signed)

## Usage

1. Run the playbook (instructions can be found [here](../../../../roles/ssl/README.md))
2. After installation, if you specified the generation of an SSL certificate, you will have it available at the specified output paths
3. Renewal works the same way as the generation: it sends the new generated certificate to the indicated paths
