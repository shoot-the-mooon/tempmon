# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import os, pathlib

block_cipher = None

# ───────────────────────────────────────────────────────────
# 1) hiddenimports  ──  collect_submodules 後に手動フィルタ
# ───────────────────────────────────────────────────────────
hidden_plotly = [
    m for m in collect_submodules('plotly')
    if not m.startswith('plotly.plotly')      # deprecated を除外
]

hidden_pandas = [
    m for m in collect_submodules('pandas')
    if not m.startswith('pandas.tests')       # テスト一式を除外
]

extra_hidden = (
      collect_submodules('django_bootstrap5')
    + collect_submodules('widget_tweaks')
    + hidden_plotly
    + hidden_pandas
)

# ───────────────────────────────────────────────────────────
# 2) data files ──  collect_data_files → ファイルパスで絞る
# ───────────────────────────────────────────────────────────
plotly_datas_all  = collect_data_files('plotly')
plotly_datas_json = [d for d in plotly_datas_all if d[0].endswith('.json')]

pandas_datas_all  = collect_data_files('pandas')
pandas_datas_csv  = [
    d for d in pandas_datas_all
    if pathlib.PurePosixPath(d[0]).match('*/io/data/*')     # csv, txt サンプル
]

extra_datas = plotly_datas_json + pandas_datas_csv

# ───────────────────────────────────────────────────────────
# 3) Analysis
# ───────────────────────────────────────────────────────────
a = Analysis(
    ['run_app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static',    'static'),
        ('tools',     'tools'),
        ('db.sqlite3','db.sqlite3'),
        ('backup',    'backup'),
    ] + extra_datas,
    hiddenimports=[
        # Django 本体まわり
        'django',
        'django.template.loaders.filesystem',
        'django.template.loaders.app_directories',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'sqlite3',
        # プロジェクト側で直接 import している物
        'django_bootstrap5',
        'widget_tweaks',
        'plotly',
        'pandas',
    ] + extra_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='VitalRec',
    debug=False,                  # 開発時は True でコンソール確認
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,             # macOS/arm64 は自動
    codesign_identity=None,
    entitlements_file=None,
    icon='static/favicon.ico'
)