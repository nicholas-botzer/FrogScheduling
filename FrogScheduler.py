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

            #get priority list of jobs waiting to run
            #determine the job with the highest priority

            freeProcessor =  self.getFreeProcessor()

            #We have a free processor so schedule a task to it
            if(freeProcessor):
                pass #schedule the highest priority task to the free processor
            else:
                pass
                #get priority list of tasks and processors they are on

                #determine the lowest priority task and processor combination

                #if the slected job has a higher priority than the lowest priorty task/processor combo kick it off
                #otherwise let it continue to run



            # Select a free processor or, if none,
            # the one with the greatest deadline (self in case of equality):
            key = lambda x: (
                1 if not x.running else 0,
                x.running.absolute_deadline if x.running else 0,
                1 if x is cpu else 0
            )

            cpu_min = max(self.processors, key=key)

            # Select the job with the least priority:
            job = min(ready_jobs, key=lambda x: x.absolute_deadline)

            if (cpu_min.running is None or
                    cpu_min.running.absolute_deadline > job.absolute_deadline):
                print(self.sim.now(), job.name, cpu_min.name)
                return (job, cpu_min)


    def getFreeProcessor(self):
        for processor in self.processors:
            if not processor.running:
                return processor
    

    def initializeChromosome(self, chromosome):
        self.chromosome = chromosome