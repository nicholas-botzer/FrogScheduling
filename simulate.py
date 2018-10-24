import sys, argparse, os, logging
from os import listdir
from os.path import abspath, dirname, isfile, join
import xml.etree.ElementTree

from simulators.ga_simulator import main


### Parse and Check Arguments
parser = argparse.ArgumentParser(
    description='Simulate schedulers.')
parser.add_argument('simulator', metavar='module_name',
                    help='Specify the name of the simulator module.',
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
    assert num >= 0 and num <= 1.0, 'ESC entry invalid.'
    tot += num
assert tot==1.0, 'ESC must sum to 1.0'
assert args.mutRate > 0, 'Mutation rate (%.2f) invalid'%args.mutRate
assert args.numChrom > 0, 'Number of chromosomes (%d) invalid'%args.numGen
assert args.numGen > 0, 'Number of generations (%d) invalid'%args.numGen

# Check files
# Namespace(ESCperc=[10, 50, 40], config='FROG_baseTest.xml', log=True, mutRate=[1.5], 
#     resultsFN=['frogbase_results.txt'], simulator='ga_simulator', totChrom=[30])



# ### Config File: Add similator to XML and grab file
# xmlFilePath = os.path.join(curr_dir+'/ConfigurationFiles',args.config)
# xmlFile = xml.etree.ElementTree.parse(xmlFilePath)


# # Append new tag: <a x='1' y='abc'>body text</a>
# new_tag = xml.etree.ElementTree.SubElement(et.getroot(), 'a')
# new_tag.text = 'body text'
# new_tag.attrib['x'] = '1' # must be str; cannot be an int
# new_tag.attrib['y'] = 'abc'

# # Write back to file
# #et.write('file.xml')
# et.write('file_new.xml')

# #print sys.modules
# config_fn = 'EDF_periodicTest.xml'
# curr_dir = dirname(abspath(__file__))
# config_dir = os.path.join(curr_dir+'/ConfigurationFiles',config_fn)
# edf_simulator.main([0,config_dir])

main(args)