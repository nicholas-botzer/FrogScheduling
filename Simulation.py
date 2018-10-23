import sys
from simso.core import Model
from simso.configuration import Configuration
from GeneticAlgorithm import GeneticAlgorithm
from Results import Results

def chooseOptimalChromosome(chromosomeList):
    bestFitnessScore = 9999999
    bestChromosome = None
    for chromosome in chromosomeList:
        fitnessScore = chromosome.fitnessScore

        if(fitnessScore < bestFitnessScore):
            bestFitnessScore = fitnessScore
            bestChromosome = chromosome

    return bestChromosome


def main(argv):
    argv = [0,"./ConfigurationFiles/config_2_20_0.xml"]
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
    geneticAlgorithm = GeneticAlgorithm(model.task_list, 40)

    #Run genetic algorithm
    for x in range(0,10):
        for chromosome in geneticAlgorithm.chromosomeList:
            model = Model(configuration)
            #set chromosome for model to use
            model.scheduler.initializeChromosome(chromosome)
            # Execute the simulation.
            model.run_model()
            #evaluate fitness
            chromosome.evaluate_fitness(model)

        # on last run DO NOT DO THE BELOW OPERATIONS
        bestChromosome = chooseOptimalChromosome(geneticAlgorithm.chromosomeList)
        print("Best fitness Score: " , str(bestChromosome.fitnessScore))

        #Perform the selection, crossover, and mutation 
        nextChromosomeGenerationList = geneticAlgorithm.selection(30)
        childChromosomeList = geneticAlgorithm.crossover(nextChromosomeGenerationList, 5) #returns 4

        # print(childChromosomeList)
        nextChromosomeGenerationList.extend(childChromosomeList)
        
        #set the GA's list of chromosomes to this new list
        geneticAlgorithm.chromosomeList = nextChromosomeGenerationList

        #mutate the generation before running again
        geneticAlgorithm.mutate()


    Results(bestChromosome.model).print_results()


main(sys.argv)