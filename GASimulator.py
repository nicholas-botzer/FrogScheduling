import sys, logging
logging.basicConfig(format='%(message)s',stream=None, level=logging.NOTSET)
from simso.core import Model
from simso.configuration import Configuration
from GeneticAlgorithm import GeneticAlgorithm
from Crossovers import Crossovers
from Results import Results
from Debug import Debug

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

    #Run genetic algorithm
    for x in range(0,20):
        for chromosome in geneticAlgorithm.chromosomeList:
            #set chromosome for model to use
            model = Model(configuration)
            model.scheduler.initializeChromosome(chromosome)
            # # Execute the simulation.
            logging.debug(Debug.getTaskListStr(chromosome.taskToPriorityDict,
                                     name='Chromosome Task Priorities'))
            model.run_model()

            # Debug.printGanttPerCPU(model.scheduler.ganttData)
            # Results(model).print_results()
            
            #evaluate fitness
            chromosome.evaluate_fitness(model)

        bestChromosome = chooseOptimalChromosome(geneticAlgorithm.chromosomeList)
        print("Iteration Number: ", x)
        print("Best Fitness Score: ", bestChromosome.fitnessScore)
        Results(bestChromosome.model).print_results()


        #Perform the selection, crossover, and mutation 
        nextChromosomeGenerationList = geneticAlgorithm.selection()
        childChromosomeList = geneticAlgorithm.crossover(nextChromosomeGenerationList)

        # print(childChromosomeList)
        nextChromosomeGenerationList.extend(childChromosomeList)
        
        #set the GA's list of chromosomes to this new list
        geneticAlgorithm.chromosomeList = nextChromosomeGenerationList

        #mutate the generation before running again
        geneticAlgorithm.mutate()


if __name__ == '__main__':
    main(sys.argv)
