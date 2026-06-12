# run.pyw — py launcher ใช้ pythonw.exe (ไม่มี console window)
import runpy, os, sys
_d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _d)
runpy.run_path(os.path.join(_d, 'markitdown_gui.py'), run_name='__main__')
