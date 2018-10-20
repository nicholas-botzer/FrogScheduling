import random
from Chromosome import Chromosome
from ChromosomeTask import ChromosomeTask

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
                chromosomeTask = ChromosomeTask(task.deadline, task.arrival_time, task.wcet)
                chromosome.insert_task(chromosomeTask, priority)
                priority += 1
            
            self.chromosomeList.append(chromosome)
                        
    def selection(self):
        pass

    def crossover(self):
        pass

    def mutate(self):
        pass

    def evaluate_fitness(self, model):

        missedDeadlinesScore = 1 - (model.results.total_exceeded_count / len(model.taks))

        fitnessScore = missedDeadlinesScore + self.getAverageNormalizedLaxity(model)

        # print("Total Migrations: " + str(model.results.total_migrations))
        # print("Total Pre-emptions: " + str(model.results.total_preemptions))
        # print("Total Exceeded Count: " + str(model.results.total_exceeded_count))

        return fitnessScore

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
