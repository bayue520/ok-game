import os
from setuptools import setup
from Cython.Build import cythonize

BASE = os.path.dirname(os.path.abspath(__file__))

py_files = [
    os.path.join(BASE, "src", "tasks", "AutoBattle.py"),
    os.path.join(BASE, "config.py"),
]

setup(
    ext_modules=cythonize(py_files, language_level=3),
)