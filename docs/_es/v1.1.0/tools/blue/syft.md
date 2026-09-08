---
layout: default
title: Syft
parent: Herramientas
permalink: /es/v1.1.0/syft
---

# Syft

## Introducción

Syft es una herramienta instalable utilizada para generar un Inventario de Software (SBOM) a partir de una variedad de objetivos de escaneo. El SBOM resultante puede ser utilizado por herramientas como Grype. Pertenece a la sección `Blue Team`.

## Implementación

Cuando se instala mediante el rol de Ansible de este repositorio, Syft se configura de la siguiente forma:

1. Syft se instala y configura en el host especificado.
2. Se crea un archivo de configuración en `/etc/syft/config.yaml` con los parámetros de análisis.
3. La variable de entorno `SYFT_CONFIG` se define a nivel de sistema, apuntando a dicho archivo de configuración.
4. Opcionalmente, se puede configurar un cron job para generar informes automáticamente de forma programada.

## Uso del rol en Ansible

```yaml
- hosts: example-host
  become: true
  roles:
    - syft
  vars:
    syft_user: syft
    syft_group: syft
    syft_time:
      weekday: "0"
      hour: "3"
      minute: "0"
```

### Propiedades

- `syft_user` (string, opcional): Nombre del usuario que puede ejecutar el binario y acceder a los informes/logs (por defecto: `syft`)
- `syft_group` (string, opcional): Nombre del grupo que puede ejecutar el binario y acceder a los informes/logs (por defecto: `syft`)
- `syft_time` (diccionario, opcional): Si está presente, se programa un cron job a la hora especificada. Por defecto: `weekday: "0"`, `hour: "3"`, `minute: "0"` (todos los domingos a las 3 AM). Campos disponibles:

```yaml
month: "0"
day: "0"
weekday: "0"
hour: "0"
minute: "0"
```

## Uso desde línea de comandos

Una vez instalado, Syft puede ejecutarse directamente en el host:

```bash
syft <target>
```

El informe se imprime en la salida estándar. Algunos ejemplos de uso:

```bash
syft .                      # Scans the current directory
syft ubuntu:22.04           # Scans a container image
```

## Suite de pruebas

Este rol ha sido probado con las siguientes configuraciones de host:

### Hosts de destino

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Hosts gestores

- Ubuntu Server 22.04 (Jammy Jellyfish)
