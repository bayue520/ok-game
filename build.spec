# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

ok_datas, ok_binaries, ok_hiddenimports = collect_all('ok')
ttk_datas, ttk_binaries, ttk_hiddenimports = collect_all('ttkbootstrap')
ultra_datas, ultra_binaries, ultra_hiddenimports = collect_all('ultralytics')
torch_datas, torch_binaries, torch_hiddenimports = collect_all('torch')
tv_datas, tv_binaries, tv_hiddenimports = collect_all('torchvision')

datas = ok_datas + ttk_datas + ultra_datas + torch_datas + tv_datas + [
    ('src', 'my/src'),
    ('best.pt', 'my'),
    ('tpl.png', 'my'),
    ('zero.png', 'my'),
    ('retry.png', 'my'),
    ('assets', 'my/assets'),
    ('icons', 'my/icons'),
    ('configs', 'my/configs'),
    ('global_state.py', 'my'),
    ('pyarmor_runtime_000000', 'my/pyarmor_runtime_000000'),
]

binaries = ok_binaries + ttk_binaries + ultra_binaries + torch_binaries + tv_binaries

hiddenimports = (
    ok_hiddenimports + ttk_hiddenimports + ultra_hiddenimports
    + torch_hiddenimports + tv_hiddenimports
    + [
        'ok', 'ok.task', 'ok.task.task', 'ok.cli', 'ok.gui', 'ok.device',
        'ok.device.DeviceManager', 'ok.task.TaskExecutor',
        'src', 'src.config', 'src.tasks', 'src.tasks.AutoBattle',
        'global_state',
        'ttkbootstrap', 'cv2', 'numpy', 'PIL', 'PIL.Image',
        'pynput', 'pydirectinput', 'comtypes', 'pycaw', 'adbutils',
        'shapely', 'pyclipper', 'opencc', 'requests', 'urllib3',
        'certifi', 'charset_normalizer', 'idna',
        'torch', 'torchvision',
        'pyarmor_runtime_000000',
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
        'notebook', 'jupyter', 'IPython', 'tkinter.test',
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
    [],
    exclude_binaries=True,
    name='AutoBattle',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='AutoBattle',
)