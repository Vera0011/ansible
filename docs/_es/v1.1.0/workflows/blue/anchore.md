---
layout: default
title: Anchore
parent: Workflows
permalink: /es/v1.1.0/anchore
---

# Workflow - Anchore

## Introducción

El workflow de Anchore incluye varias herramientas:

- [Syft](../../tools/blue/syft.md)
- [Grype](../../tools/blue/grype.md)
- [Grant](../../tools/blue/grant.md)

Con este workflow (proporcionado por Anchore) se puede escanear un sistema, un contenedor o un proyecto, con las siguientes ventajas:

- Análisis de dependencias
- Análisis de licencias

La implementación actual del workflow solo ejecuta un análisis de todo el sistema (en un cronjob). El workflow completo se encuentra [aquí](../../../../workflows/anchore.yml)

## Organización del workflow

![image](/assets/anchore_workflow.png)

## Cuándo incluir este workflow

- Se puede configurar a nivel de sistema, pero no es muy recomendable, ya que existen programas más específicos para el sistema (como Lynis).
- Es muy útil en pipelines de CI/CD (Jenkins, Bitbucket, Github...).
