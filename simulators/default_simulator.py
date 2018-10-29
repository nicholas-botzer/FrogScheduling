import sys, logging
from simso.core import Model
from simso.configuration import Configuration
from tools.results import Results
from tools.debug import Debug

logging.basicConfig(format='%(message)s',stream=sys.stderr, level=logging.DEBUG)

"""
Runs EDF (earliest deadline first) scheduling algorithm.
"""
def main(args):
    configuration = None
    # Configuration load from a file.
    configuration = Configuration(args.configPath)

    # Check the config before trying to run it.
    configuration.check_all()

    results = Results()

    # Init a model from the configuration.
    model = Model(configuration)

    # Execute the simulation.
    model.run_model()

    # Debug.printGanttPerCPU(model.scheduler.ganttData)
    print(args)
    results.createOutputFile(args.resultsFN,args.configFileName,args.simModuleName, model)

if __name__ == '__main__':
    main(sys.argv)