from tools.fitness import Fitness

class Chromosome:

    def __init__(self, taskList, name='Noname'):
        self.statsDict = {
            'PriorityDictList': [],
            'RankList': [],
            'OpsList': []
        }
        self.priorityDictList = [] # holds dicts that maps taskName to priority
        self.taskNameToPriority = dict(zip(
                                    [t.name for t in taskList],
                                    range(len(taskList))))
        self.fitness = Fitness()
        self.name = name

    def __str__(self):
        return f"Chrom{self.name}"

    def __repr__(self):
        return self.__str__()
    
    def saveCurrentPriorityDict(self):
        self.statsDict['PriorityDictList'].append(self.taskNameToPriority)
    def setNewPriorityDict(self,newDict):
        self.taskNameToPriority = newDict
    def addRank(self,newRank):
        self.statsDict['RankList'].append(newRank)
    
    
    # def updateTaskListWithLists(self, tasklist, prioritylist):
    #     for 
    #     self.taskNameToPriority[task.name] = priority

    # def update_task(self, task, priority):
    #     assert task in self.taskNameToPriorityDict, \
    #            f'Task ({task}) not in {self.taskNameToPriorityDict.items()}'
    #     self.taskNameToPriority[task.name] = priority


        