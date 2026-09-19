# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 把 ok-script 的 src/ 整个打包进去
        ('src', 'src'),
        # 模型和模板图片
        ('best.pt', '.'),
        ('tpl.png', '.'),
        ('zero.png', '.'),
        ('retry.png', '.'),
        # 如果你有 assets、icons、configs 目录也加进来
        ('assets', 'assets'),
        ('icons', 'icons'),
    ],
    hiddenimports=[
        'ok',
        'ok.task',
        'ok.task.task',
        'ttkbootstrap',
        'ultralytics',
        'cv2',
        'numpy',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'PySide6', 'PyQt5', 'PyQt6',
        'matplotlib', 'pandas', 'scipy',
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,        # 不显示黑窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/icon.ico',   # 有图标就留，没有就删掉这行
)