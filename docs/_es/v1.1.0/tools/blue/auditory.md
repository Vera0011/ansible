---
layout: default
title: Auditory
parent: Herramientas
permalink: /es/v1.1.0/auditory
---

# Auditory

## Introducción

Este rol ejecuta un conjunto de herramientas de auditoría de seguridad en el host de destino, recopila sus informes y envía los resultados de vuelta al controlador. Este rol pertenece a la sección `Blue Team`.

Las siguientes herramientas se ejecutan, en orden, con el propósito descrito:

- **[Lynis](/es/v1.1.0/lynis)** — Escanea el host e informa de las medidas de hardening recomendadas que faltan actualmente.
- **[Syft](/es/v1.1.0/syft)** — Genera un Inventario de Software (SBOM) del host.
- **[Grype](/es/v1.1.0/grype)** — Escanea el SBOM generado por Syft en busca de vulnerabilidades conocidas.
- **[Grant](/es/v1.1.0/grant)** — Comprueba el SBOM generado por Syft en busca de problemas de cumplimiento de licencias.

Este rol **no instala** ninguna herramienta en el host de destino. Todos los binarios residen en el controlador. En cada ejecución, las herramientas necesarias se:

1. Comprimen en el controlador
2. Transfieren al host de destino
3. Ejecutan en el host de destino
4. Eliminan del host de destino una vez finalizada la ejecución

Esto mantiene el host de destino limpio: no queda ninguna herramienta de auditoría instalada tras la finalización del rol.

## Uso

```yaml
- hosts: example-host
  become: true
  roles:
    - audit
```

{: .note }
Este ejemplo utiliza `become: true` porque el rol necesita privilegios elevados para ejecutar herramientas como Lynis, que inspeccionan la configuración a nivel de sistema.

## Suite de pruebas

Este rol ha sido probado con las siguientes configuraciones de host:

### Hosts de destino

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Hosts gestores

- Ubuntu Server 22.04 (Jammy Jellyfish)
