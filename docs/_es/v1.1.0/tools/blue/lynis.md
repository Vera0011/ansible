---
layout: default
title: Lynis
parent: Herramientas
permalink: /es/v1.1.0/lynis
---

# Lynis

## Introducción

Lynis es una herramienta instalable utilizada para realizar auditorías de seguridad del sistema, analizando configuraciones, vulnerabilidades y el estado general de salud del sistema. Pertenece a la sección `Blue Team`.

## Implementación

Cuando se instala mediante el rol de Ansible de este repositorio, Lynis se configura de la siguiente forma:

1. Lynis se instala y configura en el host especificado.
2. Se utiliza un usuario y grupo dedicados para ejecutar Lynis. Si no existen, se crean automáticamente (el usuario creado es de tipo "sistema" y no tiene directorio home).
3. Opcionalmente, se puede configurar un cron job para la generación automática de informes.
4. Los siguientes estándares de cumplimiento están habilitados actualmente:
   - `cis`
   - `iso27001`
   - `pci-dss`
5. No se incluye ninguna licencia, ya que esta configuración utiliza la versión community de Lynis.

## Uso del rol en Ansible

```yaml
- hosts: example-host
  become: true
  roles:
    - lynis
  vars:
    lynis_lang: en
    lynis_user: lynis
    lynis_group: lynis
    lynis_time:
      weekday: "0"
      hour: "3"
      minute: "0"
```

### Propiedades

- `lynis_user` (string, opcional): Nombre del usuario que puede ejecutar el binario y acceder a los informes/logs (por defecto: `lynis`)
- `lynis_group` (string, opcional): Nombre del grupo que puede ejecutar el binario y acceder a los informes/logs (por defecto: `lynis`)
- `lynis_lang` (string, opcional): Idioma del informe generado (por defecto: `en`)
- `lynis_time` (diccionario, opcional): Si está presente, se programa un cron job a la hora especificada. Por defecto: `weekday: "0"`, `hour: "3"`, `minute: "0"` (todos los domingos a las 3 AM). Campos disponibles:

```yaml
month: "0"
day: "0"
weekday: "0"
hour: "0"
minute: "0"
```

## Uso desde línea de comandos

Una vez instalado, Lynis puede ejecutarse directamente en el host:

```bash
lynis audit system
```

El informe se genera y se almacena en `/var/log/lynis/`. Ten en cuenta que ejecutar este comando requiere privilegios de superusuario (`root`), o pertenecer al grupo configurado para Lynis en el playbook.

## Suite de pruebas

Este rol ha sido probado con las siguientes configuraciones de host:

### Hosts de destino

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Hosts gestores

- Ubuntu Server 22.04 (Jammy Jellyfish)
