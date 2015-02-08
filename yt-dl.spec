# -*- mode: python -*-
a = Analysis(['yt-dl.py'],
             pathex=['D:\\Torben\\yt-dl'],
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

"""
resources = []
ffmpeg = r'D:\Torben\bin\ffmpeg.exe'
if not os.path.exists(ffmpeg): raise RuntimeError("Unable to find ffmpeg at " + ffmpeg)
resources.append(('ffmpeg.exe', ffmpeg, 'DATA'))


#a.binaries + [('ffmpeg', r'D:\Torben\bin\ffmpeg.exe', 'DATA')],
"""