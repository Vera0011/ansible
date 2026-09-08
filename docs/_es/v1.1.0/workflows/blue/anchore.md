---
layout: default
title: Anchore
parent: Workflows
permalink: /es/v1.1.0/anchore
---

# Flujo de trabajo - Anchore

## Introducción

El flujo de trabajo de Anchore combina varias herramientas en un único pipeline de escaneo:

- [Syft](/es/v1.1.0/syft) — genera un SBOM del objetivo.
- [Grype](/es/v1.1.0/grype) — escanea ese SBOM en busca de vulnerabilidades conocidas.
- [Grant](/es/v1.1.0/grant) — escanea ese SBOM en busca de problemas de cumplimiento de licencias.

Utilizando este flujo de trabajo (basado en el conjunto de herramientas [Anchore](https://anchore.com/)), es posible escanear un sistema, contenedor o proyecto para obtener:

- **Análisis de dependencias** — mediante Syft y Grype.
- **Análisis de licencias** — mediante Grant.

La implementación actual ejecuta **únicamente un escaneo a nivel de sistema**, activado de forma programada mediante cron.

## Implementación

Este flujo de trabajo realiza los siguientes pasos:

1. Instala y configura Syft, Grype y Grant en el host especificado, utilizando un usuario, grupo, carpeta de configuración y carpeta de logs compartidos (`anchore`) para las tres herramientas.
2. Syft y Grype se instalan **sin** su propio cron job programado (`syft_time` y `grype_time` se dejan vacíos).
3. Grant se programa (por defecto, cada domingo a las 3 AM) para ejecutar una tarea combinada que:
   - Genera un SBOM actualizado del host con Syft.
   - Escanea ese SBOM en busca de vulnerabilidades con Grype.
   - Comprueba ese SBOM en busca de problemas de cumplimiento de licencias con Grant.
4. La salida de cada paso se añade a la carpeta de logs compartida (`/var/log/anchore` por defecto).

## Organización del flujo de trabajo

![Diagrama del flujo de trabajo de Anchore](../../../../assets/anchore_workflow.png)

## Uso del flujo de trabajo en Ansible

```yaml
- name: Installs the Anchore workflow
  hosts: vagrant-ubuntu-1
  become: true
  roles:
    - syft
    - grype
    - grant
  vars:
    group: anchore
    user: anchore
    config_folder: /etc/anchore
    log_folder: /var/log/anchore

    syft_group: "{{ group }}"
    syft_user: "{{ user }}"
    syft_time: {} # No cron job for Syft; it only runs as part of Grant's scheduled job
    syft_config_folder: "{{ config_folder }}"
    syft_log_folder: "{{ log_folder }}"

    grype_group: "{{ group }}"
    grype_user: "{{ user }}"
    grype_time: {} # No cron job for Grype; it only runs as part of Grant's scheduled job
    grype_config_folder: "{{ config_folder }}"
    grype_log_folder: "{{ log_folder }}"

    grant_group: "{{ group }}"
    grant_user: "{{ user }}"
    grant_time:
      weekday: "0"
      hour: "3"
      minute: "0"
    grant_config_folder: "{{ config_folder }}"
    grant_log_folder: "{{ log_folder }}"
    grant_job_title: "Anchore workflow - EasySec"
    grant_job: > # Chains Syft, Grype, and Grant into a single scheduled job
      {{ syft_binary_path }} -c {{ syft_custom_config_path }} / -o json > {{ syft_log_folder }}/audit-sbom.json 2>&1 &&
      {{ grype_binary_path }} -c {{ grype_custom_config_path }} sbom:{{ syft_log_folder }}/audit-sbom.json >> {{ grype_log_path }} 2>&1 &&
      {{ grant_binary_path }} -c {{ grant_custom_config_path }} check {{ syft_log_folder }}/audit-sbom.json >> {{ grant_log_path }} 2>&1
```

### Propiedades

- `group` (string, opcional): Grupo compartido utilizado para ejecutar Syft, Grype y Grant, y para acceder a sus informes/logs. Por defecto: `anchore`.
- `user` (string, opcional): Usuario compartido utilizado para ejecutar Syft, Grype y Grant, y para acceder a sus informes/logs. Por defecto: `anchore`.
- `config_folder` (string, opcional): Carpeta de configuración compartida utilizada por las tres herramientas. Por defecto: `/etc/anchore`.
- `log_folder` (string, opcional): Carpeta de logs compartida utilizada por las tres herramientas. Por defecto: `/var/log/anchore`.

Las variables específicas de cada herramienta (`syft_*`, `grype_*`, `grant_*`) corresponden a las propiedades documentadas en las páginas individuales de [Syft](/es/v1.1.0/syft), [Grype](/es/v1.1.0/grype) y [Grant](/es/v1.1.0/grant). En este flujo de trabajo, solo Grant está programado: su tarea ejecuta Syft, Grype y Grant en secuencia, de modo que una única entrada de cron produce un escaneo completo de SBOM, vulnerabilidades y licencias.

## Cuándo incluir este flujo de trabajo

- **A nivel de sistema**: posible, pero no especialmente recomendado — existen herramientas más específicas para ese uso, como Lynis, que suelen ser más adecuadas.
- **En pipelines de CI/CD** (Jenkins, Bitbucket, GitHub, etc.): aquí es donde este flujo de trabajo resulta más útil, ya que permite escanear dependencias de proyectos e imágenes de contenedor como parte del proceso de build.
