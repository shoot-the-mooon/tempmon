from PyInstaller.utils.hooks import collect_submodules, collect_data_files
block_cipher = None

extra_hidden = (
      collect_submodules('django_bootstrap5')   # ← import 名
    + collect_submodules('widget_tweaks')
    + collect_submodules('plotly')
    + collect_submodules('pandas')
)

extra_datas  = (
      collect_data_files('plotly', includes=['*.json'])
    + collect_data_files('pandas', includes=['io/data/*'])
)

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
        # 既存分
        'bootstrap5',            # インポート名ではなく Django テンプレート用なら残しても OK
        'widget_tweaks',
        'plotly',
        'pandas',
    ] + extra_hidden,            # ← 追加したリストを結合
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
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,               # デバッグ時は True にしてログ確認推奨
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,            # Mac/arm64 なら 'arm64' は自動設定で OK
    codesign_identity=None,
    entitlements_file=None,
    icon='static/favicon.ico'
)