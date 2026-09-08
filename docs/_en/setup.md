---
layout: default
title: Setup
nav_order: 2
---

# 1. Setup

This repository can be run in **two ways**: with **Ansible directly**, or with the **execution scripts** provided under [`scripts`](https://github.com/Vera0011/easysec/tree/v1.1.0/scripts).

Both methods share the same Python environment setup, but differ in how you trigger the automation:

| Method                                           | Best for                                                                                   |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| Ansible (`ansible-playbook`)                     | Users already familiar with Ansible who want direct control over inventories and playbooks |
| Execution scripts (`execute.sh` / `populate.sh`) | Users who want an interactive, guided workflow without memorizing Ansible commands         |

**Prerequisite:** Install [UV](https://github.com/astral-sh/uv) before starting either path. UV manages the Python interpreter and virtual environment for this project.

---

## 1.1 Ansible

Use this path if you want to invoke Ansible playbooks directly.

### 1.1.1 Environment

Set up the Python environment with UV:

```bash
uv python pin                       # Reads .python-version and pins the required interpreter
uv venv .venv                       # Creates a virtual environment in .venv/
source .venv/bin/activate           # Activates the virtual environment in your current shell
uv pip install -r requirements.txt  # Installs all Python dependencies listed in requirements.txt
```

### 1.1.2 Execution

Run a playbook with `ansible-playbook`, pointing it to your inventory file and the playbook you want to execute. For example, to run the main playbook against the `staging` inventory:

```bash
ansible-playbook -i inventory/staging main.yml
```

Replace `inventory/staging` with the path to your inventory file (e.g. `inventory/production`), and `main.yml` with the path to the playbook you want to run.

---

## 1.2 Execution scripts

Two helper scripts live under [`scripts`](https://github.com/Vera0011/easysec/tree/v1.1.0/scripts):

- **`execute.sh`** — An interactive CLI that lets you pick which module or workflow to run, without needing to know the underlying Ansible commands.
- **`populate.sh`** — Populates the `hosts` section of your inventory (for either `production` or `staging`). It can do this automatically (e.g. by discovering hosts) or let you enter them manually, depending on the option you choose when running it.

### 1.2.1 Environment

Same as the Ansible path — set up the Python environment with UV:

```bash
uv python pin                       # Reads .python-version and pins the required interpreter
uv venv .venv                       # Creates a virtual environment in .venv/
source .venv/bin/activate           # Activates the virtual environment in your current shell
uv pip install -r requirements.txt  # Installs all Python dependencies listed in requirements.txt
```

### 1.2.2 Running

{: .note }
If any part of your workflow uses Vagrant, install Vagrant and VirtualBox and make sure VirtualBox is running **before** launching the script below.

From the project root, run:

```bash
./scripts/execute.sh
```

You'll be prompted to choose the module or workflow you want to execute.
