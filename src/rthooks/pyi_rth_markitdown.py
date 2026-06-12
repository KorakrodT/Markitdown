# rthooks/pyi_rth_markitdown.py
# Runtime hook — force-import markitdown + magika at .exe startup
# This runs BEFORE markitdown_gui.py so MARKITDOWN_OK is set correctly.

def _force_imports():
    try:
        import magika
        from magika import Magika
    except Exception:
        pass

    try:
        import onnxruntime
    except Exception:
        pass

    try:
        import numpy
    except Exception:
        pass

    try:
        import markitdown
        from markitdown import MarkItDown
    except Exception:
        pass

    try:
        import markitdown.converters
        import markitdown.converters._pdf_converter
        import markitdown.converters._docx_converter
        import markitdown.converters._pptx_converter
        import markitdown.converters._xlsx_converter
        import markitdown.converters._html_converter
        import markitdown.converters._image_converter
        import markitdown.converters._csv_converter
        import markitdown.converters._xml_converter
        import markitdown.converters._zip_converter
    except Exception:
        pass

_force_imports()
