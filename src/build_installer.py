#!/usr/bin/env python3
"""
build_installer.py
Compiles the Inno Setup installer without relying on cmd.exe
for Unicode path handling.

Called from build_all.bat:  py build_installer.py
"""
import os, sys, re, shutil, tempfile, subprocess

# ── Paths ───────────────────────────────────────────────────────────────
SRC_DIR  = os.path.dirname(os.path.abspath(__file__))
THAI_SRC = os.path.join(SRC_DIR, 'Thai.isl')
ISS_SRC  = os.path.join(SRC_DIR, 'installer.iss')
TEMP_DIR = tempfile.gettempdir()   # always an ASCII-safe path

# ── Find ISCC.exe ────────────────────────────────────────────────────────
ISCC_PATHS = [
    r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
    r'C:\Program Files\Inno Setup 6\ISCC.exe',
]
iscc = next((p for p in ISCC_PATHS if os.path.isfile(p)), None)
if not iscc:
    sys.exit('[ERROR] Inno Setup 6 not found. '
             'Download from https://jrsoftware.org/isdl.php')
print(f'[OK] ISCC: {iscc}')

# ── Copy Thai.isl to a pure-ASCII temp path ──────────────────────────────
# Python uses Win32 Unicode APIs here — no cmd.exe encoding issues.
if not os.path.isfile(THAI_SRC):
    sys.exit(f'[ERROR] Thai.isl not found: {THAI_SRC}')

thai_temp = os.path.join(TEMP_DIR, 'MarkItDownThai.isl')
shutil.copy2(THAI_SRC, thai_temp)
print(f'[OK] Thai.isl copied to: {thai_temp}')

# Verify
if not os.path.isfile(thai_temp):
    sys.exit(f'[ERROR] Copy failed — file not found at: {thai_temp}')

# Spot-check LanguageName so we know the right file was copied
with open(thai_temp, encoding='utf-8-sig') as f:
    head = f.read(300)
lang_match = re.search(r'LanguageName=(.+)', head)
lang_name  = lang_match.group(1).strip() if lang_match else '(not found)'
print(f'[OK] LanguageName in Thai.isl: {lang_name}')

# ── Patch installer.iss ──────────────────────────────────────────────────
# Replace the #ifndef ThaiIslPath ... #endif block and {#ThaiIslPath}.
# Write the result to SRC_DIR so relative paths in the .iss remain valid.
with open(ISS_SRC, encoding='utf-8') as f:
    lines = f.readlines()

patched_lines = []
skip = False
for line in lines:
    s = line.strip()
    # Skip the ThaiIslPath define block
    if s.startswith('; ThaiIslPath') or s == '#ifndef ThaiIslPath':
        skip = True
        continue
    if skip:
        if s == '#endif':
            skip = False
        continue
    # Replace placeholder with actual ASCII temp path
    # Use forward slashes — Inno Setup accepts them and avoids escape questions
    if '{#ThaiIslPath}' in line:
        safe = thai_temp.replace('\\', '/')
        line = line.replace('{#ThaiIslPath}', safe)
    patched_lines.append(line)

ISS_GEN = os.path.join(SRC_DIR, 'installer_gen.iss')
with open(ISS_GEN, 'w', encoding='utf-8') as f:
    f.writelines(patched_lines)
print(f'[OK] installer_gen.iss written')

# Show the Languages section from the generated file
print('[OK] Languages section:')
in_lang = False
for line in patched_lines:
    if line.strip() == '[Languages]':
        in_lang = True
    if in_lang:
        print('     ', line.rstrip())
        if line.strip().startswith('[') and line.strip() != '[Languages]':
            break

# ── Run ISCC via subprocess (CreateProcessW — fully Unicode) ─────────────
# subprocess.run on Windows uses CreateProcessW, which passes Unicode args
# correctly to ISCC, bypassing all cmd.exe codepage issues.
print(f'\n[OK] Compiling installer (this may take a while)...')
result = subprocess.run([iscc, ISS_GEN])
if result.returncode != 0:
    sys.exit(f'[ERROR] ISCC exited with code {result.returncode}')

print('\n[OK] Installer compiled successfully')
