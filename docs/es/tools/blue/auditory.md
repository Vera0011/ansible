---
layout: default
title: Auditoría
parent: Herramientas
grand_parent: Español
---

# Auditoría

## Introducción

Este rol consiste en la implementación de una serie de herramientas de auditoría las cuales generan un informe para el ejecutor. </br>
Esta función pertenece a la sección `Blue Team`.

## Implementación

La implementación de esta herramienta en Ansible es la siguiente:

1. Los binarios y los archivos de configuración se comprimen en el controlador.
2. El archivo comprimido se envía al host y se descomprime allí.
3. Los binarios se ejecutan en el host.
4. Los informes generados se extraen del host y se almacenan en el controlador.
5. Los archivos y configuraciones generados se eliminan del host.

### Uso

1. Ejecuta el playbook (puedes encontrar las instrucciones [aquí](../../../../roles/audit/README.md)).
2. Los informes generados que se encuentran [aquí](../../../../roles/audit/reports/).
