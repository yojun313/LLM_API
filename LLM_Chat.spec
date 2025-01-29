# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['LLM_Chat.py'],  # Python 파일 이름
    pathex=['.'],
    binaries=[],
    datas=[],  # 추가할 데이터 파일이 있을 경우 여기에 추가
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
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
    name='LLM_Chat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # UPX 압축 활성화 (선택 사항)
    console=True,  # 콘솔 창 숨김 (GUI 프로그램일 경우)
    icon='C:/GitHub/LLM_API/source/exe_icon.ico',  # 아이콘 추가
)
