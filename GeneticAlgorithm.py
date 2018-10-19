import random

class GeneticAlgorithm():

    def __init__(self, listOfTasks, numberOfChromosomes, crossoverTechnique):
        self.listOfChromosomes = []
        self.numberOfChromosomes = numberOfChromosomes
        self.initial_population(listOfTasks)

    def initial_population(self, listOfTasks):
        
        for x in range(0, self.numberOfChromosomes):
            chromosome = Chromosome()
            shuffeledTasks = random.shuffle(listOfTasks)
            

    def crossover(self):
        pass

    def mutate(self):
        pass

    def evaluate_fitness(self):
        pass

    def genetic_algorithm(self, model):
        pass









class Chromosome():

    def __init__(self):
        self.taskToPriorityDict = {}

    def insert_task(self, task,priority):
        self.taskToPriorityDict[task] = priority

    def update_task(self, task, priority):
        if(task in self.taskToPriorityDict):
            self.taskToPriorityDict[task] = priority

class Task():

    def __init__(self, deadline, arrival_time, wcet):
        self.deadline = deadline
        self.arrival_time = arrival_time
        self.wcet = wcet

