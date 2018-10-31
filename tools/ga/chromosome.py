from tools.fitness import Fitness

class Chromosome:

    def __init__(self, taskList, name='Noname'):
        self.priorityDictList = [] # holds dicts that maps taskName to priority
        self.taskNameToPriority = dict(zip(
                                    [t.name for t in taskList],
                                    range(len(taskList))))
        self.fitness = Fitness()
        self.name = name

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
    
    def saveCurrentPriorityDict(self):
        self.priorityDictList.append(self.taskNameToPriority)

    def setNewPriorityDict(self,newDict):
        self.taskNameToPriority = newDict
    
    # def updateTaskListWithLists(self, tasklist, prioritylist):
    #     for 
    #     self.taskNameToPriority[task.name] = priority

    # def update_task(self, task, priority):
    #     assert task in self.taskNameToPriorityDict, \
    #            f'Task ({task}) not in {self.taskNameToPriorityDict.items()}'
    #     self.taskNameToPriority[task.name] = priority


        