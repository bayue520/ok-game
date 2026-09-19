# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

# ===== 自动收集 ok-script 的全部内容 =====
ok_datas, ok_binaries, ok_hiddenimports = collect_all('ok')

# ===== 自动收集 ttkbootstrap =====
ttk_datas, ttk_binaries, ttk_hiddenimports = collect_all('ttkbootstrap')

# ===== 自动收集 ultralytics =====
ultra_datas, ultra_binaries, ultra_hiddenimports = collect_all('ultralytics')

# ===== 自动收集 onnxocr =====
try:
    ocr_datas, ocr_binaries, ocr_hiddenimports = collect_all('onnxocr')
except Exception:
    ocr_datas, ocr_binaries, ocr_hiddenimports = [], [], []

# ===== 合并 =====
datas = ok_datas + ttk_datas + ultra_datas + ocr_datas + [
    ('src', 'src'),
    ('best.pt', '.'),
    ('tpl.png', '.'),
    ('zero.png', '.'),
    ('retry.png', '.'),
    ('assets', 'assets'),
    ('icons', 'icons'),
]

binaries = ok_binaries + ttk_binaries + ultra_binaries + ocr_binaries

hiddenimports = (
    ok_hiddenimports
    + ttk_hiddenimports
    + ultra_hiddenimports
    + ocr_hiddenimports
    + [
        'ok',
        'ok.task',
        'ok.task.task',
        'ok.cli',
        'ok.gui',
        'ok.device',
        'ttkbootstrap',
        'cv2',
        'numpy',
        'PIL',
        'PIL.Image',
        'pynput',
        'pydirectinput',
        'comtypes',
        'pycaw',
        'adbutils',
        'shapely',
        'pyclipper',
        'opencc',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
    ]
)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'PySide6', 'PyQt5', 'PyQt6',
        'matplotlib', 'pandas', 'scipy',
        'notebook', 'jupyter',
        'IPython', 'tkinter.test',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='自动战斗',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                 # ok-script 里有二进制，UPX 压缩容易出问题，关掉
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,             # 单 exe 无控制台
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/icon.ico',
)