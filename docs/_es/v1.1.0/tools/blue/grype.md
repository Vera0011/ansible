---
layout: default
title: Grype
parent: Herramientas
permalink: /es/v1.1.0/grype
---

# Grype

## Introducción

Grype es una herramienta instalable utilizada para realizar escaneos de vulnerabilidades en imágenes de contenedor, sistemas de archivos y directorios, identificando CVEs en las dependencias del sistema. Pertenece a la sección `Blue Team`.

## Implementación

Cuando se instala mediante el rol de Ansible de este repositorio, Grype se configura de la siguiente forma:

1. Grype se instala y configura en el host especificado.
2. Se crea un archivo de configuración en `/etc/grype/config.yaml` con los parámetros de análisis.
3. La variable de entorno `GRYPE_CONFIG` se define a nivel de sistema, apuntando a dicho archivo de configuración.
4. Opcionalmente, se puede configurar un cron job para ejecutar escaneos automáticamente de forma programada.

## Uso del rol en Ansible

```yaml
- hosts: example-host
  become: true
  roles:
    - grype
  vars:
    grype_package_name: grype
    grype_group: grype
    grype_user: grype
    grype_time:
      weekday: "0"
      hour: "3"
      minute: "0"
```

### Propiedades

- `grype_package_name` (string, opcional): Nombre del paquete a instalar (por defecto: `grype`)
- `grype_user` (string, opcional): Nombre del usuario que puede ejecutar el binario y acceder a los informes/logs (por defecto: `grype`)
- `grype_group` (string, opcional): Nombre del grupo que puede ejecutar el binario y acceder a los informes/logs (por defecto: `grype`)
- `grype_time` (diccionario, opcional): Si está presente, se programa un cron job a la hora especificada. Por defecto: `weekday: "0"`, `hour: "3"`, `minute: "0"` (todos los domingos a las 3 AM). Campos disponibles:

```yaml
month: "0"
day: "0"
weekday: "0"
hour: "0"
minute: "0"
```

## Uso desde línea de comandos

Una vez instalado, Grype puede ejecutarse directamente en el host:

```bash
grype <target>
```

El informe se imprime en la salida estándar. Algunos ejemplos de uso:

```bash
grype .                      # Scans the current directory
grype ubuntu:22.04           # Scans a container image
grype sbom:./sbom.json       # Scans an existing SBOM
```

## Suite de pruebas

Este rol ha sido probado con las siguientes configuraciones de host:

### Hosts de destino

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Hosts gestores

- Ubuntu Server 22.04 (Jammy Jellyfish)
