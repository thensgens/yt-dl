# -*- mode: python -*-
a = Analysis(['yt-dl.py'],
             pathex=['C:\\Users\\thens\\software\\yt-dl'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='yt-dl.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='icons\\yt-icon_rsz.ico')
