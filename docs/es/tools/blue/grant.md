---
layout: default
title: Grant
parent: Herramientas
grand_parent: Español
---

# Grant

## Introducción

Grant es un software instalable. Se emplea analizar licencias de dependencias usadas. </br>
Esta herramienta pertenece a la sección de `Blue Team`.

## Implementación

La implementación de esta herramienta en Ansible es la siguiente:

1. Se instala y configura Grant en el host especificado
2. Se configura un fichero de configuración en `/etc/grant/config.yaml` con los parámetros de análisis
3. La variable de entorno `GRANT_CONFIG` es configurada a nivel de sistema para referenciar el fichero de configuración

## Uso

1. Ejecución del playbook (las instrucciones pueden ser encontradas [aquí](../../../../roles/grant/README.md))
2. Tras la instalación, se ejecuta el siguiente comando:

```bash
grant list <objetivo>
```

3. El reporte será generado en la salida estándar. Algunos ejemplos de uso:

```bash
grant list .                      # Escanea el directorio actual
grant list ubuntu:22.04           # Escanea una imagen de contenedor
grant list sbom:./sbom.json       # Escanea un SBOM existente
```
