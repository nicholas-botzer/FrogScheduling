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

    # Execute the simulation.
    model.run_model()

    geneticAlgorithm = GeneticAlgorithm(model.task_list)

    #Run genetic algorithm
    for x in range(0,20):
        for chromosome in geneticAlgorithm.chromosomeList:
            # Execute the simulation.
            model.scheduler.initializeTaskToPriorityDict(chromosome.taskToPriorityDict)
            model.run_model()

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