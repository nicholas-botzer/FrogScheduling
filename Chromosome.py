class Chromosome:

    def __init__(self):
        self.taskToPriorityDict = {}
        self.fitnessScore = 0

    def insert_task(self, task,priority):
        self.taskToPriorityDict[task.name] = priority

    def update_task(self, task, priority):
        if(task in self.taskToPriorityDict):
            self.taskToPriorityDict[task.name] = priority


    '''
        Initializes the chromosome's for the GA
        Args:
            - `model`: The model of the simulation after it has ran
        Return:
            - Fitness for the given model

    '''
    def evaluate_fitness(self, model):

        self.fitnessScore = model.results.total_exceeded_count
        # print(str(self.fitnessScore))
        self.model = model

    def getAverageNormalizedLaxity(self, model):
        count = 0
        totalNormalizedLaxity = 0
        for task in model.results.tasks.values():
            for job in task.jobs:
                if(job.task.deadline and job.response_time):
                    totalNormalizedLaxity += job.normalized_laxity
                    count += 1

        return totalNormalizedLaxity / count