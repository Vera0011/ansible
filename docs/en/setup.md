---
layout: default
title: Setup
nav_order: 4
permalink: /en/setup
parent: English
---

# Setup

Two scripts are available under [`scripts/`](../../scripts/):

- **execute.sh**: Interactive CLI to select and run specific modules or workflows
- **populate.sh**: Fills the inventory hosts section automatically or manuall (production or staging)

## Environment

The recommended setup uses [UV](https://github.com/astral-sh/uv) for Python environment management. These are the recommended actions:

```bash
uv python pin                       # Uses the .python-version file and selects the specific interpreter version
uv venv .venv                       # Creates the virtual environment
source .venv/bin/activate           # Activates the virtual environment
uv pip install -r requirements.txt  # Installs required dependencies
```

## Running

The main script can be executed (from the root project path) with:

```bash
./scripts/execute.sh
```

{: .note }
Ensure Vagrant and VirtualBox are installed and running before executing any script (if you will be using Vagrant)
