---
layout: default
title: SSL
parent: Herramientas
permalink: /es/v1.1.0/ssl
---

# SSL

## Introducción

SSL es un conjunto de herramientas que trabajan juntas para generar certificados SSL. Estas incluyen `certbot`, `python3-certbot-dns-digitalocean`, `python3-certbot-dns-ovh` y `python3-certbot-dns-cloudflare`. Este rol también puede generar certificados autofirmados utilizando `OpenSSL`.

{: .warning }
Este rol crea el grupo `ssl-cert` para que los servicios puedan acceder a sus claves privadas. Si utilizas este rol junto con otros servicios gestionados por roles (por ejemplo, PostgreSQL), asegúrate de que el usuario del servicio correspondiente también sea miembro de este grupo.

## Implementación

Cuando se instala mediante el rol de Ansible de este repositorio, la generación de certificados SSL se configura de la siguiente forma:

1. Se instalan las herramientas necesarias en función de la configuración seleccionada (con o sin desafío DNS-01, autofirmado o no).
2. Se configuran los directorios de Certbot.
3. Se crea el grupo `ssl-cert`, para que los servicios que necesiten leer claves privadas puedan tener acceso.
4. Se almacenan las credenciales del proveedor DNS, si se han especificado.
5. Se genera un certificado SSL.
6. Se añade un cron job para renovar el certificado automáticamente, salvo que sea autofirmado.

## Uso del rol en Ansible

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

Una vez ejecutado el playbook:

- Si se habilitó la generación de certificados, el certificado estará disponible en las rutas de salida especificadas.
- La renovación funciona igual que la generación: el certificado recién generado se envía a las mismas rutas configuradas.

### Propiedades

#### Configuración

- `ssl_dns` (booleano, opcional): Indica si el certificado debe generarse mediante un desafío DNS-01. Por defecto: `false`.
- `ssl_provider` (enum, opcional): El proveedor utilizado para generar el certificado. Opciones disponibles:
  - `ovh` — requiere `ssl_credentials`. [Documentación](https://certbot-dns-ovh.readthedocs.io/en/stable/).
  - `digitalocean` — requiere `ssl_credentials`. [Documentación](https://certbot-dns-digitalocean.readthedocs.io/en/stable/).
  - `cloudflare` — requiere `ssl_credentials`. [Documentación](https://certbot-dns-cloudflare.readthedocs.io/en/stable/).
  - `selfsigned` — no requiere credenciales.
- `ssl_credentials` (dict, opcional): Credenciales utilizadas para el proveedor seleccionado. Campos requeridos:
  - `token` (string) — requerido para los proveedores `ovh`, `digitalocean` y `cloudflare`.
  - `secret` (string) — requerido para el proveedor `ovh`.
  - `consumer` (string) — requerido para el proveedor `ovh`.

#### Generación

- `ssl_generate` (booleano, opcional): Indica si el rol debe generar un certificado. Por defecto: `true`.
- `ssl_domain` (string, opcional): El nombre de dominio para el que se generará el certificado. Por defecto: `easysec.x`.
- `ssl_move_cert` (booleano, opcional): Indica si el certificado generado debe moverse a una ubicación específica. Por defecto: `false`.
- `ssl_move_key` (booleano, opcional): Indica si la clave generada debe moverse a una ubicación específica. Por defecto: `false`.
- `ssl_move_csr` (booleano, opcional): Indica si el CSR generado debe moverse a una ubicación específica. Por defecto: `false`.
- `ssl_cert_path` (string, opcional): Ruta de destino para el certificado generado. Por defecto: `/tmp/{{ ssl_domain }}.crt`.
- `ssl_key_path` (string, opcional): Ruta de destino para la clave generada. Por defecto: `/tmp/{{ ssl_domain }}.key`.
- `ssl_csr_path` (string, opcional): Ruta de destino para el CSR generado. Por defecto: `/tmp/{{ ssl_domain }}.csr`.
- `ssl_csr_config` (dict, opcional): Información necesaria para generar un CSR válido. Campos:
  - `country` (string): País de la CA. Por defecto: `ES`.
  - `organization_name` (string): Nombre de la organización de la CA. Por defecto: `EasySec`.
  - `unit_name` (string): Nombre de la unidad de la CA. Por defecto: `Security`.
- `ssl_email` (string, opcional): Correo de contacto utilizado durante la generación del certificado. Por defecto: `whoami@easysec.x`.
- `ssl_new_owner` (string, opcional): Nuevo propietario a asignar al certificado/clave si se mueven. Por defecto, el propietario configurado en el rol.
- `ssl_new_group` (string, opcional): Nuevo grupo a asignar al certificado/clave si se mueven. Por defecto, el grupo configurado en el rol.

## Suite de pruebas

{: .warning }
Este rol solo ha sido probado con el proveedor `selfsigned`. Dado que actualmente no se utiliza ningún dominio para este proyecto, las demás opciones de proveedor no han sido probadas.

Este rol ha sido probado con las siguientes configuraciones de host:

### Hosts de destino

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Hosts gestores

- Ubuntu Server 22.04 (Jammy Jellyfish)
