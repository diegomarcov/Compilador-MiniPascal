from distutils.core import setup
import py2exe
from glob import glob
data_files = [("Microsoft.VC90.CRT", glob(r'E:\Archivos de programa\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT.manifest')),
              ("Microsoft.VC90.CRT", glob(r'E:\Archivos de programa\Microsoft Visual Studio 9.0\VC\redist\x86\msvcr90.dll'))]
setup(
  data_files=data_files,
  console=['pycomp.py']
  
)
