from simso.core import Model
from simso.configuration import Configuration
from tools.ga.organism import Organism
from tools.ga.change_chromosomes import ChangeChromosomes
from tools.ga.chromosome import Chromosome
from tools.results import Results
from tools.debug import Debug

import sys, logging, time
logger = logging.getLogger('root')


"""
Main gets called from simulate.py.
One execution of main represents one organism's entire lifecycle given
its own config file.
"""
def main(args):

    # Load configuration file and check
    configPath = args.configPaths[args.currentConfigIdx]
    configuration = Configuration(configPath)
    configuration.check_all()

    # Init a model from the configuration.
    model = Model(configuration)

    #initial population
    organism = Organism( model.task_list,args.numChrom, 
        shuffleTaskPriority=True, elitePercent=args.ESCperc[0], 
        selectionPercent=args.ESCperc[1], crossOverPercent=args.ESCperc[2], 
        mutationRate=args.mutRate, configFile=configPath)

    # results = Results()
    optimalOverallChromosome = None

    #Run genetic algorithm
    for gen in range(args.numGen):
        organism.checkValid()
        logger.log(15, f"\n---------------\n[Iteration Num {gen+1}]")
        logger.log(15,f"Running generation {gen+1}..")
        startTime = time.time()
        for chromosome in organism.chromList:
            #set chromosome for model to use
            model = Model(configuration)
            model.scheduler.initializeChromosome(chromosome)
            # Execute the simulation.
            logger.log(3, Debug.getTaskListStr(chromosome.taskNameToPriority,
                                     name='Chromosome Task Priorities'))
            model.run_model()
            chromosome.fitness.updateAllFitnessMetrics(model)
            del model
        endTime = time.time()
        logger.log(15,f"..Gen {gen+1} running complete. (Time: {endTime-startTime:.2f} secs).")
        ## After all chromosomes in organism has run...
        #  Record statistics via logging and internally
        bestChromList = organism.getSortedChromList()
        
        for i in range(3):
            chrom = bestChromList[i]
            logger.log(15, f"Rank {i+1} - Fitness: {chrom.fitness.getFitnessScore()}," \
                        f" Migrations: {chrom.fitness.getMigrations()}," \
                        f" Preemptions: {chrom.fitness.getPreemptions()}," \
                        f" Exceeded Count: {chrom.fitness.getExceededCount()}")

        if gen == 0:
            optimalOverallChromosome = bestChromList[0]
        elif gen > 0 and (bestChromList[0].fitness.getFitnessScore() < \
                  optimalOverallChromosome.fitness.getFitnessScore()):
            optimalOverallChromosome = bestChromList[0]

        #Perform the selection, crossover, and mutation
        organism.checkValid()
        organism.goNextGen(bestChromList=bestChromList)

    ## Generations have fully ran..
    #  Recording statistics to file from internals
    #results.setOptimalChromosome(optimalChromosome)
    #results.print_results(optimalChromosome.model)
    Results.outputStatsForRun(args.resultsFN, 
                             args.configFileNames[args.currentConfigIdx],
                             args.schedNames[args.currentSchedIdx],
                             organism)
    


if __name__ == '__main__':
    main(sys.argv)
