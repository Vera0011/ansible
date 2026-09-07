---
layout: default
title: Syft
parent: Herramientas
grand_parent: Español
---

# Syft

## Introducción

Syft es un software instalable. Se emplea para generar un SBOM para una gran variedad de objetivos y puede ser empleado al usarse con herramientas como Grype. </br>
Esta herramienta pertenece a la sección de `Blue Team`.

## Implementación

La implementación de esta herramienta en Ansible es la siguiente:

1. Se instala y configura Syft en el host especificado
2. Se configura un fichero de configuración en `/etc/syft/config.yaml` con los parámetros de análisis
3. La variable de entorno `SYFT_CONFIG` es configurada a nivel de sistema para referenciar el fichero de configuración

## Uso

1. Ejecución del playbook (las instrucciones pueden ser encontradas [aquí](../../../../roles/syft/README.md))
2. Tras la instalación, se ejecuta el siguiente comando:

```bash
syft <objetivo>
```

3. El reporte será generado en la salida estándar. Algunos ejemplos de uso:

```bash
syft .                      # Escanea el directorio actual
syft ubuntu:22.04           # Escanea una imagen de contenedor
```
