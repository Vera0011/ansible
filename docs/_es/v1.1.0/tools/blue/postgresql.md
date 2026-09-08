---
layout: default
title: PostgreSQL
parent: Herramientas
permalink: /es/v1.1.0/postgresql
---

# PostgreSQL

## Introducción

PostgreSQL es un sistema de base de datos relacional utilizado para almacenar información y datos, gestionado mediante SQL. Pertenece a la sección `Blue Team`.

La versión de PostgreSQL implementada por este rol es **v18**.

{: .warning }
Este rol modifica parámetros de `sysctl` para configurar `hugepages` y protección frente a terminaciones por OOM (falta de memoria). Ten cuidado al instalar en un sistema que ya sobrescriba estos valores, ya que podrían modificarse.

{: .warning }
Este rol **no** gestiona SSL. Asegúrate de ejecutar el rol de SSL antes de utilizar este rol.

## Implementación

Cuando se instala mediante el rol de Ansible de este repositorio, PostgreSQL se configura de la siguiente forma:

1. PostgreSQL se instala y configura en el host especificado.
2. Se utiliza un usuario y grupo dedicados para ejecutar PostgreSQL. Estos se configuran automáticamente como parte de la instalación del paquete.
3. Se pueden habilitar varios módulos opcionales:
   - **Creación de usuarios**
   - **Creación de bases de datos**
   - **Autenticación OAuth** (previsto para futuras implementaciones; no está activo actualmente)
   - **Configuración de WAL y replicación**
4. Si se crean usuarios, sus credenciales se escriben en un archivo generado (ver [Propiedades](#propiedades) más abajo).

## Uso del rol en Ansible

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

Una vez ejecutado el playbook, la base de datos quedará instalada, configurada y lista para usarse.

### Propiedades

- `postgresql_port` (int, opcional): Puerto en el que escucha el servidor. Por defecto: `5432`.
- `postgresql_address` (string, opcional): Dirección en la que escucha el servidor. Por defecto: `'*'` (todas las direcciones).
- `postgresql_user_enable` (booleano, opcional): Indica si el rol debe crear usuarios. Si es `true`, configura `postgresql_users` en consecuencia. Por defecto: `true`.
- `postgresql_database_enable` (booleano, opcional): Indica si el rol debe crear bases de datos. Si es `true`, configura `postgresql_databases` en consecuencia. Por defecto: `true`.
- `postgresql_oauth_enable` (booleano, opcional): Indica si el rol debe configurar conexiones OAuth. Si es `true`, configura las variables `postgresql_oauth_*` en consecuencia. Por defecto: `false`.
- `postgresql_wal_enable` (booleano, opcional): Indica si el rol debe configurar WAL y replicación. Si es `true`, configura las variables `postgresql_wal_*` en consecuencia. Por defecto: `false`.

- `postgresql_users` (lista de dicts, opcional): Usuarios a crear. Campos disponibles:
  - `name` (string): Nombre del usuario.
  - `password` (string): Contraseña en texto claro. Si se deja vacía, se genera una contraseña automáticamente y se muestra en los logs de Ansible.
  - `superuser` (booleano): Indica si el usuario debe ser superusuario. Si es `false`, el usuario se crea con `NOSUPERUSER, NOCREATEDB, NOCREATEROLE`.

- `postgresql_databases` (lista de dicts, opcional): Bases de datos a crear. Campos disponibles:
  - `name` (string): Nombre de la base de datos.
  - `owner` (string): Propietario de la base de datos (debe coincidir con el nombre de un usuario existente).
  - `encoding` (string): Codificación de caracteres. Normalmente debería ser `UTF-8`.

{: .warning }
El módulo de OAuth solo está disponible en PostgreSQL `18+`.

- `postgresql_oauth_provider` (string, opcional): Nombre del proveedor OAuth. Por defecto: `kc_validator`.
- `postgresql_oauth_endpoint` (string, opcional): URL del endpoint de tokens del proveedor. Por defecto: `https://<keycloak>/realms/<realm>/protocol/openid-connect/token`.
- `postgresql_oauth_audience` (string, opcional): Nombre de audiencia del proveedor. Por defecto: `postgres-resource`.
- `postgresql_oauth_resource_name` (string, opcional): Nombre del recurso del proveedor. Por defecto: `appdb`.
- `postgresql_oauth_client_id` (string, opcional): ID de cliente del proveedor. Por defecto: `postgres-resource`.
- `postgresql_oauth_http_timeout` (int, opcional): Tiempo de espera HTTP, en milisegundos. Por defecto: `2000`.
- `postgresql_oauth_issuer` (string, opcional): URL del realm/emisor. Por defecto: `https://<keycloak>/realms/<realm>`.

- `postgresql_wal_level` (string, opcional): Nivel de replicación. Consulta la [documentación de WAL de PostgreSQL](https://www.postgresql.org/docs/18/runtime-config-wal.html) para ver las opciones disponibles. Por defecto: `replica`.
- `postgresql_wal_max_size` (string, opcional): Tamaño máximo que puede alcanzar el WAL durante los checkpoints. Consulta la [documentación de WAL de PostgreSQL](https://www.postgresql.org/docs/18/runtime-config-wal.html). Por defecto: `1GB`.
- `postgresql_wal_min_size` (string, opcional): Espacio mínimo en disco reservado para los archivos WAL. Consulta la [documentación de WAL de PostgreSQL](https://www.postgresql.org/docs/18/runtime-config-wal.html). Por defecto: `80MB`.
- `postgresql_wal_max_senders` (int, opcional): Número máximo de conexiones concurrentes desde servidores en espera (standby). Consulta la [documentación de replicación de PostgreSQL](https://www.postgresql.org/docs/18/runtime-config-replication.html). Por defecto: `10`.
- `postgresql_wal_max_replicas` (int, opcional): Número máximo de slots de replicación. Consulta la [documentación de replicación de PostgreSQL](https://www.postgresql.org/docs/18/runtime-config-replication.html). Por defecto: `10`.

- `postgresql_hba_entries` (lista de dicts, opcional): Entradas escritas en `pg_hba.conf`. Campos disponibles:
  - `type` (string): Tipo de conexión (`local`, `hostssl`, `host`).
  - `database` (string): Nombre de la base de datos, o `all`.
  - `user` (string): Nombre de usuario específico, o `all`.
  - `address` (string): Dirección IP específica, o `""`.
  - `method` (string): Método de autenticación (`peer`, `reject`, `scram-sha-256`).

{: .note }
Si se utiliza `postgresql_users`, las credenciales generadas se escriben en `generated/postgresql_users.txt`.

## Suite de pruebas

{: .warning }
Este rol solo ha sido probado como instancia de un único nodo, sin OAuth. El módulo de OAuth se incluye para futuras implementaciones y no está activo actualmente.

Este rol ha sido probado con las siguientes configuraciones de host:

### Hosts de destino

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Hosts gestores

- Ubuntu Server 22.04 (Jammy Jellyfish)
