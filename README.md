# simso_extension

Since all the algorithms in the simulator are preemptive, I wrote this fully-non-preemptive NP_RM scheduler. Also Fixed Preemption Point (FPP) with RM underlying is added.
  
from simso.core import Scheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.NP_RM")
class FPP(Scheduler):
    def init(self):
        self.ready_list = []

    def on_activate(self, job):
        self.ready_list.append(job)
	if (self.ready_list and not self.ready_list[0].is_running()):
		job.cpu.resched()

    def on_terminated(self, job):
        self.ready_list.remove(job)
        job.cpu.resched()

    def schedule(self, cpu):
        if self.ready_list:
            # job with the highest priority
            job = min(self.ready_list, key=lambda x: x.period)
        else:
            job = None

        return (job, cpu)


---The results---
$python test_FPP.py 
(I wrote this test code at a models directory at simos home directory)
The scheduler was also tested on simso's gui version


[0, ('T1_1 Activated.', True)]
[0, ('T2_1 Activated.', True)]
[0, ('T3_1 Activated.', True)]
[0, ('T1_1 Executing on CPU 1', True)]
[1000000, ('T1_1 Terminated.', True)]
[1000000, ('T2_1 Executing on CPU 1', True)]
[4000000, ('T2_1 Terminated.', True)]
[4000000, ('T3_1 Executing on CPU 1', True)]
[6000000, ('T1_2 Activated.', True)]
[6000000, ('T3_1 Preempted! ret: 4000000', True)]
[6000000, ('T3_1 Executing on CPU 1', True)]
[10000000, ('T2_2 Activated.', True)]
[10000000, ('Job T1_2 aborted! ret:1.0', False)]
[10000000, ('T3_1 Terminated.', True)]
[10000000, ('T2_2 Executing on CPU 1', True)]
[12000000, ('T1_3 Activated.', True)]
[12000000, ('T2_2 Preempted! ret: 1000000', True)]
[12000000, ('T2_2 Executing on CPU 1', True)]
[13000000, ('T2_2 Terminated.', True)]
[13000000, ('T1_3 Executing on CPU 1', True)]
[14000000, ('T1_3 Terminated.', True)]
T2:
T2_1 3.000 ms
T2_2 3.000 ms
T1:
T1_1 1.000 ms
T1_2 0.000 ms
T1_3 1.000 ms
T3:
T3_1 6.000 ms
T2 1
T1 0
T3 1




