import sys, logging
from simso.core import Model
from simso.configuration import Configuration
from tools.ga.genetic_algorithm import GeneticAlgorithm
from tools.ga.crossovers import Crossovers
from tools.ga.chromosome import Chromosome
from tools.results import Results
from tools.debug import Debug

def chooseOptimalChromosome(chromosomeList):
    bestFitnessScore = 9999999
    bestChromosome = None
    for chromosome in chromosomeList:
        fitnessScore = chromosome.fitnessScore

        if(fitnessScore < bestFitnessScore):
            bestFitnessScore = fitnessScore
            bestChromosome = chromosome

    return bestChromosome

def main(args):
    logger = logging.getLogger('root')
    configuration = None
    # Configuration load from a file.
    configuration = Configuration(args.configPath)
    

    # Check the config before trying to run it.
    configuration.check_all()

    # Init a model from the configuration.
    model = Model(configuration)

    #initial population
    geneticAlgorithm = GeneticAlgorithm(model.task_list,args.numChrom, shuffleTaskPriority=True,
        elitePercent=args.ESCperc[0], selectionPercent=args.ESCperc[1] ,crossOverPercent=args.ESCperc[2], mutationRate=args.mutRate )

    results = Results()

    optimalChromosome = Chromosome()

    #Run genetic algorithm
    for x in range(0,args.numGen):
        for chromosome in geneticAlgorithm.chromosomeList:
            #set chromosome for model to use
            model = Model(configuration)
            model.scheduler.initializeChromosome(chromosome)
            # Execute the simulation.
            logger.info(Debug.getTaskListStr(chromosome.taskToPriorityDict,
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
    results.createOutputFile(args.resultFN,args.config,args.simulator,optimalChromosome.model)
    results.print_results(optimalChromosome.model)


if __name__ == '__main__':
    main(sys.argv)
