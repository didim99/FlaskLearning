from distutils.core import setup
from Cython.Build import cythonize

ext_options = {"compiler_directives": {"profile": True}, "annotate": True, "language_level": 3}
setup(ext_modules=cythonize("encryption/fastmath.pyx", **ext_options))
