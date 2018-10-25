import sys, argparse, os, logging, importlib, pkgutil
from os import listdir
from os.path import abspath, dirname, isfile, join
import xml.etree.ElementTree as ET

from simulators import *


### Parse and Check Arguments
parser = argparse.ArgumentParser(
    description='Simulate schedulers.')
parser.add_argument('simModuleName', metavar='module_name',
                    help='Specify the name of the simulator module.',
                    type=str)
parser.add_argument('schedFileName', metavar='scheduler_filename',
                    help='Specify the name of the scheduler file.',
                    type=str)
parser.add_argument('configFileName', metavar='config_file_name',
                    help='Specify the name of the config file.',
                    type=str)
parser.add_argument('--numGen', metavar='N',
                    help='Specify the number of generations to train for.',
                    type=int,default=100)
parser.add_argument('--numChrom', metavar='N',
                    help='Specify the total chromosomes per generation.',
                    type=int,default=30)
parser.add_argument('--ESCperc','-ESC', metavar='N',
                    help='Specify the elite, selection, crossover ratio in ' \
                    'percents. (MUST sum to 1.0)', 
                    nargs=3,type=float,default=[0.10,0.50,0.40])
parser.add_argument('--mutRate', '-mr', metavar='R',
                    help='Specify the starting mutation rate',
                    type=float,default=1.5)
parser.add_argument('--resultsFN', metavar='FN', 
                    help='Specify where to output results stats to.',
                    type=str,default='results')
parser.add_argument('--log', '-l', 
                    help='Flag to print out log statements for debugging.',
                    action='store_true',default=False)
args = parser.parse_args()

# Check ESC, mutRate, numGen, numChrom
tot = 0
for num in args.ESCperc:
    assert num >= 0.0 and num <= 1.0, 'ESC entry invalid.'
    tot += num
assert tot==1.0, 'ESC must sum to 100'
assert args.mutRate > 0, 'Mutation rate (%.2f) invalid'%args.mutRate
assert args.numChrom > 0, 'Number of chromosomes (%d) invalid'%args.numGen
assert args.numGen > 0, 'Number of generations (%d) invalid'%args.numGen

# Check files
currPath = dirname(abspath(__file__))
configPath = os.path.join(currPath,'ConfigurationFiles',args.configFileName)
assert os.path.isfile(configPath), f'Config File {args.configFileName} is invalid'
args.configPath = configPath

schedPath = os.path.join(currPath,'schedulers',args.schedFileName)
assert os.path.isfile(schedPath), f'Scheduler File {args.schedFileName} is invalid'

simMod = importlib.util.find_spec(f'simulators.{args.simModuleName}')
assert simMod is not None, f'Simulator module {args.simModuleName} does not exist.'

### Config File: Add similator to XML and grab file
xmlTree = ET.parse(configPath)
xmlTree.getroot().findall('sched')[0].set('className',schedPath)
xmlTree.write(configPath)

### Execute Simulator
importedSimMod = importlib.import_module(f"simulators.{args.simModuleName}")
importedSimMod.main(args)

sys.exit(0)

#simMod.loader.main(args)
for mod in sys.modules:
    print(type(mod))
current_module = __import__(__name__)

# this is the package we are inspecting -- for example 'email' from stdlib
for importer, modname, _ in pkgutil.iter_modules(sys.modules['simulators'].__path__):
    if modname == args.simModuleName:
        print(f'simulators.{modname}')
        module = __import__(f'simulators.{modname}',globals())
        print("Imported", module)
    #module = __import__(modname, fromlist="dummy")
    #
#print(sys.modules['edf_simulator'])



e = None
for e in globals():
    if e == 0:
        print(e)



#print(sys.modules[f'simulators/{args.simulator}']) #['mod1'])
# print(sys.modules[f'simulators/{args.simulator}'])
# print(f'simulators/{args.simulator}')
e = None
GD = globals()
for e in GD:
    print(f'Elem {e}: {GD[e]}' )
#print(globals())

edf_simulator.main(args)
