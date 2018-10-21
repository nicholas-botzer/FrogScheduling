import random
from Chromosome import Chromosome
from ChromosomeTask import ChromosomeTask
from Crossovers import Crossovers

class GeneticAlgorithm():

    def __init__(self, taskList, numberOfChromosomes=10, crossoverTechnique=None):
        self.chromosomeList = []
        self.numberOfChromosomes = numberOfChromosomes
        self.initial_population(taskList)

    '''
        Initializes the chromosome's for the GA
        Args:
            - `taskList`: The list of tasks for the simulation
        Return:
            - Nothing, just creates the initial population for the class

    '''
    def initial_population(self, taskList):
        for x in range(0, self.numberOfChromosomes):
            chromosome = Chromosome()
            random.shuffle(taskList)
            priority = 0
            for task in taskList:
                chromosomeTask = ChromosomeTask(task.name, task.deadline, task._task_info.activation_date, task.wcet)
                chromosome.insert_task(chromosomeTask, priority)
                priority += 1
        
            self.chromosomeList.append(chromosome)

    '''
        Selects the number of chromosomes that will live on to the next generation
        Args: N/A
        Return:
            - List of chromosomes that will live on
    '''          
    def selection(self, numberOfChromosomesToLive):
        chromosomesToLiveList = []
        for x in range (0,numberOfChromosomesToLive):
            chromosomesToLiveList.append(self.roulette_wheel_selection())
        
        return chromosomesToLiveList

    '''
        Performs a roulette wheel selection the the chromosome list to get a chromosome
        Args: N/A
        Return:
            - Chromosome selected to continue living it's life
    '''
    def roulette_wheel_selection(self):
        max = sum(chromosome.fitnessScore for chromosome in self.chromosomeList)
    
        pick = random.uniform(0, max)
        current = 0
        for chromosome in self.chromosomeList:
            current += chromosome.fitnessScore
        if current > pick:
            return chromosome

    '''
    Args
    - parentChromosomesList: chromosomes selected to be the parents
    - numberOfChildrenDesired: maximum value in partition range
    Return
    - list of new chromosomes created from the parent chromosomes
    '''
    def crossover(self, parentChromosomesList, numberOfChildrenDesired=0):

        newChromosomesList = []
        for x in range(0,numberOfChildrenDesired):
            parentOneIndex = random.randint(0, len(parentChromosomesList)-1)
            parentTwoIndex = random.randint(0, len(parentChromosomesList)-1)

            newChromosome = Chromosome()


            print("Dict 1 " , parentChromosomesList[parentOneIndex].taskToPriorityDict)
            print("Dict 2 " , parentChromosomesList[parentTwoIndex].taskToPriorityDict)

            newChromosome.taskToPriorityDict = Crossovers.OX1(parentChromosomesList[parentOneIndex].taskToPriorityDict,
                parentChromosomesList[parentTwoIndex].taskToPriorityDict)


            newChromosomesList.append(newChromosome)
            print(newChromosome)

        return newChromosomesList

                
    def mutate(self):
        pass