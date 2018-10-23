"""
Implementation of the Global-EDF (Earliest Deadline First) for multiprocessor
architectures.
"""
from simso.core import Scheduler
from simso.schedulers import scheduler
import logging
from collections import defaultdict

@scheduler("simso.schedulers.EDF")
class EDFScheduler(Scheduler):

    def init(self):
        self.ganttData = defaultdict(list)

    """Earliest Deadline First"""
    def on_activate(self, job):
        logging.debug('[A] - JOB ACTIVATED. Job:{} (Time: {}) '.format(
            job.name,self.sim.now()))
        
        job.cpu.resched()

    def on_terminated(self, job):
        logging.debug('[T] - JOB TERMINATED. Job:{} (Time: {}) '.format(
            job.name,self.sim.now()))
        self.ganttData[job.cpu.name].append('Terminated job {} (Time: {})'.format(
            job.name,self.sim.now()))
        job.cpu.resched()

    def schedule(self, cpu):
        # List of ready jobs not currently running:
        ready_jobs = [t.job for t in self.task_list
                      if t.is_active() and not t.job.is_running()]
        logging.debug('[S] - Scheduler called. CPU:{} ready_jobs:{} (Time: {})'.format( 
            cpu._internal_id,[x.name for x in ready_jobs],self.sim.now()))
        if ready_jobs:
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
                #print(self.sim.now(), job.name, cpu_min.name)
                if cpu_min.name not in self.ganttData:
                    self.ganttData[cpu_min.name] = []
                self.ganttData[cpu_min.name].append('Added job {} (Time: {})'.format(
                    job.name,self.sim.now())) 
                return (job, cpu_min)
