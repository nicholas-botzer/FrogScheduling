import sys
from simso.core import Model
from simso.configuration import Configuration
from GeneticAlgorithm import GeneticAlgorithm

            
def main(argv):
    if len(argv) == 2:
        # Configuration load from a file.
        configuration = Configuration(argv[1])

    # Check the config before trying to run it.
    configuration.check_all()

    # Init a model from the configuration.
    model = Model(configuration)

    geneticAlgorithm = GeneticAlgorithm(model.task_list)

    # geneticAlgorithm.genetic_algorithm(model)


main(sys.argv)