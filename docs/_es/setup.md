---
layout: default
title: Configuración
nav_order: 2
---

# 1. Configuración

Este repositorio puede ejecutarse de **dos formas**: usando **Ansible directamente**, o con los **scripts de ejecución** disponibles en [`scripts`](https://github.com/Vera0011/easysec/tree/v1.1.0/scripts).

Ambos métodos comparten la misma configuración del entorno de Python, pero se diferencian en cómo se activa la automatización:

| Método                                              | Recomendado para                                                                                   |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Ansible (`ansible-playbook`)                        | Usuarios ya familiarizados con Ansible que quieran control directo sobre inventarios y playbooks   |
| Scripts de ejecución (`execute.sh` / `populate.sh`) | Usuarios que prefieran un flujo de trabajo interactivo y guiado, sin memorizar comandos de Ansible |

**Requisito previo:** Instala [UV](https://github.com/astral-sh/uv) antes de comenzar con cualquiera de las dos opciones. UV gestiona el intérprete de Python y el entorno virtual de este proyecto.

---

## 1.1 Ansible

Usa esta opción si quieres invocar los playbooks de Ansible directamente.

### 1.1.1 Entorno

Configura el entorno de Python con UV:

```bash
uv python pin                       # Lee el archivo .python-version y fija la versión del intérprete requerida
uv venv .venv                       # Crea un entorno virtual en .venv/
source .venv/bin/activate           # Activa el entorno virtual en tu shell actual
uv pip install -r requirements.txt  # Instala todas las dependencias de Python listadas en requirements.txt
```

### 1.1.2 Ejecución

Ejecuta un playbook con `ansible-playbook`, indicando tu archivo de inventario y el playbook que deseas ejecutar. Por ejemplo, para ejecutar el playbook principal contra el inventario `staging`:

```bash
ansible-playbook -i inventory/staging main.yml
```

Sustituye `inventory/staging` por la ruta a tu archivo de inventario (por ejemplo, `inventory/production`), y `main.yml` por la ruta al playbook que quieras ejecutar.

---

## 1.2 Scripts de ejecución

En [`scripts`](https://github.com/Vera0011/easysec/tree/v1.1.0/scripts) hay disponibles dos scripts auxiliares:

- **`execute.sh`** — Una CLI interactiva que permite elegir qué módulo o flujo de trabajo ejecutar, sin necesidad de conocer los comandos de Ansible subyacentes.
- **`populate.sh`** — Rellena la sección `hosts` de tu inventario (ya sea para `production` o `staging`). Puede hacerlo automáticamente (por ejemplo, descubriendo hosts) o permitir introducirlos manualmente, según la opción que elijas al ejecutarlo.

### 1.2.1 Entorno

Igual que en la opción de Ansible: configura el entorno de Python con UV:

```bash
uv python pin                       # Lee el archivo .python-version y fija la versión del intérprete requerida
uv venv .venv                       # Crea un entorno virtual en .venv/
source .venv/bin/activate           # Activa el entorno virtual en tu shell actual
uv pip install -r requirements.txt  # Instala todas las dependencias de Python listadas en requirements.txt
```

### 1.2.2 Ejecución

{: .note }
Si alguna parte de tu flujo de trabajo utiliza Vagrant, instala Vagrant y VirtualBox y asegúrate de que VirtualBox esté en ejecución **antes** de lanzar el script indicado a continuación.

Desde la raíz del proyecto, ejecuta:

```bash
./scripts/execute.sh
```

Se te pedirá que elijas el módulo o flujo de trabajo que deseas ejecutar.
