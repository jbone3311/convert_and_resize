# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect all data, binaries, and hidden imports for Streamlit
datas = []
binaries = []
hiddenimports = ['streamlit', 'pkg_resources.py2_warn']  # Ensure streamlit and pkg_resources warning module are included

# Collect Streamlit's data, binaries, and hidden imports
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Analysis step to bundle the script with the necessary dependencies
a = Analysis(
    ['convert_and_resizeV2_0.py'],  # Your main script
    pathex=[],  # Add any custom paths if needed
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],  # Custom hooks path if any
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # Exclude unnecessary packages
    noarchive=False,  # Whether to archive the code or not
)

# Package the Python bytecode
pyz = PYZ(a.pure)

# Bundle the executable
exe = EXE(
    pyz,
    a.scripts,  # The scripts to include
    a.binaries,  # The binaries to include
    a.datas,  # The data files to include
    [],
    name='convert_and_resizeV2_0',  # The name of the executable
    debug=False,  # Set to True if you need debugging info
    bootloader_ignore_signals=False,
    strip=False,  # If True, will reduce the size by stripping symbols
    upx=True,  # Compression to reduce size; set to False if it causes issues
    upx_exclude=[],  # Exclude certain binaries from UPX compression
    runtime_tmpdir=None,  # Temporary directory
    console=True,  # Set to False if you don't want the console to appear
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
