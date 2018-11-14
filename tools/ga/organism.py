from tools.ga.chromosome import Chromosome
from tools.ga.change_chromosomes import ChangeChromosomes
from collections import defaultdict
import random, logging
logger = logging.getLogger('root')

"""
Container for all chromosomes and their modifications. A new object instance
is created for each config run.
"""
class Organism:

    def __init__(self, args, taskList, numberOfChromosomes=10, 
        crossoverTechnique=None, shuffleTaskPriority=True, elitePercent=0.10,
        selectionPercent=0.50, crossOverPercent=0.40, mutationRate=0.01):

        self.metadataDict = {
            'ConfigFile' : args.configFileNames[args.currentConfigIdx],
            'ResultsFilePath' : args.resultsFilePath,
            'SchedulerName' : args.schedNames[args.currentSchedIdx] 
        }
        self.avgFitnessDict = {
            'ExceededCount' : [], 
            'Preemptions' : [], 
            'Migrations' : [],
            'NormalizedLaxity' : [],
            'FitnessScore' : []
        }
        self.chromList = []
        self.optimalChromList = []

        self.currentGen = 0

        self.numTasks = len(taskList)
        self.numberOfChromosomes = numberOfChromosomes
        self.initial_population(taskList,shuffleTaskPriority)
        self.numOfEliteChromosomes = self.calculateNumberOfChromosomes(elitePercent)
        self.numOfSelectionChromosomes = self.calculateNumberOfChromosomes(selectionPercent)
        #cross over returns two chromosomes so we only need half the value for looping
        self.numOfCrossOverChromosomes = round(self.calculateNumberOfChromosomes(crossOverPercent))
        self.mutationRate = mutationRate

    '''
    Initializes the chromosome's for the GA called by constructor.
    Args:
        - `taskList`: The list of tasks for the simulation
    '''
    def initial_population(self, taskList, shuffle=True):
        for i in range(self.numberOfChromosomes):
            if shuffle:
                random.Random(3).shuffle(taskList)
            chromosome = Chromosome(taskList, name=i)
            self.chromList.append(chromosome)

    ############### NEXT GENERATION FUNCTIONALITY ############# 
    '''
    This is called from simulator.main and is run after the model is done
    executing one generation. TASKS here include:
        1. Invokes select, crossover, mutate to get new chromList
        2. Archiving old priority lists in each chrom and putting in the new list
        3. Saves statistics into chromosome stats data structures
    (NOTE: Make sure new dicts don't modify old dict objects)
    '''
    def goNextGen(self,bestChromList):
        # Archive current priority dict and create empty lists for ops
        self.saveAllPriorityDictsAndInstantiateChromOpLists()
        self.optimalChromList.append(bestChromList)
        self.currentEliteSet = set(bestChromList[:self.numOfEliteChromosomes])
        
        # Calculate inverse fitness and get max
        maxFitness = float(max([c.fitness.getFitnessScore() for c in self.chromList]))
        sumInvFS = 0.0
        for c in self.chromList:
            invScore = (maxFitness - c.fitness.getFitnessScore()) + 1
            c.inverseFitnessScore = invScore
            sumInvFS += invScore
        logger.log(10, '\nElite: ' + str(bestChromList[:self.numOfEliteChromosomes]))
        
        # SELECT / CROSSOVER / MUTATE
        self.select(bestChromList[self.numOfEliteChromosomes:], sumInvFS)
        self.crossover(self.currentEliteSet, self.chromList, sumInvFS)
        self.mutateChromosomes(self.chromList,mr=self.mutationRate)
        
        self.currentGen += 1
        
    
    def select(self,selChromList,sumInvFS):
        chromosomesSelected = []
        while(len(chromosomesSelected) < self.numOfSelectionChromosomes):
            chromPicked = ChangeChromosomes.rouletteWheelSelection(
                                                        selChromList,sumInvFS)
            if chromPicked not in chromosomesSelected and chromPicked:
                chromosomesSelected.append(chromPicked)
        self.mutateChromosomes(chromosomesSelected,mr=self.mutationRate*5)    
        return chromosomesSelected


    '''
    Args
    - parentChromosomesList: chromosomes selected to be the parents
    - numberOfChildrenDesired: maximum value in partition range
    Return
    - list of new chromosomes created from the parent chromosomes
    '''
    def crossover(self, chosenSet, fullList, sumInvFS):

        for _ in range(self.numOfCrossOverChromosomes):
            C1 = ChangeChromosomes.rouletteWheelSelection(fullList,sumInvFS)
            C2 = C1
            while(C2 is C1 or C2 is None):
                C2 = ChangeChromosomes.rouletteWheelSelection(fullList,sumInvFS)

            C1dict, C2dict = C1.taskNameToPriority, C2.taskNameToPriority
            newC1dict, newC2dict = ChangeChromosomes.OX2Cross(C1dict,C2dict)
            logger.log(5,f"{C1.name} and {C2.name} chosen for crossover")
            if C1 not in chosenSet:
                logger.log(5,f"Setting new dict to {C1.name}")
                C1.taskNameToPriority = newC1dict
                C1.statsDict['OpsList'][-1].append(f'Crossed {C1.name} {C2.name}')
            if C2 not in chosenSet:
                logger.log(5,f"Setting new dict to {C2.name}")
                C2.taskNameToPriority = newC2dict
                C2.statsDict['OpsList'][-1].append(f'Crossed {C1.name} {C2.name}')

    '''
    Assigns current chromosome priority dict to new mutated dict.
    '''
    def mutateChromosomes(self,chromList,mr):
        for chromosome in chromList:
            rnum = random.uniform(0,100)
            if(rnum < mr): # mutate
                maxr = int(self.numTasks*0.05) if int(self.numTasks*0.05) > 2 else 2
                numruns = random.randint(1,maxr)
                newDict = dict(chromosome.taskNameToPriority)
                if chromosome in self.currentEliteSet:
                    logger.log(10,f"\t-----> MUTATING ELITE CHROMOSOME ({chromosome.name})")
                for run in range(numruns):
                    k1,k2 = random.sample(list(newDict), 2)
                    newDict[k1], newDict[k2] = newDict[k2], newDict[k1]
                    logger.log(10,f"Mutating k1({k1}) and k2({k2}) in" \
                        f" chromosome ({chromosome.name})")
                    chromosome.statsDict['OpsList'][-1].append(f'Mutated {k1} {k2}')
                chromosome.taskNameToPriority = newDict


    '''
    1. Saves current priority dictionaries for all chromosomes.
    2. Adds empty lists to stats['OpsList'] to store so that cross/mutate can record.
    '''
    def saveAllPriorityDictsAndInstantiateChromOpLists(self):
        for chrom in self.chromList:
            chrom.saveCurrentPriorityDict()
            chrom.statsDict['OpsList'].append([])


    ############### STATISTICS FUNCTIONALITY ############# 

    def calculateNumberOfChromosomes(self, percent):
        return round(self.numberOfChromosomes * percent)

    def getSortedChromList(self):
        score_chrom = []
        for chrom in self.chromList:
            score_chrom.append((chrom.fitness.getFitnessScore(),chrom))
        return [x[1] for x in sorted(score_chrom,reverse=False,key=lambda x: x[0])]

    ############### HELPER FUNCTIONS #############
    '''
    Checks if current state of the organism is valid.
      - Every chromosome has a valid priority list and history
      - Every chromosome has valid fitness statistics history
    '''
    def checkValid(self):
        # Check parameters
        assert self.numberOfChromosomes == len(self.chromList), \
               f'Length of chromList ({len(self.chromList)})doesn\'t match number of' \
               f'chromosomes ({self.numberOfChromosomes})'
        assert self.numOfEliteChromosomes + self.numOfCrossOverChromosomes + \
               self.numOfSelectionChromosomes == self.numberOfChromosomes, \
               f'ECS ({self.numOfEliteChromosomes})({self.numOfCrossOverChromosomes})({self.numOfSelectionChromosomes}) != ({self.numberOfChromosomes})number of chromosomes.'
        # Check chromosomes and their fitness
        for idx,chrom in enumerate(self.chromList):
            assert chrom is not None, 'chromList has None object!'
            assert isinstance(chrom,Chromosome), 'chromList has non-chromosome object!'
            # Check chrom current priority list
            pd = chrom.taskNameToPriority
            assert pd is not None and len(pd) == self.numTasks, \
                   f'Chrom ({idx}) dict is not valid'
            ts, ps = set(), set()
            for tn,p in chrom.taskNameToPriority.items():
                assert isinstance(tn,str), 'Task name not a string'
                assert isinstance(p,int), 'Priority is not an int'
                ts.add(tn)
                ps.add(p)
            assert len(ts) == self.numTasks, 'Num tasks in chrom dict not valid!'
            assert len(ps) == self.numTasks, 'Num priorities in chrom dict not valid!'
            assert max(ps) == self.numTasks-1, f'Priorities max {max(ps)} not {self.numTasks-1}'
            assert min(ps) == 0, f'Priorities min {min(ps)} not 0'
                
            
