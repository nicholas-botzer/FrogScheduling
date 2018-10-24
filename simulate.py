import sys, argparse, os, logging, importlib
from os import listdir
from os.path import abspath, dirname, isfile, join
import xml.etree.ElementTree as ET

from simulators import *


### Parse and Check Arguments
parser = argparse.ArgumentParser(
    description='Simulate schedulers.')
parser.add_argument('simulator', metavar='module_name',
                    help='Specify the name of the simulator module.',
                    type=str)
parser.add_argument('sched', metavar='scheduler_filename',
                    help='Specify the name of the scheduler file.',
                    type=str)
parser.add_argument('config', metavar='config_file_name',
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
                    'percents. (MUST sum to 100)', 
                    nargs=3,type=float,default=[10,50,40])
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
configPath = os.path.join(f'{currPath}/ConfigurationFiles',args.config)
assert os.path.isfile(configPath), f'Config File {args.config} is invalid'
args.configPath = configPath

schedPath = os.path.join(f'{currPath}/schedulers',args.sched)
assert os.path.isfile(schedPath), f'Scheduler File {args.sched} is invalid'

mod = importlib.util.find_spec(f'simulators.{args.simulator}')
assert mod is not None, f'Simulator module {args.simulator} does not exist.'

### Config File: Add similator to XML and grab file
xmlTree = ET.parse(configPath)
print(schedPath, ET.SubElement(xmlTree.getroot(),'sched'))
ET.SubElement(xmlTree.getroot(),'sched').set('className',schedPath)
# new_tag.attrib['x'] = '1'
xmlTree.write(args.config)

### Execute Simulator
sys.exit(0)
edf_simulator.main([0,config_dir])
