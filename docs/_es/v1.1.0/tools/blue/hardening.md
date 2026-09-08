---
layout: default
title: Hardening
parent: Herramientas
permalink: /es/v1.1.0/hardening
---

# Hardening

## Introducción

Este rol aplica configuraciones seguras y medidas de hardening a un sistema. Pertenece a la sección `Blue Team`.

El rol está **basado en módulos**, por lo que puedes habilitar únicamente los módulos relevantes para tu caso de uso. Cada tarea y bloque incluye anotaciones que hacen referencia a la recomendación de Lynis correspondiente.

{: .warning }
Si no sabes qué cambia un módulo en concreto, no lo habilites. El conjunto de módulos por defecto suele ser suficiente para proporcionar una seguridad base sólida, pero algunas opciones pueden dejarte bloqueado fuera del sistema si se configuran incorrectamente.

## Implementación

Según qué módulos estén habilitados, Ansible aplica los cambios correspondientes al sistema. Módulos disponibles:

- **`hardening_grub`** — Desactiva el modo de recuperación de GRUB y establece una contraseña maestra requerida al iniciar GRUB. Por defecto: `false`.
- **`hardening_coredumps`** — Desactiva todos los core dumps del sistema. Por defecto: `true`.
- **`hardening_passwords`** — Establece una política de expiración de contraseñas, cambia el UMASK por defecto, habilita el registro de `su`, bloquea la contraseña de la cuenta root, fuerza el almacenamiento de contraseñas mediante SHA512, aumenta las rondas de hashing e instala `libpam-passwdqc` y `libpam-pwquality`. Por defecto: `true`.
- **`hardening_ports`** — Desactiva el USB, restringe el acceso a los puertos serie, desactiva otros puertos de acceso físico, y elimina `firewire-core` y `firewire-ohci`. Por defecto: `true`.
- **`hardening_protocols`** — Desactiva los protocolos de red `dccp`, `sctp`, `rds` y `tipc`. Por defecto: `true`.
- **`hardening_banners`** — Establece un banner personalizado en `/etc/issue` y `/etc/issue.net`, mostrado al acceder al sistema. Por defecto: `true`.
- **`hardening_antivirus`** — Instala `rkhunter`, `clamav` y `chkrootkit`. Por defecto: `true`.
- **`hardening_patch_management`** — Instala `debsums`, `unattended-upgrades`, `apt-listchanges` y `apt-show-versions`, y habilita las actualizaciones de seguridad automáticas. Por defecto: `true`.
- **`hardening_partitions`** — Mueve las particiones `/home`, `/var` y `/tmp` a un nuevo disco (preservando los datos existentes; requiere que haya un disco vacío disponible), y crea una partición `/secrets` cifrada con LUKS. Por defecto: `false`.
- **`hardening_auditory`** — Instala AIDE, Sysstat y AuditD, los inicializa y arranca, y añade reglas de auditoría personalizadas (procedentes de Neo23x0). Por defecto: `true`.
- **`hardening_services`** — Aplica hardening de unidades Systemd y AppArmor a servicios específicos. Actualmente, solo el servicio `UFW` recibe este hardening. Por defecto: `true`.

### Consecuencias de una configuración incorrecta

{: .warning }
Los siguientes módulos pueden provocar interrupciones del servicio si se habilitan sin comprender su efecto:

- **Modificación de GRUB** — Perder la contraseña de GRUB te deja completamente bloqueado fuera del sistema; una configuración incorrecta también puede impedir que el sistema arranque.
- **Modificación de particiones** — Es posible perder datos; perder la clave de cifrado te deja sin acceso a la partición cifrada; una configuración incorrecta puede impedir que el sistema monte correctamente.

## Uso

```yaml
- hosts: example-host
  become: true
  roles:
    - hardening
  vars:
    hardening_grub: false
    hardening_coredumps: false
    hardening_passwords: true
    hardening_ports: true
    hardening_protocols: true
    hardening_banners: true
    hardening_antivirus: true
    hardening_patch_management: true
    hardening_partitions: false
    hardening_auditory: true
    hardening_services: true
```

Una vez ejecutado el playbook, todas las opciones seleccionadas se habrán aplicado al host de destino.

## Propiedades

- `hardening_grub` (booleano, opcional): Habilita el módulo de hardening de GRUB. Por defecto: `false`.
- `hardening_coredumps` (booleano, opcional): Habilita el módulo de hardening de core dumps. Por defecto: `true`.
- `hardening_passwords` (booleano, opcional): Habilita el módulo de hardening de contraseñas. Por defecto: `true`.
- `hardening_ports` (booleano, opcional): Habilita el módulo de hardening de puertos (USB y otros medios). Por defecto: `true`.
- `hardening_protocols` (booleano, opcional): Habilita el módulo de hardening de protocolos de red. Por defecto: `true`.
- `hardening_banners` (booleano, opcional): Habilita el módulo de hardening de banners. Por defecto: `true`.
- `hardening_antivirus` (booleano, opcional): Habilita la instalación y configuración del antivirus. Por defecto: `true`.
- `hardening_patch_management` (booleano, opcional): Habilita el módulo de gestión de parches. Por defecto: `true`.
- `hardening_partitions` (booleano, opcional): Habilita el módulo de hardening de particiones. Por defecto: `false`.
- `hardening_auditory` (booleano, opcional): Habilita el módulo de auditoría. Por defecto: `true`.
- `hardening_services` (booleano, opcional): Habilita el módulo de hardening de servicios. Por defecto: `true`.

## Suite de pruebas

Este rol ha sido probado con las siguientes configuraciones de host:

### Hosts de destino

- Ubuntu Server 22.04 (Jammy Jellyfish)

### Hosts gestores

- Ubuntu Server 22.04 (Jammy Jellyfish)
