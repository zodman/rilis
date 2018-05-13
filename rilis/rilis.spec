# -*- mode: python -*-

block_cipher = None


a = Analysis(['rilis.py'],
             pathex=['C:\\Users\\crx\\Desktop\\fansub_rilis\\rilis'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='rilis',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
