import sys, logging
logging.basicConfig(format='%(message)s',stream=sys.stderr, level=logging.DEBUG)
from simso.core import Model
from simso.configuration import Configuration
from GeneticAlgorithm import GeneticAlgorithm
from Crossovers import Crossovers
from Debug import Debug

def main(argv):
    argv = [0,"./ConfigurationFiles/initialTest.xml"]
    configuration = None
    if len(argv) == 2:
        # Configuration load from a file.
        configuration = Configuration(argv[1])
    else:
        raise ValueError('invalid number of args')

    # Check the config before trying to run it.
    configuration.check_all()

    # Init a model from the configuration.
    model = Model(configuration)

    #initial population
    geneticAlgorithm = GeneticAlgorithm(model.task_list,shuffleTaskPriority=)

    #Run genetic algorithm
    for x in range(0,20):
        for chromosome in geneticAlgorithm.chromosomeList:
            #set chromosome for model to use
            model.scheduler.initializeChromosome(chromosome)
            # Execute the simulation.
            logging.debug(Debug.getTaskListStr(chromosome.taskToPriorityDict,
                                     name='Chromosome Task Priorities'))
            model.run_model()
            sys.exit(0)
            #evaluate fitness
            chromosome.evaluate_fitness(model)

        #Perform the selection, crossover, and mutation 
        nextChromosomeGenerationList = geneticAlgorithm.selection(8)
        childChromosomeList = geneticAlgorithm.crossover(nextChromosomeGenerationList, 4)

        # print(childChromosomeList)
        nextChromosomeGenerationList.extend(childChromosomeList)
        
        #set the GA's list of chromosomes to this new list
        geneticAlgorithm.chromosomeList = nextChromosomeGenerationList

        #mutate the generation before running again
        geneticAlgorithm.mutate()



main(sys.argv)