# MarkItDown GUI — คู่มือ Build

## โครงสร้างโปรเจกต์

| ตำแหน่ง | คำอธิบาย |
|---|---|
| `src\markitdown_gui.py` | ซอร์สโค้ดหลัก (Python + tkinter) |
| `src\build_all.bat` | สคริปต์ build ครบวงจร: exe + installer |
| `src\markitdown_gui.spec` | คอนฟิก PyInstaller |
| `src\installer.iss` | สคริปต์ Inno Setup (เลขเวอร์ชันอยู่ที่ `MyAppVersion`) |
| `src\build_installer.py` | ตัวเรียก ISCC (รองรับ path ภาษาไทย) |
| `src\Thai.isl` | ภาษาไทยสำหรับหน้าติดตั้ง |
| `release\dist\MarkItDown\` | โปรแกรมที่ build แล้ว (portable) |
| `release\installer\` | ตัวติดตั้ง `MarkItDown_Setup_vX.X.X.exe` |

## วิธี Build

Double-click `src\build_all.bat` — สคริปต์จะทำให้ทั้งหมด:

1. ติดตั้ง dependencies (`pip install -r requirements.txt`)
2. ลบ build เก่า
3. Build exe ด้วย PyInstaller → `release\dist\MarkItDown\`
4. หา Inno Setup (ถ้าไม่มีจะข้ามขั้นตอน installer)
5. สร้าง installer → `release\installer\`

ใช้เวลา ~5–7 นาที

## สิ่งที่ต้องติดตั้งก่อน

- Python 3.9+ (ทดสอบกับ 3.13) — https://python.org
- Inno Setup 6 (สำหรับสร้าง installer) — https://jrsoftware.org/isdl.php

## การเปลี่ยนเลขเวอร์ชัน

แก้ 2 จุดให้ตรงกัน:

1. `src\markitdown_gui.py` → `APP_VERSION = "x.x.x"`
2. `src\installer.iss` → `#define MyAppVersion "x.x.x"`

## ข้อควรระวัง

- **ไฟล์ .bat ต้องเป็น ASCII + CRLF เท่านั้น** ห้ามใส่คอมเมนต์ภาษาไทยหรือ `chcp 65001` กลางไฟล์ — cmd จะอ่านไฟล์เพี้ยนทันที (อาการ: `'tDown' is not recognized...`)
- คีย์ลัดใน tkinter ต้อง bind ด้วย `<Control-KeyPress>` + `event.keycode` (ไม่ใช่ keysym) เพื่อให้ทำงานกับแป้นพิมพ์ไทย
- โฟลเดอร์ `release\build\` เป็นไฟล์ชั่วคราว ลบได้เสมอ
