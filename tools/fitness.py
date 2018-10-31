"""
Instantiable object that keeps track of fitness for a certain model.
Also contains all fuctions to calculate fitness related 
"""
from collections import defaultdict

class Fitness:

    ####### FITNESS FUNCTIONS ########
    def __init__(self):
        dictInstantiation = {'Total Exceeded Count' : [], 
                             'Total Preemptions' : [], 
                             'Total Migrations' : [],
                             'Schedule Overhead' : [],
                             'Activate Overhead' : [],
                             'Normalized Laxity' : [],
                             'Fitness Score' : []}
        self.metricToVal = defaultdict(list, **dictInstantiation)

    def updateAllFitnessMetrics(self,model):
        self.metricToVal['Total Exceeded Count'].append(model.results.total_exceeded_count)
        self.metricToVal['Total Preemptions'].append(model.results.total_preemptions)
        self.metricToVal['Total Migrations'].append(model.results.total_migrations)
        self.metricToVal['Schedule Overhead'].append(model.results.scheduler.schedule_overhead)
        self.metricToVal['Activate Overhead'].append(model.results.scheduler.activate_overhead)
        self.metricToVal['Normalized Laxity'].append(Fitness.getAverageNormalizedLaxity(model))
        self.metricToVal['Fitness Score'].append(self.calculateFitnessScore())

    def getFitnessCSVStr(self):
        self.checkValidDict()
        s = (f"{self.metricToVal['Total Exceeded Count'][-1]},"
             f"{self.metricToVal['Total Preemptions'][-1]},"
             f"{self.metricToVal['Total Migrations'][-1]},"
             f"{self.metricToVal['Normalized Laxity'][-1]},"
             f"{self.metricToVal['Schedule Overhead'][-1]},"
             f"{self.metricToVal['Activate Overhead'][-1]}")
        return s

    '''
    Returns various metrics given recent data...
    '''
    def calculateFitnessScore(self):
        fs = self.metricToVal['Total Exceeded Count'][-1] * 50 + \
             self.metricToVal['Total Preemptions'][-1]
        return fs
    def getFitnessScore(self):
        return self.metricToVal['Fitness Score'][-1]
    def getMigrations(self):
        return self.metricToVal['Total Migrations'][-1]
    def getPreemptions(self):
        return self.metricToVal['Total Preemptions'][-1]
    def getExceededCount(self):
        return self.metricToVal['Total Exceeded Count'][-1]
    def getNormalizedLaxity(self):
        return self.metricToVal['Normalized Laxity'][-1]
    


    @staticmethod
    def getAverageNormalizedLaxity(model):
        count = 0.0
        totalNormalizedLaxity = 0.0
        for task in model.results.tasks.values():
            for job in task.jobs:
                if(job.task.deadline and job.response_time):
                    totalNormalizedLaxity += job.normalized_laxity
                    count += 1
        return totalNormalizedLaxity / count

    ######## HELPER FUNCTIONS ###########
    def checkValidDict(self):
        for k,v in self.metriToVal.items():
            assert len(v) > 0, f'Item {k} was not updated/instantiated.'



        