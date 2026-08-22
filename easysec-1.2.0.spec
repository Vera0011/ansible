# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all

datas = [('playbooks', 'playbooks'), ('roles', 'playbooks/roles'), ('inventory', 'inventory'), ('ansible.cfg', '.')]
binaries = [('.venv/bin/ansible-playbook', 'ansible/bin')]
hiddenimports = []
datas += collect_data_files('ansible_collections')
hiddenimports += collect_submodules('ansible_collections')
hiddenimports += collect_submodules('ansible.plugins')
hiddenimports += collect_submodules('ansible.modules')
tmp_ret = collect_all('ansible')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['cli/main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='easysec-1.2.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='easysec-1.2.0',
)
