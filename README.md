# MarkItDown GUI

โปรแกรม Windows สำหรับแปลงไฟล์เอกสารเป็น Markdown — สร้างด้วย Python + Tkinter ครอบ [Microsoft MarkItDown](https://github.com/microsoft/markitdown)

A Windows GUI for converting documents to Markdown, powered by Microsoft MarkItDown.

## ความสามารถ

- แปลงไฟล์เดียวพร้อมดูตัวอย่างผลลัพธ์ทันที (ลากวางไฟล์ได้)
- แปลงหลายไฟล์/ทั้งโฟลเดอร์แบบ Batch
- รองรับ PDF, Word, Excel, PowerPoint, รูปภาพ, เสียง, HTML, ZIP, EPUB และอื่นๆ
- ธีมมืด/สว่าง (sv-ttk) อินเทอร์เฟซภาษาไทย
- คีย์ลัด Ctrl+C / Ctrl+A / Ctrl+S ใช้ได้ทั้งแป้นพิมพ์ไทยและอังกฤษ

## การติดตั้ง

ดาวน์โหลดตัวติดตั้ง `MarkItDown_Setup_vX.X.X.exe` จากหน้า [Releases](https://github.com/KorakrodT/Markitdown/releases) แล้วติดตั้งตามขั้นตอน (มีหน้าติดตั้งภาษาไทย)

## รันจากซอร์ส

```bash
pip install -r src/requirements.txt
python src/markitdown_gui.py
```

ต้องใช้ Python 3.9 ขึ้นไป (ทดสอบกับ 3.13)

## Build เป็น .exe + Installer

ดูรายละเอียดใน [BUILD_GUIDE.md](BUILD_GUIDE.md) — สรุปสั้นๆ: double-click `src\build_all.bat` (ต้องมี Python และ Inno Setup 6) ผลลัพธ์จะอยู่ใน `release\`

## โครงสร้างโปรเจกต์

```
src/
├── markitdown_gui.py    # ซอร์สโค้ดหลัก
├── build_all.bat        # สคริปต์ build ครบวงจร
├── markitdown_gui.spec  # คอนฟิก PyInstaller
├── installer.iss        # สคริปต์ Inno Setup
├── build_installer.py   # ตัวเรียก ISCC (รองรับ path ภาษาไทย)
└── Thai.isl             # ภาษาไทยสำหรับหน้าติดตั้ง
```

## เครดิต

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) — ตัวแปลงเอกสาร
- [sv-ttk](https://github.com/rdbende/Sun-Valley-ttk-theme) — ธีม
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) — ลากวางไฟล์

## License

[MIT](LICENSE)
