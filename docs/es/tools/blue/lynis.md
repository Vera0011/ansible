---
layout: default
title: Lynis
parent: Herramientas
grand_parent: Español
---

# Lynis

## Introducción

Lynis es un software instalable. Se emplea para realizar auditorías de seguridad del sistema, analizando configuraciones, vulnerabilidades y el estado general del sistema. </br>
Esta herramienta pertenece a la sección de `Blue Team`.

## Implementación

La implementación de esta herramienta en Ansible es la siguiente:

1. Se instala y configura Lynis en el host especificado
2. Se emplea un usuario y grupo dedicado para la ejecución de Lynis. Si no existe, se crean automáticamente (el usuario creado es del tipo "sistema" y no tiene la ruta del home)
3. Se configura (opcionalmente) un cron job para la generación automática de reportes
4. Las normas de cumplimiento activadas actualmente son:
   - `cis`
   - `iso27001`
   - `pci-dss`
5. El script no incluye ninguna licencia, ya que el software instalado es la versión comunitaria

## Uso

1. Ejecución del playbook (las instrucciones pueden ser encontradas [aquí](../../../../roles/lynis/README.md))
2. Tras la instalación, se ejecuta el siguiente comando:

```bash
lynis audit system
```

3. El reporte será generado y almacenado en `/var/log/lynis/`. Hay que tener en cuenta que la ejecución requiere privilegios de superusuario (`root`) o pertenecer al grupo especificado en el playbook.
