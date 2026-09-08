#!/bin/bash

#rm -rf build dist *.spec                                                                                                                                                                                               ✖ ✹ ✭feature/python_cli 

uv run pyinstaller \
    --name easysec-1.2.0 \
    --onefile \
    --console \
    --add-data "playbooks:playbooks" \
    --add-data "roles:playbooks/roles" \
    --add-data "inventory:inventory" \
    --add-data "ansible.cfg:." \
    --add-binary ".venv/bin/ansible-playbook:ansible/bin" \
    --collect-all ansible \
    --collect-data ansible_collections \
    --collect-submodules ansible_collections \
    --collect-submodules ansible.plugins \
    --collect-submodules ansible.modules \
    cli/main.py
