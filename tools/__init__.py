"""
TOOLS PACKAGE DESCRIPTION:
  - This directory contains global tools
  - Subdirectories contain tool packages for specific scheduling algorithms.
"""


### Set __all__ to contain all modules in simulator directory
# from os import listdir
# from os.path import abspath, dirname, isfile, join
# init_dir = dirname(abspath(__file__)) # get folder dir from init file dir
# py_files = [file_name.replace(".py", "") for file_name in listdir(init_dir) \
#             if isfile(join(init_dir, file_name)) and ".py" in file_name \
#             and  not ".pyc" in file_name]
# py_files.remove("__init__")
# print 'simulators __all__: {}'.format(py_files)
# __all__ = py_files

import pkgutil
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    # module = loader.find_module(module_name).load_module(module_name)
    # globals()[module_name] = module
#print 'tools __all__: {}'.format(__all__)

### Import modules from other depend directors
from schedulers import *
from tools import *