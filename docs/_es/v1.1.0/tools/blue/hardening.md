---
layout: default
title: Hardening
parent: Herramientas
---

# Hardening

## Introducción

Este rol modifica el sistema, implementando configuraciones seguras y reforzando la seguridad de los servicios. </br>
Este rol pertenece a la sección `Blue Team`.

## Implementación

La implementación de este rol en Ansible es la siguiente:

1. En función de las opciones seleccionadas, Ansible realizará cambios en el sistema.
2. Módulos disponibles:

- `GRUB`: Desactiva la recuperación y establece una contraseña maestra para GRUB.
- `CoreDumps`: Desactiva los volcados de memoria (coredumps) en el sistema.
- `Passwords`: Establece una política de gestión de contraseñas, cambia el valor predeterminado de UMASK, activa los logs, bloquea la contraseña de la cuenta root, obliga a utilizar SHA512 para el almacenamiento de contraseñas y aumenta a un límite seguro el número de rondas de hash.
- `Ports`: Desactiva los puertos físicos y lógicos (serie, USB).
- `Protocols`: Desactiva los protocolos de red no utilizados o inseguros.
- `Banners`: Establece un banner personalizado que se muestra al acceder al sistema.
- `Antivirus`: Instala y configura varios programas relacionados con el malware y los virus.
- `Gestión de parches`: Instala y configura varios programas relacionados con la gestión de parches. Habilita las actualizaciones de seguridad automáticas.
- `Particiones`: Traslada secciones críticas (`/home`, `/var`, `/home`) a particiones independientes. Está disponible la opción de crear otras nuevas (y cifrarlas con LUKS).
- `Auditoría`: Instala y configura varios programas relacionados con la auditoría.
- `Servicios`: Aplica unidades de hardening de Systemd y AppArmor a servicios específicos.

## Uso

1. Ejecuta el playbook (puedes encontrar las instrucciones [aquí](../../../../roles/hardening/README.md))
2. Todas las opciones seleccionadas deberían haberse aplicado.
