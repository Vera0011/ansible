---
layout: default
title: Grype
parent: Herramientas
---

# Grype

## Introducción

Grype es un software instalable. Se emplea para realizar análisis de vulnerabilidades en imágenes de contenedores, sistemas de archivos y directorios, identificando CVEs en las dependencias del sistema. </br>
Esta herramienta pertenece a la sección de `Blue Team`.

## Implementación

La implementación de esta herramienta en Ansible es la siguiente:

1. Se instala y configura Grype en el host especificado
2. Se configura un fichero de configuración en `/etc/grype/config.yaml` con los parámetros de análisis
3. La variable de entorno `GRYPE_CONFIG` es configurada a nivel de sistema para referenciar el fichero de configuración

## Uso

1. Ejecución del playbook (las instrucciones pueden ser encontradas [aquí](../../../../roles/grype/README.md))
2. Tras la instalación, se ejecuta el siguiente comando:

```bash
grype <objetivo>
```

3. El reporte será generado en la salida estándar. Algunos ejemplos de uso:

```bash
grype .                      # Escanea el directorio actual
grype ubuntu:22.04           # Escanea una imagen de contenedor
grype sbom:./sbom.json       # Escanea un SBOM existente
```
