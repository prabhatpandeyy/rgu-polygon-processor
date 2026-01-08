"""
Create PyInstaller spec file with proper geospatial library inclusion
"""

spec_content = """# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

a = Analysis(
    ['rgu_polygon_processor.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pyogrio',
        'fiona',
        'geopandas',
        'shapely',
        'pandas',
        'openpyxl',
        'xlrd',
        'tkinter',
        'threading'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Collect all geospatial libraries
pyogrio_datas, pyogrio_binaries, pyogrio_hiddenimports = collect_all('pyogrio')
fiona_datas, fiona_binaries, fiona_hiddenimports = collect_all('fiona')
geopandas_datas, geopandas_binaries, geopandas_hiddenimports = collect_all('geopandas')

a.datas += pyogrio_datas
a.datas += fiona_datas
a.datas += geopandas_datas
a.binaries += pyogrio_binaries
a.binaries += fiona_binaries
a.binaries += geopandas_binaries
a.hiddenimports += pyogrio_hiddenimports
a.hiddenimports += fiona_hiddenimports
a.hiddenimports += geopandas_hiddenimports

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RGU_Polygon_Processor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

with open('RGU_Polygon_Processor.spec', 'w') as f:
    f.write(spec_content.strip())

print("PyInstaller spec file created: RGU_Polygon_Processor.spec")