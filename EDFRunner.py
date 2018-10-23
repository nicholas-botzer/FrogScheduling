import sys, logging
logging.basicConfig(format='%(message)s',stream=sys.stderr, level=logging.DEBUG)
from simso.core import Model
from simso.configuration import Configuration
from Results import Results
from Debug import Debug

"""
Runs EDF (earliest deadline first) scheduling algorithm.
"""
def main(argv):
    argv = [0,"./ConfigurationFiles/EDF_baseTest.xml"]
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