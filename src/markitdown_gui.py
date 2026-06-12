"""
MarkItDown GUI — Windows 11 style  v1.0.0
Converts PDF, Word, Excel, PowerPoint, Images, Audio, HTML → Markdown
"""

import os
import threading
import traceback
import inspect
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# Debug helper: catch misuse of pack() where a non-widget or positional
# numeric/string arg is being passed. Print stack to stderr for diagnosis.
try:
    _orig_pack = tk.Misc.pack
    def _pack_debug(self, *args, **kwargs):
        try:
            # Detect if any positional arg is an int or purely-numeric string
            for a in args:
                if isinstance(a, int) or (isinstance(a, str) and a.isdigit()):
                    print('[DEBUG] pack called with positional arg:', repr(a), file=sys.stderr)
                    traceback.print_stack(file=sys.stderr)
                    break
            # Also detect pack called on something without widget attributes
            if not hasattr(self, '_w'):
                print('[DEBUG] pack called on non-widget:', repr(self), file=sys.stderr)
                traceback.print_stack(file=sys.stderr)
        except Exception:
            pass
        return _orig_pack(self, *args, **kwargs)
    tk.Misc.pack = _pack_debug
except Exception:
    # Don't fail import if monkeypatching is not possible
    pass

# ── Clipboard ──────────────────────────────────────────────────────────────
def _clipboard_write(text: str) -> bool:
    """Write text to Windows clipboard.
    Order: tkinter native → ctypes WinAPI → clip.exe subprocess."""
    if not text:
        return False
    # 1. tkinter native (most compatible — same API tkinter Copy button uses)
    try:
        root = tk._default_root
        if root:
            root.clipboard_clear()
            root.clipboard_append(text)
            return True
    except Exception:
        pass
    # 2. ctypes Windows API
    try:
        import ctypes
        enc = (text + "\x00").encode("utf-16-le")
        h = ctypes.windll.kernel32.GlobalAlloc(0x0002, len(enc))
        ctypes.memmove(ctypes.windll.kernel32.GlobalLock(h), enc, len(enc))
        ctypes.windll.kernel32.GlobalUnlock(h)
        if ctypes.windll.user32.OpenClipboard(None):
            ctypes.windll.user32.EmptyClipboard()
            ctypes.windll.user32.SetClipboardData(13, h)  # CF_UNICODETEXT
            ctypes.windll.user32.CloseClipboard()
            return True
    except Exception:
        pass
    # 3. clip.exe subprocess fallback
    try:
        import subprocess
        p = subprocess.Popen("clip", stdin=subprocess.PIPE, shell=True,
                             creationflags=subprocess.CREATE_NO_WINDOW)
        p.communicate(text.encode("utf-16"))
        return True
    except Exception:
        pass
    return False

# ── Dependencies ───────────────────────────────────────────────────────────
_MD_ERROR = ""
try:
    from markitdown import MarkItDown
    MD_OK = True
except Exception as _exc:
    MD_OK = False
    _MD_ERROR = f"{type(_exc).__name__}: {_exc}\n\n{traceback.format_exc()}"

try:
    import sv_ttk;              SVTTK = True
except ImportError:             SVTTK = False

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND = True
except ImportError:             DND = False

# ── Constants ──────────────────────────────────────────────────────────────
APP_NAME    = "MarkItDown"
APP_VERSION = "1.0.0"

SUPPORTED_EXT = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt",
    ".xlsx", ".xls", ".csv",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff",
    ".mp3", ".wav", ".m4a", ".ogg", ".flac",
    ".html", ".htm", ".xml", ".json", ".yaml", ".yml",
    ".zip", ".epub", ".ipynb", ".py", ".txt", ".md",
}

# ── Colours ────────────────────────────────────────────────────────────────
BG    = "#1c1c1e";  BG2 = "#2c2c2e";  BG3 = "#3a3a3c"
FG    = "#f2f2f7";  FG2 = "#aeaeb2"
ACC   = "#0a84ff";  ACC2 = "#409cff"
OK_C  = "#30d158";  ERR_C = "#ff453a";  WARN_C = "#ffd60a"


# ── Single File Tab ────────────────────────────────────────────────────────
class SingleTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="Tab.TFrame")
        self.app     = app
        self.current = None
        self._build()

    def _build(self):
        # ── left column ──────────────────────────────────────────
        left = tk.Frame(self, bg=BG, width=400)
        left.pack(side="left", fill="y", padx=(24, 12), pady=24)
        left.pack_propagate(False)

        lbl_title = tk.Label(left, text="แปลงไฟล์เป็น Markdown",
                 font=("Segoe UI", 18, "bold"), fg=FG, bg=BG)
        lbl_title.pack(anchor="w")
        lbl_sub = tk.Label(left, text="เลือกหรือวางไฟล์เพื่อเริ่มต้น",
                 font=("Segoe UI", 10), fg=FG2, bg=BG)
        lbl_sub.pack(anchor="w", pady=(2, 16))

        # drop zone
        zone = tk.Frame(left, bg=BG2, width=360, height=200,
                        highlightbackground=BG3, highlightthickness=2, cursor="hand2")
        zone.pack(fill="x", pady=(0, 12))
        zone.pack_propagate(False)
        icon_lbl = tk.Label(zone, text="📁", font=("Segoe UI Emoji", 40), fg=ACC, bg=BG2)
        icon_lbl.pack(expand=True, pady=(16, 2))
        lbl_drop = tk.Label(zone, text="ลากวางไฟล์ที่นี่",
                 font=("Segoe UI", 12, "bold"), fg=FG, bg=BG2)
        lbl_drop.pack()
        lbl_formats = tk.Label(zone, text="PDF · Word · Excel · PowerPoint · รูปภาพ · Audio",
                 font=("Segoe UI", 9), fg=FG2, bg=BG2)
        lbl_formats.pack(pady=(2, 16))
        for w in [zone, *zone.winfo_children()]:
            w.bind("<Button-1>", lambda e: self._pick_file())
            if DND:
                w.drop_target_register(DND_FILES)
                w.dnd_bind("<<Drop>>", self._on_drop)

        # file info
        self.file_lbl = tk.Label(left, text="", font=("Segoe UI", 9),
                                  fg=FG2, bg=BG, wraplength=360)
        self.file_lbl.pack(anchor="w", pady=(0, 10))

        # action buttons
        btn_pick = ttk.Button(left, text="  📂  เลือกไฟล์...",
                   command=self._pick_file, style="Accent.TButton")
        btn_pick.pack(fill="x", pady=(0, 8))
        row = tk.Frame(left, bg=BG)
        row.pack(fill="x")
        for txt, cmd in [("💾 บันทึก", self._save),
                         ("📋 คัดลอก", self._copy_all),
                         ("🗑 ล้าง",   self._clear)]:
            b = ttk.Button(row, text=txt, command=cmd)
            b.pack(side="left", padx=(0, 6), pady=3)

        # progress (hidden until converting)
        self.progress = ttk.Progressbar(left, mode="indeterminate")

        # status bar
        sf = tk.Frame(left, bg=BG2, height=44)
        sf.pack(fill="x", side="bottom", pady=(8, 0))
        sf.pack_propagate(False)
        self._s_icon = tk.Label(sf, text="", font=("Segoe UI Emoji", 14), bg=BG2)
        self._s_icon.pack(side="left", padx=(10, 4))
        self._s_msg  = tk.Label(sf, text="", font=("Segoe UI", 9),
                                 fg=FG2, bg=BG2, anchor="w", wraplength=310)
        self._s_msg.pack(side="left", fill="x", expand=True)

        # ── right column: result area ─────────────────────────────
        right = tk.Frame(self, bg=BG2)
        right.pack(side="right", fill="both", expand=True, padx=(0, 24), pady=24)

        hdr = tk.Frame(right, bg=BG2)
        hdr.pack(fill="x", padx=12, pady=(12, 4))
        lbl_res = tk.Label(hdr, text="ผลลัพธ์ Markdown",
                 font=("Segoe UI", 12, "bold"), fg=FG, bg=BG2)
        lbl_res.pack(side="left")
        btn_copy = ttk.Button(hdr, text="📋 Copy", command=self._copy_all,
                   style="Small.TButton")
        btn_copy.pack(side="right")

        tf = tk.Frame(right, bg=BG2)
        tf.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        scroll = ttk.Scrollbar(tf)
        scroll.pack(side="right", fill="y")

        self.result = tk.Text(
            tf, bg=BG, fg=FG, insertbackground=FG,
            font=("Cascadia Code", 10), wrap="word",
            yscrollcommand=scroll.set, relief="flat", padx=12, pady=8,
            selectbackground=ACC,
            exportselection=False,   # ← keeps "sel" tag alive when focus moves
        )
        self.result.pack(fill="both", expand=True)
        scroll.config(command=self.result.yview)

        # ── Keyboard shortcuts ─────────────────────────────────────────────
        # Use bindtags to inject a custom class 'MDResult' at position 0
        # so our handlers fire BEFORE the tkinter Text class binding.
        # This guarantees Ctrl+C is intercepted even if something else
        # would otherwise capture it first.
        _cls = 'MDResult'
        self.result.bindtags((_cls,) + self.result.bindtags())
        self.result.bind_class(_cls, '<Control-c>', self._do_copy)
        self.result.bind_class(_cls, '<Control-C>', self._do_copy)
        self.result.bind_class(_cls, '<<Copy>>',    self._do_copy)
        self.result.bind_class(_cls, '<Control-a>', self._select_all)
        self.result.bind_class(_cls, '<Control-A>', self._select_all)
        self.result.bind_class(_cls, '<<SelectAll>>', self._select_all)
        self.result.bind_class(_cls, '<Control-s>', lambda e: (self._save(), "break")[1])
        self.result.bind_class(_cls, '<Control-S>', lambda e: (self._save(), "break")[1])
        # Keep the instance-level bindings as a second layer of defence
        self.result.bind("<Control-c>", self._do_copy)
        self.result.bind("<Control-C>", self._do_copy)
        self.result.bind("<<Copy>>",    self._do_copy)
        self.result.bind("<Control-a>", self._select_all)
        self.result.bind("<Control-A>", self._select_all)
        self.result.bind("<<SelectAll>>", self._select_all)
        self.result.bind("<Control-s>", lambda e: (self._save(), "break")[1])
        self.result.bind("<Control-S>", lambda e: (self._save(), "break")[1])
        # ── Layout-independent shortcuts (e.g. Thai keyboard) ──────────
        # The keysym bindings above only match when the active keyboard
        # layout produces latin letters. On a Thai layout, Ctrl+C sends a
        # Thai keysym so <Control-c> never fires. Dispatch by PHYSICAL
        # keycode instead (Windows VK codes: A=65, C=67, S=83) — these are
        # the same for every keyboard language.
        def _ctrl_key(e):
            if e.keycode == 67:                       # C → copy
                return self._do_copy(e)
            if e.keycode == 65:                       # A → select all
                return self._select_all(e)
            if e.keycode == 83:                       # S → save
                self._save()
                return "break"
        self.result.bind_class(_cls, '<Control-KeyPress>', _ctrl_key)
        # keep focus after mouse drag-select
        self.result.bind("<Button-1>",        lambda e: self.result.focus_set())
        self.result.bind("<ButtonRelease-1>", lambda e: self.result.focus_set())

        # right-click menu
        menu = tk.Menu(self.result, tearoff=0,
                       bg=BG2, fg=FG, activebackground=ACC, activeforeground=FG,
                       relief="flat", bd=1)
        menu.add_command(label="📋  คัดลอกที่เลือก", command=lambda: self._do_copy(sel_only=True))
        menu.add_command(label="📋  คัดลอกทั้งหมด",  command=self._copy_all)
        menu.add_separator()
        menu.add_command(label="✔  เลือกทั้งหมด",    command=self._select_all)
        menu.add_command(label="🗑  ล้าง",            command=self._clear)
        self.result.bind("<Button-3>",
                         lambda e: (self.result.focus_set(), menu.tk_popup(e.x_root, e.y_root)))

        self._set_status()

    # ── helpers ──────────────────────────────────────────────────
    def _set_status(self, icon="", msg="", color=FG2):
        self._s_icon.config(text=icon)
        self._s_msg.config(text=msg, fg=color)

    def _set_result(self, text, color=FG):
        self.result.config(state="normal")
        self.result.delete("1.0", "end")
        if text:
            self.result.insert("1.0", text)
        self.result.config(fg=color)

    # ── file ──────────────────────────────────────────────────────
    def _on_drop(self, event):
        self._load_file(event.data.strip().strip("{}"))

    def _pick_file(self):
        p = filedialog.askopenfilename(
            title="เลือกไฟล์ที่ต้องการแปลง",
            filetypes=[("ไฟล์ที่รองรับ",
                        " ".join(f"*{e}" for e in sorted(SUPPORTED_EXT))),
                       ("All files", "*.*")])
        if p:
            self._load_file(p)

    def _load_file(self, path):
        path = Path(path)
        if not path.exists():
            self._set_status("⚠️", f"ไม่พบไฟล์: {path.name}", WARN_C)
            return
        if path.suffix.lower() not in SUPPORTED_EXT:
            self._set_status("⚠️", f"ไฟล์ {path.suffix} อาจไม่รองรับ", WARN_C)
        self.current = path
        self.file_lbl.config(
            text=f"📄 {path.name}  ({path.stat().st_size / 1024:.1f} KB)", fg=FG)
        self._convert()

    # ── conversion ────────────────────────────────────────────────
    def _convert(self):
        if not self.current:
            return
        if not MD_OK:
            detail = f"\n\nรายละเอียด:\n{_MD_ERROR}" if _MD_ERROR else ""
            self._set_result(f"❌ MarkItDown ไม่ได้ติดตั้ง{detail}", ERR_C)
            self._set_status("❌", "MarkItDown ไม่ได้ติดตั้ง", ERR_C)
            return
        self._set_result("⏳ กำลังแปลง...", FG2)
        self._set_status("⏳", "กำลังแปลง...", FG2)
        self.progress.pack(fill="x", pady=(4, 0))
        self.progress.start(12)
        path = self.current

        def _run():
            try:
                md = self.app.md.convert(str(path)).text_content
                self.after(0, lambda: self._done(md))
            except Exception as exc:
                err = f"{type(exc).__name__}: {exc}\n\n{traceback.format_exc()}"
                self.after(0, lambda: self._error(err))

        threading.Thread(target=_run, daemon=True).start()

    def _done(self, md):
        self.progress.stop(); self.progress.pack_forget()
        self._set_result(md)
        self._set_status("✅", f"สำเร็จ — {md.count(chr(10))+1:,} บรรทัด  {len(md):,} ตัวอักษร", OK_C)
        self.result.focus_set()   # ← give focus so Ctrl+C works immediately

    def _error(self, msg):
        self.progress.stop(); self.progress.pack_forget()
        self._set_result(f"❌ เกิดข้อผิดพลาด:\n\n{msg}", ERR_C)
        self._set_status("❌", "เกิดข้อผิดพลาด", ERR_C)

    # ── clipboard / edit ──────────────────────────────────────────
    def _do_copy(self, e=None, sel_only=False):
        """Copy selected text; fall back to all text if nothing selected."""
        try:
            text = self.result.get("sel.first", "sel.last")
        except tk.TclError:
            if sel_only:
                self._set_status("⚠️", "ไม่มีข้อความที่เลือก", WARN_C)
                return "break"
            text = self.result.get("1.0", "end-1c")
        if not text:
            return "break"
        if _clipboard_write(text):
            self._set_status("📋", f"คัดลอกแล้ว ({len(text):,} ตัวอักษร)", OK_C)
        else:
            self._set_status("❌", "Copy ไม่สำเร็จ", ERR_C)
        return "break"

    def _copy_all(self):
        text = self.result.get("1.0", "end-1c")
        if not text.strip():
            return
        if _clipboard_write(text):
            self._set_status("📋", f"คัดลอกแล้ว ({len(text):,} ตัวอักษร)", OK_C)
        else:
            self._set_status("❌", "Copy ไม่สำเร็จ", ERR_C)

    def _select_all(self, e=None):
        self.result.tag_add("sel", "1.0", "end")
        return "break"

    def _save(self):
        text = self.result.get("1.0", "end-1c")
        if not text.strip():
            return
        default = (self.current.stem + ".md") if self.current else "output.md"
        path = filedialog.asksaveasfilename(
            defaultextension=".md", initialfile=default,
            filetypes=[("Markdown", "*.md"), ("Text", "*.txt")])
        if path:
            Path(path).write_text(text, encoding="utf-8")
            self._set_status("💾", f"บันทึกแล้ว: {Path(path).name}", OK_C)

    def _clear(self):
        self.current = None
        self.file_lbl.config(text="")
        self._set_result("")
        self._set_status()


# ── Batch Tab ──────────────────────────────────────────────────────────────
class BatchTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="Tab.TFrame")
        self.app   = app
        self.files = []
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=24, pady=24)
        lbl_batch_title = tk.Label(top, text="แปลงหลายไฟล์พร้อมกัน",
                 font=("Segoe UI", 18, "bold"), fg=FG, bg=BG)
        lbl_batch_title.pack(anchor="w")
        lbl_batch_sub = tk.Label(top, text="เพิ่มไฟล์หรือโฟลเดอร์ แล้วกดแปลงทั้งหมด",
                 font=("Segoe UI", 10), fg=FG2, bg=BG)
        lbl_batch_sub.pack(anchor="w", pady=(2, 12))

        br = tk.Frame(top, bg=BG)
        br.pack(anchor="w")
        for txt, cmd in [("📂 เพิ่มไฟล์",    self._add_files),
                         ("📁 เพิ่มโฟลเดอร์", self._add_folder),
                         ("🗑 ล้างรายการ",    self._clear_list)]:
            b = ttk.Button(br, text=txt, command=cmd)
            b.pack(side="left", padx=(0, 8))

        # file list (Delete key removes selected item)
        lf = tk.Frame(self, bg=BG2, highlightbackground=BG3, highlightthickness=1)
        lf.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        sb = ttk.Scrollbar(lf)
        sb.pack(side="right", fill="y")
        self.listbox = tk.Listbox(lf, bg=BG, fg=FG, font=("Segoe UI", 10),
                                   selectbackground=ACC, activestyle="none",
                                   yscrollcommand=sb.set, relief="flat", bd=0)
        self.listbox.pack(fill="both", expand=True)
        sb.config(command=self.listbox.yview)
        self.listbox.bind("<Delete>", self._remove_selected)
        lbl_delete_hint = tk.Label(lf, text="  กด Delete เพื่อลบรายการที่เลือก",
                 font=("Segoe UI", 8), fg=BG3, bg=BG2)
        lbl_delete_hint.pack(anchor="w")

        # output folder
        of = tk.Frame(self, bg=BG)
        of.pack(fill="x", padx=24, pady=(0, 8))
        lbl_out = tk.Label(of, text="บันทึกไปที่:", font=("Segoe UI", 10), fg=FG2, bg=BG)
        lbl_out.pack(side="left")
        self.out_var = tk.StringVar(value=str(Path.home() / "Desktop" / "Markdown Output"))
        entry_out = tk.Entry(of, textvariable=self.out_var, font=("Segoe UI", 10),
                 bg=BG3, fg=FG, insertbackground=FG, relief="flat",
                 width=44)
        entry_out.pack(side="left", padx=8)
        btn_pick_out = ttk.Button(of, text="เลือก", command=self._pick_out, width=6)
        btn_pick_out.pack(side="left")

        # bottom row: status + convert button
        bot = tk.Frame(self, bg=BG)
        bot.pack(fill="x", padx=24, pady=(0, 16))
        self.status_lbl = tk.Label(bot, text="", font=("Segoe UI", 9), fg=FG2, bg=BG)
        self.status_lbl.pack(side="left")
        self.convert_btn = ttk.Button(bot, text="  ⚡  แปลงทั้งหมด",
                                       command=self._convert_all, style="Accent.TButton")
        self.convert_btn.pack(side="right")

        # progress bar (shown during conversion)
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self, variable=self.progress_var, maximum=100)

    # ── file management ───────────────────────────────────────────
    def _add_files(self):
        paths = filedialog.askopenfilenames(
            title="เลือกไฟล์",
            filetypes=[("ไฟล์ที่รองรับ",
                        " ".join(f"*{e}" for e in sorted(SUPPORTED_EXT))),
                       ("All files", "*.*")])
        for p in paths:
            if p not in self.files:
                self.files.append(p)
                self.listbox.insert("end", f"  {Path(p).name}  —  {Path(p).parent}")

    def _add_folder(self):
        folder = filedialog.askdirectory(title="เลือกโฟลเดอร์")
        if not folder:
            return
        added = sum(
            1 for p in Path(folder).rglob("*")
            if p.suffix.lower() in SUPPORTED_EXT and str(p) not in self.files
            and (self.files.append(str(p)) or True)
            and (self.listbox.insert("end", f"  {p.name}  —  {p.parent}") or True)
        )
        self.status_lbl.config(text=f"เพิ่ม {added} ไฟล์", fg=FG2)

    def _pick_out(self):
        d = filedialog.askdirectory()
        if d:
            self.out_var.set(d)

    def _clear_list(self):
        self.files.clear()
        self.listbox.delete(0, "end")
        self.status_lbl.config(text="")

    def _remove_selected(self, e=None):
        for i in reversed(self.listbox.curselection()):
            self.listbox.delete(i)
            del self.files[i]

    # ── conversion ────────────────────────────────────────────────
    def _convert_all(self):
        if not self.files:
            messagebox.showwarning("ไม่มีไฟล์", "กรุณาเพิ่มไฟล์ก่อน"); return
        if not MD_OK:
            messagebox.showerror("ข้อผิดพลาด", "MarkItDown ไม่ได้ติดตั้ง"); return

        out_dir = Path(self.out_var.get())
        out_dir.mkdir(parents=True, exist_ok=True)
        total = len(self.files)
        self.convert_btn.config(state="disabled")
        self.progress.pack(fill="x", padx=24, pady=(0, 4))
        files = list(self.files)

        def _run():
            ok, errors = 0, []
            for i, fp in enumerate(files, 1):
                self.after(0, lambda i=i: (
                    self.status_lbl.config(text=f"กำลังแปลง {i}/{total}...", fg=FG2),
                    self.progress_var.set(i / total * 100),
                ))
                try:
                    res = self.app.md.convert(fp)
                    (out_dir / (Path(fp).stem + ".md")).write_text(
                        res.text_content, encoding="utf-8")
                    ok += 1
                except Exception as exc:
                    errors.append(f"{Path(fp).name}: {exc}")
            self.after(0, lambda: self._batch_done(ok, errors, out_dir))

        threading.Thread(target=_run, daemon=True).start()

    def _batch_done(self, ok, errors, out_dir):
        self.progress.pack_forget()
        self.convert_btn.config(state="normal")
        err = len(errors)
        color = OK_C if not err else WARN_C
        msg = f"✅ สำเร็จ {ok} ไฟล์" + (f"  ❌ ล้มเหลว {err} ไฟล์" if err else "")
        self.status_lbl.config(text=msg, fg=color)

        detail = "\n".join(errors[:5]) + ("\n..." if len(errors) > 5 else "")
        q = (f"แปลงสำเร็จ {ok} ไฟล์  ล้มเหลว {err} ไฟล์\n\n{detail}\n\n"
             if err else f"แปลงสำเร็จ {ok} ไฟล์\n\n")
        if messagebox.askyesno("เสร็จสิ้น", q + "ต้องการเปิดโฟลเดอร์ผลลัพธ์ไหม?"):
            os.startfile(str(out_dir))


# ── Settings Tab ───────────────────────────────────────────────────────────
class SettingsTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="Tab.TFrame")
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="ตั้งค่า",
                 font=("Segoe UI", 18, "bold"), fg=FG, bg=BG).pack(
            anchor="w", padx=32, pady=(24, 4))
        sep = ttk.Separator(self)
        sep.pack(fill="x", padx=32, pady=(0, 16))

        # theme
        sec = self._section("ธีม")
        self._theme = tk.StringVar(value="dark")
        for val, lbl in [("dark", "มืด (Dark)"), ("light", "สว่าง (Light)")]:
            rb = ttk.Radiobutton(sec, text=lbl, variable=self._theme,
                            value=val, command=self._apply_theme)
            rb.pack(anchor="w", padx=8, pady=2)

        # markitdown status
        sec2 = self._section("สถานะ MarkItDown")
        if MD_OK:
            try:
                import importlib.metadata
                ver = importlib.metadata.version("markitdown")
            except Exception:
                ver = "ติดตั้งแล้ว"
            lbl_markitdown = tk.Label(sec2, text=f"✅  markitdown v{ver}",
                     font=("Segoe UI", 10), fg=OK_C, bg=BG2)
            lbl_markitdown.pack(anchor="w", padx=8)
        else:
            lbl_not_ready = tk.Label(sec2, text="❌  MarkItDown ไม่พร้อมใช้งาน",
                     font=("Segoe UI", 10), fg=ERR_C, bg=BG2)
            lbl_not_ready.pack(anchor="w", padx=8)
            if _MD_ERROR:
                sb = ttk.Scrollbar(sec2); sb.pack(side="right", fill="y")
                t = tk.Text(sec2, bg=BG, fg=ERR_C, font=("Cascadia Code", 8),
                            height=8, wrap="word", yscrollcommand=sb.set,
                            relief="flat", padx=6, pady=4)
                t.pack(fill="x", padx=8, pady=4)
                sb.config(command=t.yview)
                t.insert("1.0", _MD_ERROR)
                t.config(state="disabled")

        # about
        sec3 = self._section("เกี่ยวกับ")
        for line in [f"MarkItDown GUI  v{APP_VERSION}",
                     "Python + Tkinter + sv-ttk",
                     "Microsoft MarkItDown"]:
            lbl_about = tk.Label(sec3, text=line, font=("Segoe UI", 9),
                     fg=FG2, bg=BG2)
            lbl_about.pack(anchor="w", padx=8, pady=1)

    def _section(self, title):
        lbl_section = tk.Label(self, text=title, font=("Segoe UI", 11, "bold"),
                 fg=FG, bg=BG)
        lbl_section.pack(anchor="w", padx=32, pady=(8, 4))
        f = tk.Frame(self, bg=BG2, highlightbackground=BG3, highlightthickness=1)
        f.pack(fill="x", padx=32, pady=(0, 12))
        inner = tk.Frame(f, bg=BG2)
        inner.pack(fill="x", padx=8, pady=8)
        return inner

    def _apply_theme(self):
        if SVTTK:
            sv_ttk.set_theme(self._theme.get())


# ── App ────────────────────────────────────────────────────────────────────
class App:
    def __init__(self):
        self.root = (TkinterDnD.Tk if DND else tk.Tk)()
        self.root.title(f"{APP_NAME} — แปลงไฟล์เป็น Markdown")
        self.root.geometry("1100x720")
        self.root.minsize(800, 560)
        self.root.configure(bg=BG)

        if SVTTK:
            sv_ttk.set_theme("dark")

        self.md = MarkItDown() if MD_OK else None

        self._apply_styles()
        self._build_ui()
        self._center()

    def _apply_styles(self):
        s = ttk.Style()
        s.configure("TNotebook",     background=BG,  borderwidth=0)
        s.configure("TNotebook.Tab", background=BG2, foreground=FG2,
                    padding=[16, 8], font=("Segoe UI", 10))
        s.map("TNotebook.Tab",
              background=[("selected", BG),  ("active", BG3)],
              foreground=[("selected", FG),  ("active", FG)])
        s.configure("Tab.TFrame",    background=BG)
        s.configure("TProgressbar",  troughcolor=BG2, background=ACC, thickness=4)
        s.configure("TSeparator",    background=BG3)
        s.configure("TRadiobutton",  background=BG2, foreground=FG, font=("Segoe UI", 10))
        s.configure("Small.TButton", font=("Segoe UI", 8), padding=[4, 2])

    def _build_ui(self):
        # header
        hdr = tk.Frame(self.root, bg=BG2, height=52)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="  📄  MarkItDown",
                 font=("Segoe UI", 14, "bold"), fg=FG, bg=BG2).pack(side="left", padx=16)
        if not MD_OK:
            tk.Label(hdr, text="  ⚠️  MarkItDown ยังไม่ได้ติดตั้ง — ไปที่ ตั้งค่า",
                     font=("Segoe UI", 9), fg=BG, bg=ERR_C).pack(side="right", padx=16)

        # notebook
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True)
        self.tab_single   = SingleTab(nb, self)
        self.tab_batch    = BatchTab(nb, self)
        self.tab_settings = SettingsTab(nb, self)
        nb.add(self.tab_single,   text="  📄  ไฟล์เดียว")
        nb.add(self.tab_batch,    text="  📦  Batch")
        nb.add(self.tab_settings, text="  ⚙️  ตั้งค่า")
        self.notebook = nb

        # Global Ctrl+C — fires for ALL widgets; on Single File tab, always copy.
        # This catches the case where the user never clicked the result area
        # (no focus, no selection) — without this, nothing would copy.
        def _global_copy(e=None):
            try:
                active_tab = nb.index(nb.select())
            except Exception:
                return
            if active_tab == 0:          # 0 = Single File tab
                self.tab_single._do_copy()
                return "break"
        self.root.bind_all("<Control-c>", _global_copy)
        self.root.bind_all("<Control-C>", _global_copy)

        # ── Layout-independent shortcuts for the WHOLE app ──────────────
        # On non-latin layouts (Thai) the keysym bindings above never match,
        # so dispatch by physical keycode (VK codes are layout-independent):
        # A=65, C=67, V=86, X=88. For widgets like Entry/Text we synthesize
        # the standard virtual events so native Copy/Paste/Cut/SelectAll
        # behaviour keeps working no matter the active keyboard language.
        _VK_EVENTS = {86: "<<Paste>>", 88: "<<Cut>>",
                      67: "<<Copy>>",  65: "<<SelectAll>>"}
        _LATIN = set("aAcCvVxXsS")
        def _global_ctrl(e):
            # EN layout → the specific keysym bindings already handled it
            if e.keysym in _LATIN:
                return
            kc = getattr(e, "keycode", None)
            if kc == 67:                              # physical C → copy
                r = _global_copy(e)
                if r == "break":
                    return r
            ev = _VK_EVENTS.get(kc)
            if ev:
                try:
                    e.widget.event_generate(ev)
                    return "break"
                except Exception:
                    pass
        self.root.bind_all("<Control-KeyPress>", _global_ctrl)

        # footer
        ftr = tk.Frame(self.root, bg=BG2, height=26)
        ftr.pack(fill="x", side="bottom")
        ftr.pack_propagate(False)
        tk.Label(ftr,
                 text=f"  {APP_NAME} v{APP_VERSION}  |  PDF · Word · Excel · PowerPoint · รูปภาพ · Audio · และอื่นๆ",
                 font=("Segoe UI", 8), fg=FG2, bg=BG2).pack(side="left")

    def _center(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")

    def run(self):
        self.root.mainloop()


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    App().run()
