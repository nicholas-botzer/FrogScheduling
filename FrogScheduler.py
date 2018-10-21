"""
Implementation of the Frog Scheduling genetic algorithm
"""
from simso.core import Scheduler
from simso.schedulers import scheduler

class FrogScheduler(Scheduler):
    
    def on_activate(self, job):
        pass

    def on_terminated(self, job):
        pass

    def schedule(self, cpu):
        pass

    def initalizePriorityQueue(self, priorityQueue):
        self.priorityQueue = priorityQueue