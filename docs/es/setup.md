---
layout: default
title: Setup
nav_order: 4
permalink: /es/setup
parent: Español
---

# Configuración
Hay dos scripts disponibles en [`scripts/`](../../scripts/):
- **execute.sh**: Interfaz de línea de comandos interactiva para seleccionar y ejecutar módulos o workflows
- **populate.sh**: Añade hosts a los inventarios de forma manual o automática (producción y staging)

## Entorno
La configuración recomendada utiliza [UV](https://github.com/astral-sh/uv) para la gestión del entorno de Python. Estas son las acciones recomendadas:
```bash
uv python pin                       # Utiliza el archivo .python-version y selecciona la versión específica del intérprete
uv venv .venv                       # Crea el entorno virtual
source .venv/bin/activate           # Activa el entorno virtual
uv pip install -r requirements.txt  # Instala las dependencias necesarias
```

## Ejecución
El script se puede ejecutar (desde la ruta raíz del proyecto) con:
```bash
./scripts/execute.sh
```

{: .note }
Asegúrate de que Vagrant y VirtualBox estén instalados y en ejecución antes de ejecutar cualquier script (si vas a trabajar solamente con Vagrant)