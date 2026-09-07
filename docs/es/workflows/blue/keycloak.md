---
layout: default
title: Keycloak
parent: Workflows
grand_parent: Español
---

# Keycloak

## Introducción

Keycloak es una plataforma de código abierto de gestión de identidades y accesos (IAM, por sus siglas en inglés). Con este software, se pueden declarar identidades y vincularlas a múltiples servicios diferentes (Google, Microsoft...) para centralizar las identidades.</br>
Esta herramienta pertenece a la sección «Blue Team».</br>
Este flujo de trabajo también incluye las siguientes herramientas:

- [PostgreSQL](../../tools/blue/postgresql.md)

## Implementación

La implementación de este flujo de trabajo en Ansible es la siguiente:

1. Instala y configura PostgreSQL en el host especificado.
2. Descarga y configura Keycloak.
3. Genera certificados SSL.
4. Crea un usuario predeterminado (y temporal) para gestionar la instancia. Las credenciales generadas se pueden encontrar [aquí](../../../../generated/keycloak_admin.txt).

## Uso

1. Ejecuta el playbook (las instrucciones se pueden encontrar [aquí](../../../../workflows/keycloak.yml)).
2. Tras la instalación y la configuración, accede a https[://]tu_dominio:8443 para interactuar con Keycloak.
