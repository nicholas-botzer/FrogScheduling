from tools.ga.chromosome import Chromosome
from tools.ga.chromosome_task import ChromosomeTask
from tools.ga.crossovers import Crossovers
from tools.ga.selection import Selection
import random

"""
Container for all chromosomes and their modifications. A new object instance
is created for each config run.
"""
class GeneticAlgorithm:

    def __init__(self, taskList, numberOfChromosomes=10, 
        crossoverTechnique=None, shuffleTaskPriority=True,elitePercent=0.10,
        selectionPercent=0.50, crossOverPercent=0.40, mutationRate=0.01):
        self.chromosomeList = []
        self.numberOfChromosomes = numberOfChromosomes
        self.initial_population(taskList,shuffleTaskPriority)
        self.numOfEliteChromosomes = self.calculateNumberOfChromosomes(elitePercent)
        self.numOfSelectionChromosomes = self.calculateNumberOfChromosomes(selectionPercent)
        #cross over returns two chromosomes so we only need half the value for looping
        self.numOfCrossOverChromosomes = round(self.calculateNumberOfChromosomes(crossOverPercent) / 2)
        self.mutationRate = mutationRate

    '''
        Initializes the chromosome's for the GA
        Args:
            - `taskList`: The list of tasks for the simulation
        Return:
            - Nothing, just creates the initial population for the class

    '''
    def initial_population(self, taskList, shuffle=True):
        for _ in range(self.numberOfChromosomes):
            chromosome = Chromosome()
            if shuffle:
                random.shuffle(taskList)
            priority = 0
            for task in taskList:
                chromosome.insert_task(task, priority)
                priority += 1
        
            self.chromosomeList.append(chromosome)

    '''
        Selects the number of chromosomes that will live on to the next generation
        Args: N/A
        Return:
            - List of chromosomes that will live on
    '''          
    def selection(self):
        chromosomesToLiveList = []

        self.normalizeFitnessScores()

        chromosomesToLiveList.extend(Selection.selectElitePopulation(
            self.chromosomeList, self.numOfEliteChromosomes))

        #Perform roulette wheel selection
        for _ in range (self.numOfSelectionChromosomes):
            chromosomesToLiveList.append(Selection.rouletteWheelSelection(self.chromosomeList))
        
        return chromosomesToLiveList


    '''
    Args
    - parentChromosomesList: chromosomes selected to be the parents
    - numberOfChildrenDesired: maximum value in partition range
    Return
    - list of new chromosomes created from the parent chromosomes
    '''
    def crossover(self, parentChromosomesList):

        newChromosomesList = []
        for x in range(0, (self.numOfCrossOverChromosomes)):
            parentOneChromosome = Selection.rouletteWheelSelection(parentChromosomesList)
            parentTwoChromosome = Selection.rouletteWheelSelection(parentChromosomesList)

            newChromosomeOne = Chromosome()
            newChromosomeTwo = Chromosome()

            newChromosomeOne.taskToPriorityDict, \
            newChromosomeTwo.taskToPriorityDict = \
                Crossovers.OX2(parentOneChromosome.taskToPriorityDict, \
                parentTwoChromosome.taskToPriorityDict)


            newChromosomesList.append(newChromosomeOne)
            newChromosomesList.append(newChromosomeTwo)

        return newChromosomesList

                
    def mutate(self):
        for chromosome in self.chromosomeList:

            mutationChance = random.uniform(0,100)
            if(mutationChance < self.mutationRate):
                #time to mutateL!!!
                dictionary = chromosome.taskToPriorityDict
                key1, key2 = random.sample(list(dictionary), 2)
                dictionary[key1], dictionary[key2] = dictionary[key2], dictionary[key1]




######## HELPER FUNCTIONS #######################################################

    def normalizeFitnessScores(self):
        #normalize fitness scores before performing roulette wheel selection
        highestFitnessScore = max(self.chromosomeList, key = lambda x: (x.fitnessScore)).fitnessScore

        #If all fitness scores are not equal need to normalize before roulette wheel selection
        if not all(x.fitnessScore == self.chromosomeList[0].fitnessScore for x in self.chromosomeList):
            for chromosome in self.chromosomeList:
                chromosome.fitnessScore = highestFitnessScore - (chromosome.fitnessScore)


    def calculateNumberOfChromosomes(self, percent):
        return round(self.numberOfChromosomes * percent)

