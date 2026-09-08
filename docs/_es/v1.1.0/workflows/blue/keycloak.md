---
layout: default
title: Keycloak
parent: Workflows
permalink: /es/v1.1.0/keycloak
---

# Flujo de trabajo - Keycloak

## Introducción

Keycloak es una plataforma de gestión de identidad y acceso (IAM) de código abierto. Con Keycloak, se pueden declarar identidades y vincularlas a múltiples servicios externos (Google, Microsoft, etc.) para centralizar la gestión de identidades. Pertenece a la sección `Blue Team`.

Este flujo de trabajo también depende de:

- [PostgreSQL](/es/v1.1.0/postgresql) — utilizado como base de datos para Keycloak.
- [SSL](/es/v1.1.0/ssl) — utilizado para generar certificados tanto para PostgreSQL como para Keycloak.

## Implementación

Este flujo de trabajo se ejecuta en dos etapas:

1. **Configuración de la base de datos** — instala y configura PostgreSQL en el host, con un certificado SSL autofirmado. Se crean dos usuarios (`easysec`, superusuario; y `keycloak`, usuario estándar), junto con una base de datos `keycloak` propiedad del usuario `keycloak`. Las reglas de acceso (`pg_hba.conf`) se configuran para permitir que únicamente el usuario `keycloak` se conecte a la base de datos `keycloak` mediante SSL, desde `localhost` (IPv4 e IPv6); el resto de conexiones se rechazan.
2. **Configuración de Keycloak** — instala y configura Keycloak, con su propio certificado SSL autofirmado. Antes de la instalación, el flujo de trabajo recupera automáticamente la contraseña autogenerada de la base de datos `keycloak` desde el archivo de credenciales generado durante el paso de PostgreSQL, por lo que no es necesario introducir ninguna contraseña manualmente.

Las credenciales generadas — incluidas las contraseñas autogeneradas de PostgreSQL — pueden encontrarse en `generated/postgresql_users.txt`.

## Uso del flujo de trabajo en Ansible

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

### Propiedades

**Configuración de la base de datos (roles `ssl` + `postgresql`)**

- `ssl_provider`: Proveedor utilizado para la generación del certificado. Definido como `selfsigned` en este flujo de trabajo.
- `ssl_cert_path` / `ssl_key_path`: Rutas de destino para el certificado y la clave de PostgreSQL.
- `ssl_generate`: Indica si se debe generar el certificado. Definido como `true`.
- `ssl_domain`: Dominio utilizado para el certificado. Definido como `postgresql.easysec.x`.
- `postgresql_ssl.cert_path` / `postgresql_ssl.key_path`: Rutas del certificado y la clave que debe usar PostgreSQL — coinciden con `ssl_cert_path` / `ssl_key_path` mencionados arriba.
- `postgresql_users`: Crea los usuarios `easysec` (superusuario) y `keycloak` (estándar), ambos con contraseñas autogeneradas.
- `postgresql_databases`: Crea la base de datos `keycloak`, propiedad del usuario `keycloak`.
- `postgresql_hba_entries`: Restringe el acceso a la base de datos de forma que únicamente el usuario `keycloak` pueda conectarse a la base de datos `keycloak`, mediante SSL, desde localhost; el resto de conexiones se rechazan.

**Configuración de Keycloak (roles `ssl` + `keycloak`)**

- `ssl_provider`, `ssl_domain`, `ssl_cert_path`, `ssl_key_path`: Mismo propósito que arriba, generando un certificado autofirmado dedicado para Keycloak. `ssl_domain` se define dinámicamente mediante `keycloak_hostname`.
- `keycloak_database_host` / `keycloak_database_port` / `keycloak_database_name` / `keycloak_database_user`: Datos de conexión a la base de datos PostgreSQL configurada en el play anterior.
- `keycloak_database_password`: No se define manualmente — un paso en `pre_tasks` lee automáticamente la contraseña autogenerada del usuario `keycloak` desde `generated/postgresql_users.txt` y la utiliza, a menos que ya se haya definido una contraseña.

Para consultar la lista completa de propiedades disponibles en cada rol individual, consulta [SSL](/es/v1.1.0/ssl), [PostgreSQL](/es/v1.1.0/postgresql) y esta documentación.

## Uso

1. Ejecuta el flujo de trabajo.
2. Una vez completadas la instalación y la configuración, accede a Keycloak en `https://your_domain:8443`.
