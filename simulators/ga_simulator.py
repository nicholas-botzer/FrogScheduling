from simso.core import Model
from simso.configuration import Configuration
from tools.ga.organism import Organism
from tools.ga.change_chromosomes import ChangeChromosomes
from tools.ga.chromosome import Chromosome
from tools.results import Results
from tools.debug import Debug

import sys, logging, time
logger = logging.getLogger('root')

PRINTTOP = 5

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
    organism = Organism( args, model.task_list, args.numChrom, 
        shuffleTaskPriority=True, elitePercent=args.ESCperc[0], 
        selectionPercent=args.ESCperc[1], crossOverPercent=args.ESCperc[2], 
        mutationRate=args.mutRate)

    #Run genetic algorithm
    for gen in range(args.numGen):
        organism.checkValid()
        logger.log(15, "\n---------------\n" + \
                      f"Running generation {gen+1}..")
        runStartTime = time.time()
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
        runEndTime = time.time()
        logger.log(15,f"..Gen {gen+1} running complete. (Time: {runEndTime-runStartTime:.2f} secs).\n")
        ## After all chromosomes in organism has run...
        #  Record statistics via logging and internally
        bestChromList = organism.getSortedChromList()
        totFS, totMig, totPre, totNL, totEC, totChrom = 0.0, 0.0, 0.0, 0.0, 0.0, args.numChrom
        for rank,chrom in enumerate(bestChromList):
            chrom.addRank(rank)
            if rank < PRINTTOP:
                logger.log(15, f"Rank {rank+1} - Fitness: {chrom.fitness.getFitnessScore()}," \
                        f" Migrations: {chrom.fitness.getMigrations()}," \
                        f" Preemptions: {chrom.fitness.getPreemptions()}," \
                        f" NL: {chrom.fitness.getNormalizedLaxity():.4f}," \
                        f" Exceeded Count: {chrom.fitness.getExceededCount()}")
            totFS += chrom.fitness.getFitnessScore()
            totMig += chrom.fitness.getMigrations()
            totPre += chrom.fitness.getPreemptions()
            totNL += chrom.fitness.getNormalizedLaxity()
            totEC += chrom.fitness.getExceededCount()
        logger.log(15, f"AVERAGE - Fitness: {totFS/totChrom}," \
                        f" Migrations: {totMig/totChrom:.1f}," \
                        f" Preemptions: {totPre/totChrom:.1f}," \
                        f" NL: {totNL/totChrom:.4f}," \
                        f" Exceeded Count: {totEC/totChrom:.1f}")
        organism.avgFitnessDict['FitnessScore'].append(totFS/totChrom)
        organism.avgFitnessDict['Migrations'].append(totMig/totChrom)
        organism.avgFitnessDict['Preemptions'].append(totPre/totChrom)
        organism.avgFitnessDict['NormalizedLaxity'].append(totNL/totChrom)
        organism.avgFitnessDict['ExceededCount'].append(totEC/totChrom)


        #Perform the selection, crossover, and mutation
        organism.checkValid()
        organism.goNextGen(bestChromList=bestChromList)
        logger.log(15,f"\n(Organism & Chromosome overhead: {time.time()-runEndTime:.2f} secs)")

    Results.outputStatsForRun(organism)
    return organism
    


if __name__ == '__main__':
    main(sys.argv)
