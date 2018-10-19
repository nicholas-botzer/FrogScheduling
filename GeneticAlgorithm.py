import random

class GeneticAlgorithm():

    def __init__(self, taskList, numberOfChromosomes=10, crossoverTechnique=None):
        self.chromosomeList = []
        self.numberOfChromosomes = numberOfChromosomes
        self.initial_population(taskList)

    """
        Initializes the chromosome's for the GA
        Args:
            - `taskList`: The list of tasks for the simulation

    """
    def initial_population(self, taskList):
        for x in range(0, self.numberOfChromosomes):
            chromosome = Chromosome()
            random.shuffle(taskList)
            priority = 1
            for task in taskList:
                chromosome.insert_task(task, priority)
                priority += 1
            
            self.chromosomeList.append(chromosome)
                        
    def selection(self):
        pass

    def crossover(self):
        pass

    def mutate(self):
        pass

    def evaluate_fitness(self, model):
        pass

    def genetic_algorithm(self, model, iterations=None):
        
        # Execute the simulation.
        model.run_model()


    def getAverageNormalizedLaxity(self, model):
        count = 0
        totalNormalizedLaxity = 0
        for task in model.results.tasks.values():
            for job in task.jobs:
                if(job.task.deadline and job.response_time):
                    totalNormalizedLaxity += job.normalized_laxity
                    count += 1

        return totalNormalizedLaxity / count









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

