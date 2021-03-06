"""
DIRECTORY DESCRIPTION:
    Holds all simulators that run on simulator.main(argv)
"""

### Set __all__ to contain all modules in simulator directory
from os import listdir
from os.path import abspath, dirname, isfile, join
init_dir = dirname(abspath(__file__)) # get folder dir from init file dir
py_files = [file_name.replace(".py", "") for file_name in listdir(init_dir) \
            if isfile(join(init_dir, file_name)) and ".py" in file_name \
            and  not ".pyc" in file_name]
py_files.remove("__init__")
#print 'simulators __all__: {}'.format(py_files)
__all__ = py_files

### Import modules from other depend directors
from schedulers import *
from tools import *