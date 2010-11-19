#ejecutar:
#python setup.py py2exe
from distutils.core import setup
import py2exe

setup(windows=[{"script" : "main.py"}], options={"py2exe" : {"includes" : ["sip", "PyQt4.QtSql"]}})
