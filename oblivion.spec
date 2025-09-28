# PyInstaller spec for OBLIVION (Crash-Proof)
import os
from PyInstaller.utils.hooks import collect_submodules

root = os.path.abspath('.')
src_dir = os.path.join(root, 'src')

# Explicit hidden imports to avoid ModuleNotFound errors
hidden = [
    'boot_manager',
    'oblivion_core',
    'hardware_info',
    'disk_wiper',
]

block_cipher = None

# Bundle private key for runtime JWT signing
private_key_src = os.path.join(root, 'CP', 'python-scripts', 'output', 'private_key.pem')
datas = []
if os.path.exists(private_key_src):
    datas.append((private_key_src, '.'))

pathex = [src_dir]

a = Analysis(
    ['src/start_oblivion.py'],
    pathex=pathex,
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OBLIVION',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)