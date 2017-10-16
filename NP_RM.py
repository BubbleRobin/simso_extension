from simso.core import Scheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.NP_RM")
class NP_RM(Scheduler):
    def init(self):
        self.ready_list = []

    def on_activate(self, job):
        self.ready_list.append(job)
	if (self.ready_list and not self.ready_list[0].is_running()):
		job.cpu.resched()

    def on_terminated(self, job):
    	
        if job in self.ready_list:
            self.ready_list.remove(job)
        else:
            job.cpu.resched()
        """
        self.ready_list.remove(job)
        job.cpu.resched()
        """
    def schedule(self, cpu):
    	"""
        if self.ready_list:
            # job with the highest priority
            job = min(self.ready_list, key=lambda x: x.period)
        else:
            job = None

        return (job, cpu)
        """
        decision = None
        if self.ready_list:
            # Get a free processor or a processor running a low priority job.
            key = lambda x: (
                0 if x.running is None else 1
            )
            cpu_min = min(self.processors, key=key)

            # Job with highest priority.
            job = min(self.ready_list, key=lambda x: x.period)

            if (cpu_min.running is None):
                self.ready_list.remove(job)
                decision = (job, cpu_min)

        return decision
        
