# -*- mode: python ; coding: utf-8 -*-
# macOS-specific build configuration

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
    [],
    exclude_binaries=True,
    name='assignment-tracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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
    name='assignment-tracker',
)

app = BUNDLE(
    coll,
    name='Assignment Tracker.app',
    icon=None,
    bundle_identifier='com.yourcompany.assignmenttracker',
    info_plist={
        'CFBundleDisplayName': 'Assignment Tracker',
        'CFBundleGetInfoString': 'Assignment Tracker App',
        'CFBundleIdentifier': 'com.yourcompany.assignmenttracker',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundleName': 'Assignment Tracker',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
    },
)
