---
layout: default
title: Grant
parent: Herramientas
permalink: /es/v1.1.0/grant
---

# Grant

## Introducción

Grant es una herramienta instalable utilizada para realizar el escaneo de licencias de las dependencias. Pertenece a la sección `Blue Team`.

## Implementación

Cuando se instala mediante el rol de Ansible de este repositorio, Grant se configura de la siguiente forma:

1. Grant se instala y configura en el host especificado.
2. Se crea un archivo de configuración en `/etc/grant/config.yaml` con los parámetros de análisis.
3. La variable de entorno `GRANT_CONFIG` se define a nivel de sistema, apuntando a dicho archivo de configuración.
4. Opcionalmente, se puede configurar un cron job para ejecutar escaneos automáticamente de forma programada.

## Uso del rol en Ansible

```yaml
- hosts: example-host
  become: true
  roles:
    - grant
  vars:
    grant_package_name: grant
    grant_group: grant
    grant_user: grant
    grant_time:
      weekday: "0"
      hour: "3"
      minute: "0"
```

### Propiedades

- `grant_package_name` (string, opcional): Nombre del paquete a instalar (por defecto: `grant`)
- `grant_user` (string, opcional): Nombre del usuario que puede ejecutar el binario y acceder a los informes/logs (por defecto: `grant`)
- `grant_group` (string, opcional): Nombre del grupo que puede ejecutar el binario y acceder a los informes/logs (por defecto: `grant`)
- `grant_time` (diccionario, opcional): Si está presente, se programa un cron job a la hora especificada. Por defecto: `weekday: "0"`, `hour: "3"`, `minute: "0"` (todos los domingos a las 3 AM). Campos disponibles:

```yaml
month: "0"
day: "0"
weekday: "0"
hour: "0"
minute: "0"
```

## Uso desde línea de comandos

Una vez instalado, Grant puede ejecutarse directamente en el host:

```bash
grant list <target>
```

El informe se imprime en la salida estándar. Algunos ejemplos de uso:

```bash
grant list .                      # Scans the current directory
grant list ubuntu:22.04           # Scans a container image
grant list sbom:./sbom.json       # Scans an existing SBOM
```

## Suite de pruebas

Este rol ha sido probado con las siguientes configuraciones de host:

### Hosts de destino

- Ubuntu Server 22.04 (Jammy Jellyfish)
- Ubuntu Server 24.04 (Noble Numbat)

### Hosts gestores

- Ubuntu Server 22.04 (Jammy Jellyfish)
