# -*- mode: python ; coding: utf-8 -*-
# markitdown_gui.spec  (v2 - fixes magika/onnxruntime bundling)

from PyInstaller.utils.hooks import (
    collect_all, collect_submodules,
    collect_data_files, copy_metadata
)

# ----------------------------------------------------------------
# Collect markitdown + ALL required runtime dependencies
# Root cause: markitdown 0.1.x requires magika, which loads an
# ONNX model (model.onnx) at import time via onnxruntime.
# None of these are auto-detected by PyInstaller static analysis.
# ----------------------------------------------------------------

PACKAGES = [
    # markitdown itself
    'markitdown',
    # markitdown hard deps (per pyproject.toml)
    'magika',              # file-type detection — has ONNX model files!
    'onnxruntime',         # magika's ML runtime — has native DLLs
    'numpy',               # onnxruntime dep
    'markdownify',         # markdown conversion
    'defusedxml',          # safe XML parsing
    'charset_normalizer',  # encoding detection
    'bs4',                 # beautifulsoup4 — HTML parsing
    'requests',            # HTTP
    # requests deps
    'certifi',
    'urllib3',
    'idna',
    # beautifulsoup4 dep
    'soupsieve',
    # markdownify dep
    'six',
    # onnxruntime deps
    'flatbuffers',
    'packaging',
    'sympy',
    'coloredlogs',
    'humanfriendly',
    # Optional: document converters (collected for completeness)
    'pdfminer',
    'lxml',
    'openpyxl',
    'PIL',
    # GUI
    'sv_ttk',
    'tkinterdnd2',
]

all_datas    = []
all_binaries = []
all_hidden   = []

for pkg in PACKAGES:
    try:
        d, b, h = collect_all(pkg)
        all_datas    += d
        all_binaries += b
        all_hidden   += h
        all_hidden   += collect_submodules(pkg)
    except Exception as _e:
        print(f'[spec] WARNING: collect_all({pkg!r}) failed: {_e}')

# Copy .dist-info for packages that read their own metadata at runtime
for pkg in ['markitdown', 'magika', 'onnxruntime', 'numpy']:
    try:
        all_datas += copy_metadata(pkg)
    except Exception:
        pass

# ----------------------------------------------------------------
# Analysis
# ----------------------------------------------------------------
a = Analysis(
    ['markitdown_gui.py'],
    pathex=['.'],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hidden,
    hookspath=['hooks'],
    runtime_hooks=['rthooks/pyi_rth_markitdown.py'],
    excludes=[
        'matplotlib', 'scipy', 'pandas',
        'tkinter.test', '_pytest',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MarkItDown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='MarkItDown',
)
