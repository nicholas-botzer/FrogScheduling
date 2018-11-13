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
    
    # Load configuration file and check
    configPath = args.configPaths[args.currentConfigIdx]
    configuration = Configuration(configPath)
    configuration.check_all()

    # Init a model from the configuration.
    model = Model(configuration)

    # Execute the simulation.
    model.run_model()

    # Write results to csv file
    Results.outputDefResults(args,model)


if __name__ == '__main__':
    main(sys.argv)