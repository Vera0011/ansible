---
layout: default
title: Introducción
nav_order: 2
---

# 1. Introducción

EasySec es un repositorio que contiene roles, documentación y herramientas que ayudan a pequeñas y medianas empresas (PYMEs) a implementar medidas de seguridad en sus propias organizaciones. También da soporte a pruebas de penetración (pentesting) y ejercicios de red teaming.

Este archivo sirve como índice, facilitando la navegación y comprensión de las herramientas y la documentación disponibles.

Todas las herramientas y flujos de trabajo (workflows) de este repositorio son **idempotentes**: ejecutarlos una o varias veces siempre produce el mismo resultado final.

# 2. Organización de la documentación

La documentación está organizada por versión del software. Las nuevas herramientas, flujos de trabajo e instrucciones se documentan bajo la versión en la que fueron introducidas. Salvo que se indique lo contrario, cada nueva versión también incluye todas las herramientas de versiones anteriores, por lo que no es necesario consultar la documentación de versiones antiguas para encontrar algo que aún esté en uso.

# 3. Hoja de ruta

La siguiente lista recoge las herramientas y entornos previstos para el proyecto. Los elementos marcados ya están implementados; los no marcados están planificados, sin un orden de prioridad concreto salvo que se indique lo contrario.

## 3.1 Redes y acceso

- [x] [Proxychains + Tor](/es/v1.1.0/proxychains)
- [x] [Keycloak](/es/v1.1.0/keycloak)
- [ ] Netmaker
- [ ] Pomerium
- [ ] Netbird
- [ ] Teleport
- [ ] Nftables
- [ ] Iptables
- [ ] UFW
- [ ] Fail2ban

## 3.2 Escaneo de vulnerabilidades y cumplimiento

- [x] [Lynis](/es/v1.1.0/lynis)
- [x] [Grype](/es/v1.1.0/grype)
- [x] [Syft](/es/v1.1.0/syft)
- [x] [Grant](/es/v1.1.0/grant)
- [ ] OpenSCAP
- [ ] InSpec
- [ ] OpenVAS
- [ ] Nessus
- [ ] Trivy
- [ ] Bandit
- [ ] Checkov
- [ ] Gitleaks
- [ ] Betterleaks
- [ ] ScoutSuite

## 3.3 Monitorización, detección y respuesta

- [ ] MISP
- [ ] TheHive
- [ ] Suricata
- [ ] Graylog
- [ ] Entorno SOC — Wazuh
- [ ] Entorno SOAR — Shuffle

## 3.4 Gestión de secretos e infraestructura

- [ ] HashiCorp Vault
- [ ] Aikido Safe-chain
- [ ] Fleet
- [ ] GLPI
- [ ] Jenkins
- [ ] OWASP Dependency-Track

## 3.5 Sistema operativo y red teaming

- [ ] NixOS — basado en [Sécurix](https://github.com/cloud-gouv/securix)
- [ ] Entorno de Red Teaming — herramientas necesarias (pendiente de definir)
