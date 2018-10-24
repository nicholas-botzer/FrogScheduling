"""
Implementation of the Frog Scheduling genetic algorithm
"""
import sys, logging
logging.basicConfig(format='%(message)s',stream=None, level=logging.NOTSET)
logging.disable(999999)
from collections import defaultdict
from simso.core import Scheduler
from simso.schedulers import scheduler
from Crossovers import Crossovers


class FrogScheduler(Scheduler):

    def init(self):
        self.ganttData = defaultdict(list)
    
    def on_activate(self, job):
        logging.debug('[A] - JOB ACTIVATED. Job:{} (Time: {}) '.format(
            job.name,self.sim.now()))
        job.cpu.resched()

    def on_terminated(self, job):
        logging.debug('[T] - JOB TERMINATED. Job:{} CPU:{} (Time: {}) '.format(
            job.name,job.cpu.name,self.sim.now()))
        self.ganttData[job.cpu.name].append('Terminated job {} (Time: {})'.format(
            job.name,self.sim.now())) 
        job.cpu.resched()

    def schedule(self, cpu):

        #List of ready jobs not currently running:
        ready_jobs = [t.job for t in self.task_list
            if t.is_active() and not t.job.is_running()]

        logging.debug('[S] - Scheduler called. CPU:{} ready_jobs:{} (Time: {})'.format( 
            cpu._internal_id,[x.name for x in ready_jobs],self.sim.now()))

        if ready_jobs:
            
            #determine the job with the highest priority
            priorList = [] # contains tuples (task Prior, job deadline, job)
            for job in ready_jobs:
                priorList.append((self.getTaskPriority(job.task),
                                  1.0/job._absolute_deadline,
                                  job))
            highestPriorTup = max(priorList)
            highestPriorJob = [highestPriorTup[0],highestPriorTup[2]] #(priority, job)

            freeProcessor =  self.getFreeProcessor()

            #We have a free processor so schedule a task to it
            if(freeProcessor):
                logging.debug('       -> Scheduled job {} to cpu {}'.format( 
                    highestPriorJob[1].name,freeProcessor.name))
                if freeProcessor.name not in self.ganttData:
                    # print '{} not in'.format(freeProcessor.name)
                    self.ganttData[freeProcessor.name] = []
                self.ganttData[freeProcessor.name].append('Added job {} (Time: {})'.format(
                    highestPriorJob[1].name,self.sim.now())) 
                return (highestPriorJob[1], freeProcessor)   #schedule the highest priority task to the free processor
            else:
        #         #get the list of processors and the priority of the tasks associated
        #         #determine the lowest priority task and processor combination

                processor, processorPriority = self.getLowestPriorityProcessorTaskCombination()

        #         #if the slected job has a higher priority than the lowest priorty task/processor combo kick it off
        #         #otherwise let it continue to run

                if(highestPriorJob[0] > processorPriority):
                    logging.debug('       -> Scheduled job {} to cpu {}'.format( 
                        highestPriorJob[1].name,processor.name))
                    if processor.name not in self.ganttData:
                        #print '{} not in'.format(processor.name)
                        self.ganttData[processor.name] = []
                    self.ganttData[processor.name].append('Added job {} (Time: {})'.format(
                        highestPriorJob[1].name,self.sim.now())) 
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

                if(taskPriority > lowestPriority):
                    lowestPriority = taskPriority
                    lowestPriorityProcessor = processor

        return lowestPriorityProcessor, lowestPriority


    def initializeChromosome(self, chromosome):
        self.chromosome = chromosome

    def getTaskPriority(self, task):
        return self.chromosome.taskToPriorityDict[task.name]
