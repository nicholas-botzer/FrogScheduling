"""
Implementation of the Frog Scheduling genetic algorithm
"""
from simso.core import Scheduler
from simso.schedulers import scheduler

class FrogScheduler(Scheduler):

    def init(self):
        pass
    
    def on_activate(self, job):
        job.cpu.resched()

    def on_terminated(self, job):
        job.cpu.resched()

    def schedule(self, cpu):
        # List of ready jobs not currently running:
        ready_jobs = [t.job for t in self.task_list
            if t.is_active() and not t.job.is_running()]

        if ready_jobs:
            
            #determine the job with the highest priority
            priorList = [] # contains tuples (task Prior, job deadline, job)
            for job in ready_jobs:
                priorList.append((self.getTaskPriority(job.task),
                                  1.0/job._absolute_deadline,
                                  job))
            highestPriorJob = max(priorList)[0,2] # (priority, job)

            freeProcessor =  self.getFreeProcessor()

            #We have a free processor so schedule a task to it
            if(freeProcessor):
                return (highestPriorJob[1], freeProcessor)   #schedule the highest priority task to the free processor
            else:
                #get the list of processors and the priority of the tasks associated
                #determine the lowest priority task and processor combination

                processor, processorPriority = self.getLowestPriorityProcessorTaskCombination()

                #if the slected job has a higher priority than the lowest priorty task/processor combo kick it off
                #otherwise let it continue to run

                if(highestPriorJob[0] > processorPriority):
                    return (highestPriorJob[1], processor)


    def getFreeProcessor(self):
        for processor in self.processors:
            if not processor.running:
                return processor
    
    def getLowestPriorityProcessorTaskCombination(self):

        lowestPriority = 0
        lowestPriorityProcessor = None
        for processor in self.processors:
            if processor.running:
                processorTask = processor.running.task
                taskPriority = self.getTaskPriority(processorTask)

                if(taskPriority < lowestPriority):
                    lowestPriority = taskPriority
                    lowestPriorityProcessor = processor

        return lowestPriorityProcessor, lowestPriority


    def initializeChromosome(self, chromosome):
        self.chromosome = chromosome

    def getTaskPriority(self, task):
        return self.chromosome.taskToPriorityDict[task]