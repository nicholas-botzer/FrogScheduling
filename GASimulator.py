import sys, logging
logging.basicConfig(format='%(message)s',stream=None, level=logging.NOTSET)
from simso.core import Model
from simso.configuration import Configuration
from GeneticAlgorithm import GeneticAlgorithm
from Crossovers import Crossovers
from Results import Results
from Debug import Debug
from Chromosome import Chromosome

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
    # argv = [0,"./ConfigurationFiles/FS_baseTest.xml"]
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
    geneticAlgorithm = GeneticAlgorithm(model.task_list,30, shuffleTaskPriority=True)

    results = Results()

    optimalChromosome = Chromosome()

    #Run genetic algorithm
    for x in range(0,4):
        for chromosome in geneticAlgorithm.chromosomeList:
            #set chromosome for model to use
            model = Model(configuration)
            model.scheduler.initializeChromosome(chromosome)
            # Execute the simulation.
            logging.debug(Debug.getTaskListStr(chromosome.taskToPriorityDict,
                                     name='Chromosome Task Priorities'))
            model.run_model()
            
            #evaluate fitness
            chromosome.evaluate_fitness(model)


        bestGenerationChromosome = chooseOptimalChromosome(geneticAlgorithm.chromosomeList)

        print("Iteration Number: ", x)
        print("Best Fitness Score: ", bestGenerationChromosome.fitnessScore)
        results.insertNewGeneration(x, geneticAlgorithm.chromosomeList)
        results.print_results(bestGenerationChromosome.model)

        if(x == 0):
            optimalChromosome = bestGenerationChromosome
        #set optimal chromosome
        if(x > 0 and bestGenerationChromosome.fitnessScore < optimalChromosome.fitnessScore):
            optimalChromosome = bestGenerationChromosome

        
        #Perform the selection, crossover, and mutation 
        nextChromosomeGenerationList = geneticAlgorithm.selection()
        childChromosomeList = geneticAlgorithm.crossover(nextChromosomeGenerationList)

        # print(childChromosomeList)
        nextChromosomeGenerationList.extend(childChromosomeList)
        
        #set the GA's list of chromosomes to this new list
        geneticAlgorithm.chromosomeList = nextChromosomeGenerationList

        #mutate the generation before running again
        geneticAlgorithm.mutate()

    results.setOptimalChromosome(optimalChromosome)
    results.createOutputFile("testOutput.csv","testConfig","testSched",optimalChromosome.model)
    results.print_results(optimalChromosome.model)


if __name__ == '__main__':
    main(sys.argv)
