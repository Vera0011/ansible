---
layout: default
title: Proxychains
parent: Herramientas
grand_parent: v1.1.0
permalink: /es/v1.1.0/proxychains
---

# Proxychains

## Introducción

Proxychains es un paquete disponible en distribuciones de Linux (Ubuntu, Kali Linux, etc.). Se utiliza para enrutar el tráfico a través de múltiples máquinas y así enmascarar el tráfico propio. Pertenece a la sección `Red Team`.

## Implementación

Cuando se instala mediante el rol de Ansible de este repositorio, Proxychains se configura de la siguiente forma:

1. Se crean múltiples proxies autoalojados utilizando Tor, cada uno ejecutándose como su propia unidad de servicio.
2. Antes de crear nuevos servicios de Tor, se eliminan los servicios de Tor personalizados ya existentes creados por este rol. A continuación, se crea un nuevo servicio utilizando una plantilla de unidad de sistema compartida y una configuración específica para cada instancia.
3. Proxychains se configura para utilizar estas instancias de Tor, mediante un método round-robin.
4. Una vez configurado, el tráfico generado a través de Proxychains se redirige a través de estos servicios de Tor.

## Uso del rol en Ansible

```yaml
- hosts: example-host
  become: true
  roles:
    - proxychains
  vars:
    proxychains_clean: false
    proxychains_total_proxies: 10
```

### Propiedades

- `proxychains_clean` (booleano, opcional): Indica si el rol debe ejecutarse en modo de limpieza, eliminando todos los proxies existentes en lugar de crear otros nuevos.
- `proxychains_total_proxies` (int, opcional): Número de proxies a configurar.

## Uso desde línea de comandos

Una vez instalado, Proxychains puede ejecutarse directamente en el host:

```bash
proxychains -q <service>
proxychains4 -q <service>
```

El tráfico generado por `<service>` se redirigirá a través de las instancias de Tor configuradas. Ten en cuenta que `<service>` se refiere a una aplicación (como `firefox`) o a un comando (como `nmap` o `dirsearch`).

## Suite de pruebas

Este rol ha sido probado con las siguientes configuraciones de host:

### Hosts de destino

- Kali Linux — Rolling

### Hosts gestores

- Ubuntu Server 22.04 (Jammy Jellyfish)
