import sys, logging
from simso.core import Model
from simso.configuration import Configuration
from tools.results import Results
from tools.debug import Debug

logging.basicConfig(format='%(message)s',stream=sys.stderr, level=logging.DEBUG)

"""
Runs EDF (earliest deadline first) scheduling algorithm.
"""
def main(argv):
    if len(argv) == 2:
        # Configuration load from a file.
        configuration = Configuration(argv[1])
    else:
        # Manual configuration:
        configuration = Configuration()

    # Check the config before trying to run it.
    configuration.check_all()


    # Init a model from the configuration.
    model = Model(configuration)

    # Execute the simulation.
    model.run_model()

    Debug.printGanttPerCPU(model.scheduler.ganttData)

    Results(model).print_results()

if __name__ == '__main__':
    main(sys.argv)