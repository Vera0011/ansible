---
layout: default
title: PostgreSQL
parent: Herramientas
grand_parent: Español
---

# PostgreSQL

## Introducción

PostgreSQL es una base de dato relacional. Se utiliza para almacenar información y datos mediante el lenguaje SQL.</br>
Esta herramienta pertenece a la sección `Blue Team`.

## Implementación

La implementación de esta herramienta en Ansible es la siguiente:

1. PostgreSQL se instala y configura en el host especificado
2. Se utilizan un usuario y un grupo dedicados para ejecutar PostgreSQL. Se implementan automáticamente al instalar el paquete
3. Hay diferentes módulos que se pueden cargar:
   - Creación de usuarios
   - Creación de bases de datos
   - Implementación de SSL
   - Implementación de OAuth (para futuras implementaciones, no disponible)
   - Implementación de WAL y réplicas
4. Si hay usuarios creados, un archivo es generado (con sus credenciales) [aquí](../../../../generated/postgresql_users.txt).

## Uso

1. Ejecute el playbook (las instrucciones se pueden encontrar [aquí](../../../../roles/postgresql/README.md))
2. Tras la instalación y la configuración, ¡tendrá acceso a la base de datos!
