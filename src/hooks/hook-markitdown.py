# hooks/hook-markitdown.py
# PyInstaller hook for markitdown 0.1.x
# Captures all converters + magika model files + onnxruntime DLLs

from PyInstaller.utils.hooks import collect_all, collect_submodules, copy_metadata

# --- markitdown itself ---
datas, binaries, hiddenimports = collect_all('markitdown')
hiddenimports += collect_submodules('markitdown')

# --- magika: ONNX model files MUST be included ---
try:
    d, b, h = collect_all('magika')
    datas     += d
    binaries  += b
    hiddenimports += h
    hiddenimports += collect_submodules('magika')
except Exception:
    pass

# --- onnxruntime: native DLLs and providers ---
try:
    d, b, h = collect_all('onnxruntime')
    datas     += d
    binaries  += b
    hiddenimports += h
    hiddenimports += collect_submodules('onnxruntime')
except Exception:
    pass

# --- numpy ---
try:
    d, b, h = collect_all('numpy')
    datas     += d
    binaries  += b
    hiddenimports += h
except Exception:
    pass

# --- Other markitdown hard deps ---
for _pkg in ['markdownify', 'defusedxml', 'charset_normalizer', 'bs4',
             'requests', 'certifi', 'urllib3', 'soupsieve', 'six',
             'flatbuffers', 'packaging', 'sympy', 'coloredlogs']:
    try:
        d, b, h = collect_all(_pkg)
        datas     += d
        binaries  += b
        hiddenimports += h
    except Exception:
        pass

# --- dist-info metadata (for importlib.metadata at runtime) ---
for _pkg in ['markitdown', 'magika', 'onnxruntime', 'numpy']:
    try:
        datas += copy_metadata(_pkg)
    except Exception:
        pass

# --- Explicit hidden imports (markitdown internals) ---
hiddenimports += [
    'markitdown',
    'markitdown._markitdown',
    'markitdown._base_converter',
    'markitdown.converters',
    'markitdown.converters._pdf_converter',
    'markitdown.converters._docx_converter',
    'markitdown.converters._pptx_converter',
    'markitdown.converters._xlsx_converter',
    'markitdown.converters._html_converter',
    'markitdown.converters._image_converter',
    'markitdown.converters._audio_converter',
    'markitdown.converters._csv_converter',
    'markitdown.converters._xml_converter',
    'markitdown.converters._zip_converter',
    'markitdown.converters._epub_converter',
    'markitdown.converters._youtube_converter',
    'markitdown.converters._bing_serp_converter',
    'markitdown.converters._wikipedia_converter',
    'markitdown.converters._ipynb_converter',
    'markitdown.converters._rss_converter',
    'markitdown.converters._url_converter',
    # magika internals
    'magika.magika',
    'magika.types',
    'magika.colors',
    'magika.logger',
    # onnxruntime
    'onnxruntime',
    'onnxruntime.capi',
    'onnxruntime.capi._pybind_state',
]
