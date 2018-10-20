class Chromosome():

    def __init__(self):
        self.taskToPriorityDict = {}

    def insert_task(self, task,priority):
        self.taskToPriorityDict[task] = priority

    def update_task(self, task, priority):
        if(task in self.taskToPriorityDict):
            self.taskToPriorityDict[task] = priority