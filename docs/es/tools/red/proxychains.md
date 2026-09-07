---
layout: default
title: Proxychains
parent: Herramientas
grand_parent: Español
permalink: /es/herramientas/proxychains
---

# Proxychains

## Introducción

Proxychains es un paquete disponible en distribuciones del kernel de Linux (Ubuntu, Kali Linux...). Se emplea para desviar el tráfico a través de diversas máquinas para disimular tu tráfico. </br>
Esta herramienta pertenece a la sección de `Red Team`.

## Implementación

La implementación de esta herramienta en Ansible es la siguiente:

1. Se crean múltiples proxies (auto-hosteados, usando unidades de servicio) usando Tor
2. Se configura proxychains para que pueda usarlos
3. EL tráfico generado durante el uso será redirigido a los servicios de Tor.

## Uso

1. Ejecución del playbook (las instrucciones pueden ser encontradas [aquí](../../../../roles/proxychains/README.md))
2. Tras la instalación, se ejecuta el siguiente comando:

```bash
proxychains -q <servicio>
proxychains4 -q <servicio>
```

3. El tráfico será redirigido a través del servicio especificado. Hay que tener en cuenta que "servicio" hace referencia a una aplicación (como puede ser `firefox`) o a comandos (`nmap`, `dirsearch`...)
