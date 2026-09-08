---
layout: default
title: SSL
parent: Herramientas
---

# SSL

## Introducción

SSL es un grupo de herramientas que funcionan de manera conjunta para generar certificados SSL. Entre ellas se incluyen: `certbot`, `python3-certbot-dns-digitalocean`, `python3-certbot-dns-ovh` y `python3-certbot-dns-cloudflare`. Este rol también puede generar certificados autofirmados utilizando `OpenSSL`.

## Implementación

La implementación de esta herramienta en Ansible es la siguiente:

1. Se instalan las herramientas según los requisitos (con o sin DNS, autofirmadas o no)
2. Configura los directorios de certbot
3. Crea el grupo `ssl-cert` para los servicios que requiran leer claves privadas.
4. Almacena las credenciales de los proveedores de DNS (si se especifican)
5. Genera un certificado SSL
6. Añade una tarea cron para renovar el certificado (si no es autofirmado)

## Uso

1. Ejecución del playbook (las instrucciones pueden ser encontradas [aquí](../../../../roles/ssl/README.md))
2. Tras la instalación, si ha especificado la generación de un certificado SSL, estará disponible en las rutas especificadas
3. La renovación funciona de la misma manera que la generación: envía el nuevo certificado generado a las rutas indicadas
