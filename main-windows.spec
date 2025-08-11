# -*- mode: python ; coding: utf-8 -*-
# Windows-specific build configuration

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('credentials.json', '.'),
        ('.env', '.'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'gspread',
        'google.auth',
        'google.auth.transport.requests',
        'google.oauth2.credentials',
        'dropbox',
        'pandas',
        'dotenv',
    ],
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
    a.binaries,
    a.datas,
    [],
    name='assignment-tracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
