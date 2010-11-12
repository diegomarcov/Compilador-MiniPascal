#ejecutar:
#python setup.py py2exe
from distutils.core import setup
import py2exe
from glob import glob

setup(console=['SynAn.py'])
