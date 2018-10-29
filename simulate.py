import sys, argparse, os, logging, importlib, pkgutil
from os import listdir
from os.path import abspath, dirname, isfile, join
import xml.etree.ElementTree as ET
import simso.schedulers
from simulators import *

logging.basicConfig(format='%(message)s')
logger = logging.getLogger('root')
SIMMOD_TO_SCHEDFILE = {'FROG.py':'ga_simulator'}

def main(args):

    # Setup Logging. Levels 0 -> 20
    if args.log:
        logger.setLevel(args.log)
    else:
        logger.setLevel(20)
    
    ### Main nested loop for simulator calls
    for sidx,schedName in enumerate(args.schedNames):
        for cidx,configFileName in enumerate(args.configFileNames):
            modifyXML(args.configPaths[cidx],args.schedPaths[sidx])

            simModuleName = SIMMOD_TO_SCHEDFILE[schedName] if \
                            SIMMOD_TO_SCHEDFILE.get(schedName) else \
                            'default_simulator'
            importedSimMod = importlib.import_module(f"simulators.{simModuleName}")
            logger.log(20,'\n===================================================\n' \
                    f'Simulating ({schedName}) on config ({configFileName}) \nwith' \
                    f' sim module ({simModuleName})' \
                    '\n===================================================\n\n')
            args.currentConfigIdx = cidx
            args.currentSchedIdx = sidx
            importedSimMod.main(args)

#### HELPER FUNCTIONS ###  

'''
Parses arguments from commandline.
Returns
- Args namespace
'''
def parse_args():
    ### Parse and Check Arguments
    parser = argparse.ArgumentParser(
        description='Simulate schedulers.')
    parser.add_argument('--schedNames', metavar='sched_name',
                        help='Specify the name of the schedulers.',
                        type=str, nargs='+')
    parser.add_argument('--configFileNames', metavar='config_file_name',
                        help='Specify the name of the config file.',
                        type=str, nargs='+')
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
    parser.add_argument('--log', '-l', type=int, nargs='?',
                        help='Set logging level.',default=10)
    args = parser.parse_args()
    return args

'''
Checks the validity of arguments and manages the config files, modules, and 
other preprocessing.
Parameters
- args namespace from argparse
Returns
- Checked and final args namespace to be passed to main
'''
def check_args(args):
    # Check ESC, mutRate, numGen, numChrom
    tot = 0
    for num in args.ESCperc:
        assert num >= 0.0 and num <= 1.0, 'ESC entry invalid.'
        tot += num
    assert tot==1.0, 'ESC must sum to 100'
    assert args.mutRate > 0, 'Mutation rate (%.2f) invalid' % args.mutRate
    assert args.numChrom > 0, 'Number of chromosomes (%d) invalid' % args.numGen
    assert args.numGen > 0, 'Number of generations (%d) invalid' % args.numGen

    # Check and manage module names
    schedNames,schedPaths = [],[]
    if args.schedNames:
        schedNames = [x for x in args.schedNames]
    else:
        with open('Scheduler List','r') as f:
            for idx,line in enumerate(f):
                if idx == 0: continue
                schedNames.append(line.rstrip())
    currPath = dirname(abspath(__file__))
    simsoSchedPath = dirname(abspath(simso.schedulers.__file__))
    for schedName in schedNames:
        if schedName[-3:] == '.py':
            p = os.path.join(currPath,'schedulers',schedName)
            assert os.path.isfile(p), f'Scheduler File {schedName} is invalid'
            schedPaths.append(p)
        else:
            schedFile = schedName.split('.')[-1] + '.py'
            p = os.path.join(simsoSchedPath,schedFile)
            assert os.path.isfile(p), f'Default scheduler {schedName} is invalid'
            schedPaths.append(p)
    args.schedNames,args.schedPaths = schedNames, schedPaths
    
    # Check and manage configuration
    configFileNames,configPaths = [],[]
    if args.configFileNames:
        configPaths = [os.path.join(currPath,'ConfigurationFiles',x) for x in \
                                                        args.configFileNames]
        for configFilePath in configPaths:
            assert os.path.isfile(configFilePath), \
                f'Config File {args.configFilePath} is invalid'
    else:
        for filename in os.listdir(os.path.join(currPath,'ConfigurationFiles')):
            configFileNames.append(filename)
            if filename[-4:] == '.xml':
                configPaths.append(os.path.join(currPath,
                                    'ConfigurationFiles', filename))
        args.configFileNames = configFileNames
    args.configPaths = configPaths

    # simMod = importlib.util.find_spec(f'simulators.{args.simModuleName}')
    # assert simMod is not None, f'Simulator module {args.simModuleName} does not exist.'
    return args

'''
Modifies XML file for a specified scheduler. Adds scheduling path to the
className attribute in sched and writes changes to file.
Parameters:
- configPath: absolute path for config
- schedPath: absolute path of scheduler
'''
def modifyXML(configPath,schedPath):
    xmlTree = ET.parse(configPath)
    xmlTree.getroot().findall('sched')[0].set('className',schedPath)
    xmlTree.write(configPath)




if __name__ == '__main__':
    main( check_args( parse_args() ) )