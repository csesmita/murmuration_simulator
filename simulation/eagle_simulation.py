#
# EAGLE 
#
# Copyright 2016 Operating Systems Laboratory EPFL
#
# Modified from Sparrow - University of California, Berkeley 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



import sys
import time
import logging
import random
from queue import PriorityQueue
import bitmap
import copy
from collections import deque, defaultdict
from itertools import count
from operator import itemgetter
from datetime import datetime

class TaskDurationDistributions:
    CONSTANT, MEAN, FROM_FILE  = range(3)
class EstimationErrorDistribution:
    CONSTANT, RANDOM, MEAN  = range(3)

class Job(object):
    job_count = 1
    per_job_task_info = {}

    def __init__(self, task_distribution, line, estimate_distribution, off_mean_bottom, off_mean_top):
        global job_start_tstamps
        global job_count

        job_args                    = (line.split('\n'))[0].split()
        self.start_time             = float(job_args[0]) / SPEEDUP
        self.num_tasks              = int(job_args[1])
        mean_task_duration          = (float(job_args[2]))

        self.id = Job.job_count
        Job.job_count += 1
        self.completed_tasks_count = 0
        self.end_time = self.start_time
        self.unscheduled_tasks = deque()
        self.actual_task_duration = []
        self.off_mean_bottom = off_mean_bottom
        self.off_mean_top = off_mean_top

        self.job_type_for_scheduling = BIG if mean_task_duration > CUTOFF_THIS_EXP  else SMALL
        self.job_type_for_comparison = BIG if mean_task_duration > CUTOFF_BIG_SMALL else SMALL
        
        if   task_distribution == TaskDurationDistributions.FROM_FILE: 
            self.file_task_execution_time(job_args)
        elif task_distribution == TaskDurationDistributions.CONSTANT:
            while len(self.unscheduled_tasks) < self.num_tasks:
                self.unscheduled_tasks.appendleft(mean_task_duration)

        self.estimate_distribution = estimate_distribution

        if   estimate_distribution == EstimationErrorDistribution.MEAN:
            self.estimated_task_duration = mean_task_duration
        elif estimate_distribution == EstimationErrorDistribution.CONSTANT:
            self.estimated_task_duration = int(mean_task_duration+off_mean_top*mean_task_duration)
        elif estimate_distribution == EstimationErrorDistribution.RANDOM:
            top = off_mean_top*mean_task_duration
            bottom = off_mean_bottom*mean_task_duration
            self.estimated_task_duration = int(random.uniform(bottom,top))
            assert(self.estimated_task_duration <= int(top))
            assert(self.estimated_task_duration >= int(bottom))

        self.probed_workers = set()
        self.remaining_exec_time = self.estimated_task_duration*len(self.unscheduled_tasks)
        self.tct = 0
        self.w2x = 0
        self.tail_tct = 0

    #Job class    """ Returns true if the job has completed, and false otherwise. """
    def update_task_completion_details(self, completion_time, task_wait_time):
        self.completed_tasks_count += 1
        self.tct += completion_time
        self.end_time = max(completion_time, self.end_time)
        if self.end_time == completion_time:
            self.tail_tct = completion_time
        self.w2x += task_wait_time
        assert self.completed_tasks_count <= self.num_tasks
        return self.num_tasks == self.completed_tasks_count


    #Job class
    def file_task_execution_time(self, job_args):
        for task_duration in (job_args[3:]):
           self.unscheduled_tasks.appendleft(float(task_duration))
           self.actual_task_duration.append(float(task_duration))
        assert(len(self.unscheduled_tasks) == self.num_tasks)

    #Job class
    def update_remaining_time(self):
        self.remaining_exec_time -= self.estimated_task_duration
        #assert(self.remaining_exec_time >=0)
        if (len(self.unscheduled_tasks) == 0): #Improvement
            self.remaining_exec_time = -1

#####################################################################################################################
#####################################################################################################################
class Stats(object):

    STATS_STEALING_MESSAGES = 0
    STATS_SH_PROBES_QUEUED_BEHIND_BIG = 0
    STATS_TASKS_SH_EXEC_IN_BP = 0
    STATS_TOTAL_STOLEN_PROBES = 0
    STATS_TOTAL_STOLEN_B_FROM_B_PROBES = 0
    STATS_TOTAL_STOLEN_S_FROM_S_PROBES = 0
    STATS_TOTAL_STOLEN_S_FROM_B_PROBES = 0
    STATS_SUCCESSFUL_STEAL_ATTEMPTS = 0
    STATS_SHORT_TASKS_WAITED_FOR_BIG = 0
    STATS_STICKY_EXECUTIONS = 0
    STATS_STICKY_EXECUTIONS_IN_BP = 0
    STATS_REASSIGNED_PROBES=0
    STATS_TASKS_TOTAL_FINISHED = 0   
    STATS_TASKS_SHORT_FINISHED = 0   
    STATS_TASKS_LONG_FINISHED = 0   
    STATS_SHORT_UNSUCC_PROBES_IN_BIG = 0
    STATS_SH_PROBES_ASSIGNED_IN_BP = 0
    STATS_BYPASSEDBYBIG_AND_STUCK = 0
    STATS_FALLBACKS_TO_SP = 0
    STATS_RND_FIRST_ROUND_NO_LOCAL_BITMAP = 0
    STATS_ROUNDS = 0
    STATS_ROUNDS_ATTEMPTS = 0
    STATS_PERC_1ST_ROUNDS = 0

#####################################################################################################################
#####################################################################################################################
class Event(object):
    def __init__(self):
        raise NotImplementedError("Event is an abstract class and cannot be instantiated directly")

    def run(self, current_time):
        """ Returns any events that should be added to the queue. """
        raise NotImplementedError("The run() method must be implemented by each class subclassing Event")

#####################################################################################################################
#####################################################################################################################

class JobArrival(Event):

    def __init__(self, simulation, task_distribution, job, jobs_file):
        self.simulation = simulation
        self.task_distribution = task_distribution
        self.job = job
        self.jobs_file = jobs_file

    def run(self, current_time):
        new_events = []

        long_job = self.job.job_type_for_scheduling == BIG
        worker_indices = []

        btmap = None
        if not long_job:
            print(current_time, ": Short Job arrived!!", self.job.id, " num tasks ", self.job.num_tasks, " estimated_duration ", self.job.estimated_task_duration)

            
            rnd_worker_in_big_partition = random.randint(self.simulation.index_first_worker_of_big_partition, len(self.simulation.workers)-1)
            self.simulation.hash_jobid_to_node[self.job.id]=rnd_worker_in_big_partition

            if SYSTEM_SIMULATED == "Hawk" or SYSTEM_SIMULATED == "Eagle" or SYSTEM_SIMULATED == "SparrowPT":
                possible_worker_indices = self.simulation.small_partition_workers
            if SYSTEM_SIMULATED == "IdealEagle":
                possible_worker_indices = self.simulation.get_list_non_long_job_workers_from_btmap(self.simulation.cluster_status_keeper.get_btmap())

            worker_indices = self.simulation.find_workers_random(PROBE_RATIO, self.job.num_tasks, possible_worker_indices,MIN_NR_PROBES)

        else:
            print(current_time, ":   Big Job arrived!!", self.job.id, " num tasks ", self.job.num_tasks, " estimated_duration ", self.job.estimated_task_duration)
            btmap = self.simulation.cluster_status_keeper.get_btmap()

            if (SYSTEM_SIMULATED == "DLWL"):
                if self.job.job_type_for_comparison == SMALL:
                    possible_workers = self.simulation.small_partition_workers_hash
                else:
                    possible_workers = self.simulation.big_partition_workers_hash
                estimated_task_durations = [self.job.estimated_task_duration for i in range(len(self.job.unscheduled_tasks))]
                worker_indices = self.simulation.find_workers_dlwl(estimated_task_durations, self.simulation.shared_cluster_status, current_time, self.simulation, possible_workers)
                self.simulation.cluster_status_keeper.update_workers_queue(worker_indices, True, self.job.estimated_task_duration)
            elif (SYSTEM_SIMULATED == "Murmuration"):
                new_events.append((current_time, NoOpSchedulingEvents(self.simulation, self.job)))

                #Task hasn't yet started
                Job.per_job_task_info[self.job.id] = {}
                for tasknr in range(0,self.job.num_tasks):
                    Job.per_job_task_info[self.job.id][tasknr] =- 1

                # Creating a new Job Arrival event for the next job in the trace
                line = self.jobs_file.readline()
                if (line == ''):
                    self.simulation.scheduled_last_job = True
                    return new_events

                self.job = Job(self.task_distribution, line, self.job.estimate_distribution, self.job.off_mean_bottom, self.job.off_mean_top)
                new_events.append((self.job.start_time, self))
                self.simulation.jobs_scheduled += 1
                return new_events
            elif (self.simulation.SCHEDULE_BIG_CENTRALIZED):
                workers_queue_status = self.simulation.cluster_status_keeper.get_queue_status()
                if SYSTEM_SIMULATED == "CLWL" and self.job.job_type_for_comparison == SMALL:
                    possible_workers = self.simulation.small_partition_workers_hash
                else:
                    possible_workers = self.simulation.big_partition_workers_hash

                worker_indices = self.simulation.find_workers_long_job_prio(self.job.num_tasks, self.job.estimated_task_duration, workers_queue_status, current_time, self.simulation, possible_workers)
                self.simulation.cluster_status_keeper.update_workers_queue(worker_indices, True, self.job.estimated_task_duration)
            else:
                worker_indices = self.simulation.find_workers_random(PROBE_RATIO, self.job.num_tasks, self.simulation.big_partition_workers,MIN_NR_PROBES)

        Job.per_job_task_info[self.job.id] = {}
        for tasknr in range(0,self.job.num_tasks):
            Job.per_job_task_info[self.job.id][tasknr] =- 1 

        new_events = self.simulation.send_probes(self.job, current_time, worker_indices, btmap)

        # Creating a new Job Arrival event for the next job in the trace
        line = self.jobs_file.readline()
        if (line == ''):
            self.simulation.scheduled_last_job = True
            return new_events

        self.job = Job(self.task_distribution, line, self.job.estimate_distribution, self.job.off_mean_bottom, self.job.off_mean_top)
        new_events.append((self.job.start_time, self))
        self.simulation.jobs_scheduled += 1
        return new_events


#####################################################################################################################
#####################################################################################################################
class PeriodicSchedulerFailureAttempt(Event):
    def __init__(self,simulation):
        self.simulation = simulation

    def run(self, current_time):
        new_events = []
        #Fail a random scheduler
        failed_sched_id = random.choice(self.simulation.scheduler_indices)
        #contact randomly chosen schedulers for their resource cache
        self.simulation.scheduler_indices.remove(failed_sched_id)
        scheduler_object = self.simulation.workers[failed_sched_id]
        print(current_time,"Scheduler", failed_sched_id, "failed.")
        print(current_time,"Scheduler", failed_sched_id, "failed.", file=finished_file,)
        #Scheduler has failed. 
        assert scheduler_object.get_scheduler_queue_length() == 0
        removed = self.simulation.cluster_status_keeper.remove_scheduler(failed_sched_id)
        assert removed

        contact_num_sched = min(2, len(self.simulation.scheduler_indices))
        if contact_num_sched > 0:
            contact_sched_ids = random.sample(self.simulation.scheduler_indices, contact_num_sched)
            print("Scheduler", failed_sched_id,"restarted at time", current_time, "will contact schedulers", contact_sched_ids)
            print("Scheduler", failed_sched_id,"restarted at time", current_time, "will contact schedulers", contact_sched_ids, file=finished_file,)
            for requested in contact_sched_ids:
                new_events.append((current_time + SCHEDULER_RESTART_TIME + NETWORK_DELAY, SchedulerCacheRequest(failed_sched_id, requested, self.simulation)))
        else:
            #Proceed since this is the only scheduler
            print("Scheduler", failed_sched_id, "will wait to restart")
            new_events.append((current_time + SCHEDULER_RESTART_TIME, SchedulerCacheResponse(failed_sched_id, failed_sched_id, defaultdict(int), self.simulation)))

        #TODO: Timeout on the contacted schedulers and take further action if need be
        #Only 1 scheduler failure in the life of the run.
        return new_events


class SchedulerCacheRequest(Event):
    def __init__(self,client_sched, server_sched, simulation):
        self.client_sched = client_sched
        self.server_sched = server_sched
        self.simulation = simulation

    def run(self, current_time):
        new_events = []
        cache_snapshot = copy.deepcopy(self.simulation.cluster_status_keeper.get_scheduler_view(self.server_sched))
        print(current_time, "Scheduler", self.server_sched, "sends its copy")
        print(current_time, "Scheduler", self.server_sched, "sends its copy", file=finished_file,)
        #send snapshot to client_sched with a random delay
        new_events.append((current_time + random.uniform(0,CACHE_RESPONSE_TIME_JITTER) + NETWORK_DELAY, SchedulerCacheResponse(self.client_sched, self.server_sched, cache_snapshot, self.simulation)))
        return new_events

class SchedulerCacheResponse(Event):
    def __init__(self,client_sched, server_sched, snapshot, simulation):
        self.client_sched = client_sched
        self.server_sched = server_sched
        self.snapshot = snapshot
        self.simulation = simulation

    def run(self, current_time):
        newly_initialized = self.simulation.cluster_status_keeper.initialize_scheduler_view(self.client_sched, self.snapshot)
        if newly_initialized:
            assert (self.client_sched not in self.simulation.scheduler_indices)
            self.simulation.scheduler_indices.append(self.client_sched)
            print(current_time, "Scheduler", self.client_sched,"copies from scheduler", self.server_sched)
            print(current_time, "Scheduler", self.client_sched,"copies from scheduler", self.server_sched, file=finished_file,)
            print("Queue lengths of schedulers - ")
            for sched_id in self.simulation.scheduler_indices:
                scheduler_object = self.simulation.workers[sched_id]
                print(sched_id,":",scheduler_object.get_scheduler_queue_length()),
        return []



class PeriodicTimerEvent(Event):
    def __init__(self,simulation):
        self.simulation = simulation

    def run(self, current_time):
        new_events = []

        total_load       = str(int(10000*(1-self.simulation.total_free_slots*1.0/(self.simulation.total_slots)))/100.0)
        small_load       = str(int(10000*(1-self.simulation.free_slots_small_partition*1.0/len(self.simulation.small_partition_workers)))/100.0)
        big_load         = str(int(10000*(1-self.simulation.free_slots_big_partition*1.0/len(self.simulation.big_partition_workers)))/100.0)
        small_not_big_load ="N/A"
        if(len(self.simulation.small_not_big_partition_workers)!=0):
            small_not_big_load        = str(int(10000*(1-self.simulation.free_slots_small_not_big_partition*1.0/len(self.simulation.small_not_big_partition_workers)))/100.0)

        print("total_load: " + total_load + " small_load: " + small_load + " big_load: " + big_load + " small_not_big_load: " + small_not_big_load+" current_time: " + str(current_time), file=load_file)

        if(not self.simulation.event_queue.empty()):
            new_events.append((current_time + MONITOR_INTERVAL,self))
        return new_events


#####################################################################################################################
#####################################################################################################################
#####################################################################################################################

class WorkerHeartbeatEvent(Event):
    
    def __init__(self,simulation):
        self.simulation = simulation

    def run(self, current_time):
        new_events = []
        if(HEARTBEAT_DELAY == 0):
            self.simulation.shared_cluster_status = self.simulation.cluster_status_keeper.get_queue_status()
        else:
            self.simulation.shared_cluster_status = copy.deepcopy(self.simulation.cluster_status_keeper.get_queue_status()) 
     
        if(HEARTBEAT_DELAY != 0): 
            if(self.simulation.jobs_completed != self.simulation.jobs_scheduled or self.simulation.scheduled_last_job == False):
                new_events.append((current_time + HEARTBEAT_DELAY,self))

        return new_events


#####################################################################################################################
#####################################################################################################################

class ProbeEvent(Event):
    def __init__(self, worker, job_id, est_task_length, job_type_for_scheduling, btmap, task_index):
        self.worker = worker
        self.job_id = job_id
        self.est_task_length = est_task_length
        self.job_type_for_scheduling = job_type_for_scheduling
        self.btmap = btmap
        self.task_index = task_index

    def run(self, current_time):
        return self.worker.add_probe(self.job_id, self.est_task_length, self.job_type_for_scheduling, current_time,self.btmap, False, self.task_index)

#####################################################################################################################
#####################################################################################################################
class ClusterStatusKeeper():
    def __init__(self, scheduler_indices):
        self.worker_queues = {}
        self.scheduler_view = {}
        self.btmap = bitmap.BitMap(TOTAL_WORKERS)
        self.scheduler_indices = scheduler_indices
        for i in range(0, TOTAL_WORKERS):
           self.worker_queues[i] = 0
        for i in scheduler_indices:
            self.scheduler_view[i] = defaultdict(int)
            for j in range(0, TOTAL_WORKERS):
                self.scheduler_view[i][j] = 0

    def get_queue_status(self):
        return self.worker_queues

    def get_btmap(self):
        return self.btmap

    def update_workers_queue(self, worker_indices, increase, duration):
        for worker in worker_indices:
            queue = self.worker_queues[worker]
            if increase:
                queue += duration
                self.btmap.set(worker) 
            else:
                queue -= duration
                if(queue == 0):
                    self.btmap.flip(worker) 
            if queue < 0:
                #print(" offending value for queue: %r %i " % (queue,worker))
                if abs(queue) < 0.001:
                    queue =0
                else:
                    raise AssertionError(" offending value for queue: %r %i " % (queue,worker))
            self.worker_queues[worker] = queue

    #Update rx scheduler with placement info.
    def update_scheduler_view(self, origin_scheduler_index, rx_scheduler_index, core_id,current_time, history_time, duration, num_slots, increment):
        if origin_scheduler_index == rx_scheduler_index:
            return
        self.update_local_scheduler_view(rx_scheduler_index, core_id, num_slots, history_time, duration, increment)

    def update_local_scheduler_view(self,rx_scheduler_index, core_id, num_slots, history_time, duration, increment):
        availability_at_cores = self.scheduler_view[rx_scheduler_index]
        core_availability = availability_at_cores[core_id]
        #Update whatever is received from other schedulers and earlier placements by self.
        #This is the complete truth.
        if history_time > core_availability:
            #Placement happened after previous tasks had completed.
            #This advancement cannot be reversed.
            #All durations get added beyond this hole.
            core_availability = history_time
        if increment:
            availability_at_cores[core_id] = core_availability + duration/num_slots
        else:
            availability_at_cores[core_id] = core_availability - duration/num_slots

    #Get shortest wait time node from cache. Update scheduler with placement info.
    def get_worker_with_shortest_wait(self, scheduler_index, current_time):
        if scheduler_index not in self.scheduler_view.keys():
            return -1
        availability_at_cores = self.scheduler_view[scheduler_index]
        chosen_worker, _ = sorted(availability_at_cores.items(), key = lambda v:(v[1], random.random()))[0]
        #print("Scheduler chooses worker with actual wait",self.worker_queues[chosen_worker],", workers have the following waits - ", "min",self.worker_queues[min(self.worker_queues, key=self.worker_queues.get)], "max", self.worker_queues[max(self.worker_queues, key=self.worker_queues.get)] , file=finished_file,)
        return chosen_worker

    def print_scheduler_view(self, scheduler_index):
        print("Scheduler view - ",file=finished_file,)
        print(self.scheduler_view[scheduler_index], file=finished_file,)

    def get_scheduler_view(self, scheduler_index):
        return self.scheduler_view[scheduler_index]

    def remove_scheduler(self, scheduler_index):
        if scheduler_index in self.scheduler_view.keys():
            del self.scheduler_view[scheduler_index]
            return True
        return False

    def initialize_scheduler_view(self, scheduler_index, snapshot):
        if scheduler_index in self.scheduler_view.keys():
            return False
        self.scheduler_view[scheduler_index] = snapshot
        if len(self.scheduler_view[scheduler_index].keys()) == 0:
            for j in range(0, TOTAL_WORKERS):
                self.scheduler_view[scheduler_index][j] = 0
        return True

#####################################################################################################################
#####################################################################################################################

class NoopGetTaskResponseEvent(Event):
    def __init__(self, worker):
        self.worker = worker

    def run(self, current_time):
        return self.worker.free_slot(current_time)

#####################################################################################################################
#####################################################################################################################

class UpdateRemainingTimeEvent(Event):
    def __init__(self, job):
        self.job = job

    def run(self, current_time):
        assert( len(self.job.unscheduled_tasks)>=0)
        self.job.update_remaining_time()
        return []

#####################################################################################################################
#####################################################################################################################

class TaskEndEvent():
    def __init__(self, worker, SCHEDULE_BIG_CENTRALIZED, status_keeper, job_id, job_type_for_scheduling, estimated_task_duration, this_task_id, task_duration):
        self.worker = worker
        self.SCHEDULE_BIG_CENTRALIZED = SCHEDULE_BIG_CENTRALIZED
        self.status_keeper = status_keeper
        self.job_id = job_id
        self.job_type_for_scheduling = job_type_for_scheduling
        self.estimated_task_duration = estimated_task_duration
        self.this_task_id = this_task_id
        self.task_duration= task_duration

    def run(self, current_time):
        global stats
        stats.STATS_TASKS_TOTAL_FINISHED += 1
        if(self.job_type_for_scheduling != BIG):
            stats.STATS_TASKS_SHORT_FINISHED += 1
            if(self.worker.in_big):
                stats.STATS_TASKS_SH_EXEC_IN_BP += 1
        elif (self.SCHEDULE_BIG_CENTRALIZED):
            self.status_keeper.update_workers_queue([self.worker.id], False, self.estimated_task_duration)

        if(self.job_type_for_scheduling == BIG):
            stats.STATS_TASKS_LONG_FINISHED += 1

        del Job.per_job_task_info[self.job_id][self.this_task_id]
            

        self.worker.tstamp_start_crt_big_task =- 1
        return self.worker.free_slot(current_time)

#####################################################################################################################
#####################################################################################################################
#Poke the scheduler when a new job is added to its queue.
class NoOpSchedulingEvents(object):
    def __init__(self, simulation, job):
        self.job = job
        self.simulation = simulation

    def run(self, current_time):
        if len(self.simulation.scheduler_indices) == 0:
            #Check ever so often if there are schedulers available.
            return [(current_time + JOB_CHECK_SCHEDULER_AVAILABILITY, self)]
        scheduler_index = random.choice(self.simulation.scheduler_indices)
        scheduler_object = self.simulation.workers[scheduler_index]
        scheduler_object.add_job_to_scheduler_queue(current_time, self.job)
        print(current_time,": Job", self.job.id, "assigned to scheduler", scheduler_index, file=finished_file,)
        print(current_time,": Job", self.job.id, "assigned to scheduler", scheduler_index)
        return scheduler_object.try_schedule_one(current_time)

#####################################################################################################################
#####################################################################################################################

class SchedulingDoneEvents(object):
    def __init__(self, simulation, scheduler_index):
        self.scheduler_index = scheduler_index
        self.simulation = simulation

    def run(self, current_time):
        scheduler_object = self.simulation.workers[self.scheduler_index]
        scheduler_object.set_scheduler_idle_status(True)
        return scheduler_object.try_schedule_one(current_time)

#####################################################################################################################
#####################################################################################################################

class Worker(object):
    def __init__(self, simulation, num_slots, id, index_last_small, index_first_big):
        
        self.simulation = simulation

        self.num_slots = num_slots
        # List of times when slots were freed, for each free slot (used to track the time the worker spends idle).
        self.free_slots = []
        while len(self.free_slots) < num_slots:
            self.free_slots.append(0)

        self.queued_big = 0
        self.queued_probes = []
        self.id = id
        self.executing_big = False

        self.tstamp_start_crt_big_task = -1
        self.estruntime_crt_task = -1

        self.in_small           = False
        self.in_big             = False
        self.in_small_not_big   = False

        if (id <= index_last_small):       self.in_small = True
        if (id >= index_first_big):        self.in_big = True
        if (id < index_first_big):         self.in_small_not_big = True

        self.btmap = None
        self.btmap_tstamp = -1
        self.busy_time = 0.0
        self.num_tasks = 0
        self.scheduler_queue = None
        self.scheduler_idle = None

    def init_scheduler_queue(self):
        self.scheduler_queue = PriorityQueue()
        self.scheduler_idle = True

    def add_job_to_scheduler_queue(self, current_time, job):
        if SCHED_REORDER_TECHNIQUE == "FCFS":
            self.scheduler_queue.put((current_time, job.id, job))
        elif SCHED_REORDER_TECHNIQUE == "SJF":
            self.scheduler_queue.put((job.estimated_task_duration, job.id, job))
        elif SCHED_REORDER_TECHNIQUE == "LRTF":
            self.scheduler_queue.put((job.num_tasks, job.id, job))
        elif SCHED_REORDER_TECHNIQUE == "SRJF":
            self.scheduler_queue.put((job.estimated_task_duration * job.num_tasks, job.id, job))

    def get_next_job_from_scheduler_queue(self):
        _, _, job = self.scheduler_queue.get()
        return job

    def get_scheduler_queue_length(self):
        return self.scheduler_queue.qsize()

    def get_scheduler_idle_status(self):
        return self.scheduler_idle

    def set_scheduler_idle_status(self, status):
        self.scheduler_idle = status

    def try_schedule_one(self, current_time):
        if self.get_scheduler_queue_length() > 0 and self.get_scheduler_idle_status():
            self.set_scheduler_idle_status(False)
            job = self.get_next_job_from_scheduler_queue()
            return self.simulation.send_probes(job, current_time, [self.id], None)
        return []

    #Worker class
    def add_probe(self, job_id, task_length, job_type_for_scheduling, current_time, btmap, handle_stealing, task_index):
        global stats

        long_job = job_type_for_scheduling == BIG
        if (not long_job and handle_stealing == False and (self.executing_big == True or self.queued_big > 0)):
            stats.STATS_SH_PROBES_QUEUED_BEHIND_BIG += 1        
    
        if (not long_job and handle_stealing == False and  self.in_big):        
            stats.STATS_SH_PROBES_ASSIGNED_IN_BP +=1
        self.queued_probes.append([job_id,task_length,(self.executing_big == True or self.queued_big > 0), 0, False,-1, task_index, current_time])

        if (long_job):
            self.queued_big     = self.queued_big + 1
            self.btmap          = copy.deepcopy(btmap)
            self.btmap_tstamp   = current_time

        if len(self.queued_probes) > 0 and len(self.free_slots) > 0:
            return self.process_next_probe_in_the_queue(current_time)
        else:
            return []

    def queue_length(self):
        queue_length = len(self.queued_probes)
        if len(self.free_slots) > 0:
            assert queue_length == 0
            return -1 * len(self.free_slots)
        return queue_length


    #Worker class
    def free_slot(self, current_time):
        self.free_slots.append(current_time)
        self.simulation.increase_free_slots_for_load_tracking(self)
        self.executing_big = False

        if len(self.queued_probes) > 0:
            return self.process_next_probe_in_the_queue(current_time)
        
        if len(self.queued_probes) == 0 and self.simulation.stealing_allowed == True:
            return self.ask_probes(current_time)
        
        return []



    #Worker class
    def ask_probes(self, current_time):
        global stats

        new_events  =  []
        new_probes  =  []
        ctr_it      =  0
        from_worker = -1

        while(ctr_it < STEALING_ATTEMPTS and len(new_probes) == 0):
            from_worker,new_probes = self.simulation.get_probes(current_time, self.id)
            ctr_it += 1

        if(from_worker!=-1 and len(new_probes)!= 0):
            print(current_time, ": Worker ", self.id," Stealing: ", len(new_probes), " from: ",from_worker, " attempts: ",ctr_it)
            from_worker_obj=self.simulation.workers[from_worker]
            if(from_worker_obj.in_big and self.in_big):
                stats.STATS_TOTAL_STOLEN_B_FROM_B_PROBES          += len(new_probes)
            if(from_worker_obj.in_big and not self.in_big):
                stats.STATS_TOTAL_STOLEN_S_FROM_B_PROBES          += len(new_probes)
            if(not from_worker_obj.in_big and not self.in_big):
                stats.STATS_TOTAL_STOLEN_S_FROM_S_PROBES          += len(new_probes)
                 

            stats.STATS_STEALING_MESSAGES           += ctr_it
            stats.STATS_TOTAL_STOLEN_PROBES          += len(new_probes)
            stats.STATS_SUCCESSFUL_STEAL_ATTEMPTS   += 1
        else:
            print(current_time, ": Worker ", self.id," failed to steal. attempts: ",ctr_it)
            stats.STATS_STEALING_MESSAGES += ctr_it

        for job_id, task_length, behind_big, cum, sticky, handle_steal, task_index in new_probes:
            assert (self.simulation.jobs[job_id].job_type_for_comparison != BIG)
            new_events.extend(self.add_probe(job_id, task_length, SMALL, current_time, None,True, task_index))

        return new_events



    #Worker class
    def get_probes_atc(self, current_time, free_worker_id):
        probes_to_give = []

        i = 0
        skipped_small = 0
        skipped_big = 0

        if not self.executing_big:
            while (i < len(self.queued_probes) and self.simulation.jobs[self.queued_probes[i][0]].job_type_for_comparison != BIG): #self.queued_probes[i][1] <= CUTOFF_THIS_EXP):
                i += 1

        skipped_short = i

        while (i < len(self.queued_probes) and self.simulation.jobs[self.queued_probes[i][0]].job_type_for_comparison == BIG): #self.queued_probes[i][1] > CUTOFF_THIS_EXP):
            i += 1

        skipped_big = i - skipped_short

        total_time_probes = 0

        nr_short_chosen = 0
        if (i < len(self.queued_probes)):
            while (len(self.queued_probes) > i and self.simulation.jobs[self.queued_probes[i][0]].job_type_for_scheduling != BIG and nr_short_chosen < STEALING_LIMIT):
                nr_short_chosen += 1
                probes_to_give.append(self.queued_probes.pop(i))
                total_time_probes += probes_to_give[-1][1]

        return probes_to_give



    #Worker class
    def get_probes_random(self, current_time, free_worker_id):
        probes_to_give = []
        all_positions_of_short_tasks = []
        randomly_chosen_short_task_positions = []
        i = 0

        #record the ids (in queued_probes) of the queued short tasks
        while (i < len(self.queued_probes)):
            big_job = self.simulation.jobs[self.queued_probes[i][0]].job_type_for_scheduling == BIG
            if (not big_job): #self.queued_probes[i][1] <= CUTOFF_THIS_EXP):
                all_positions_of_short_tasks.append(i)
            i += 1


        #select the probes to steal
        i = 0
        while (len(all_positions_of_short_tasks) > 0 and len(randomly_chosen_short_task_positions) < STEALING_LIMIT):
            rnd_index = random.randint(0,len(all_positions_of_short_tasks)-1)
            randomly_chosen_short_task_positions.append(all_positions_of_short_tasks.pop(rnd_index))
        randomly_chosen_short_task_positions.sort()

        #remove the selected probes from the worker queue in decreasing order of IDs
        decreasing_ids = len(randomly_chosen_short_task_positions)-1
        total_time_probes = 0
        while (decreasing_ids >= 0):
            probes_to_give.append(self.queued_probes.pop(randomly_chosen_short_task_positions[decreasing_ids]))
            total_time_probes += probes_to_give[-1][1]
            decreasing_ids -= 1
        probes_to_give = probes_to_give[::-1]  #reverse the list of tuples

        return probes_to_give



    #Worker class
    def process_next_probe_in_the_queue(self, current_time):
        global stats

        self.free_slots.pop(0)
        self.simulation.decrease_free_slots_for_load_tracking(self)
        
        if (SRPT_ENABLED):
            if (SYSTEM_SIMULATED == "Eagle" or SYSTEM_SIMULATED == "Hawk"):
                pos = self.get_next_probe_acc_to_sbp_srpt(current_time)
                if (pos == -1):
                    assert (len(self.queued_probes) == 0)
                    #Cannot just return [], free_slot would not be called again
                    return [(current_time, NoopGetTaskResponseEvent(self))]
            else:
                pos = self.get_next_probe_acc_to_srpt(current_time)
        else:
            pos = 0

        job_id = self.queued_probes[pos][0]
        estimated_task_duration = self.queued_probes[pos][1]
        task_index = self.queued_probes[pos][6]
        queue_start_time = self.queued_probes[pos][7]

        self.executing_big = self.simulation.jobs[job_id].job_type_for_scheduling == BIG
        if self.executing_big:
            self.queued_big                 = self.queued_big -1
            self.tstamp_start_crt_big_task  = current_time
            self.estruntime_crt_task        = estimated_task_duration
        else:
            self.tstamp_start_crt_big_task = -1

        was_successful, events = self.simulation.get_task(job_id, self, current_time, task_index, queue_start_time)
        job_bydef_big = (self.simulation.jobs[job_id].job_type_for_comparison == BIG)
       
        if(not job_bydef_big and self.queued_probes[0][5] == 1 and self.in_big and was_successful):
            stats.STATS_BYPASSEDBYBIG_AND_STUCK+=1 

        if(not job_bydef_big and self.queued_probes[0][2] == True and self.in_big and was_successful):
               stats.STATS_SHORT_TASKS_WAITED_FOR_BIG += 1
               self.simulation.jobs_affected_by_holb[job_id]=1
                   
 
        if(not job_bydef_big and not was_successful and self.in_big):
                stats.STATS_SHORT_UNSUCC_PROBES_IN_BIG +=1

        if(SBP_ENABLED==True and was_successful and not job_bydef_big):
            if(self.queued_probes[pos][4]):
                stats.STATS_STICKY_EXECUTIONS += 1
                if(self.in_big):
                    stats.STATS_STICKY_EXECUTIONS_IN_BP +=1
            self.queued_probes[pos][4] = True
    
        if(SBP_ENABLED==False or not was_successful or job_bydef_big):
            #so the probe remains if SBP is on, was succesful and is small        
            self.queued_probes.pop(pos)

        if(SRPT_ENABLED==True and (SYSTEM_SIMULATED=="Eagle" or SYSTEM_SIMULATED=="Hawk")):
            if(was_successful and job_bydef_big):
                for delay_it in range(0,pos):
                    self.queued_probes[delay_it][5]=1

            if(was_successful and not job_bydef_big):
                # Add estimated_delay to probes in front
                for delay_it in range(0,pos):
                    job_id        = self.queued_probes[delay_it][0]
                    new_acc_delay = self.queued_probes[delay_it][3] + estimated_task_duration
                    self.queued_probes[delay_it][3] = new_acc_delay

                    #Debug
                    if(SYSTEM_SIMULATED=="Eagle"):
                        job_bydef_big = self.simulation.jobs[job_id].job_type_for_comparison == BIG
                        assert(not job_bydef_big)
                        task_duration = self.simulation.jobs[job_id].estimated_task_duration
                        if (CAP_SRPT_SBP != float('inf')):
                            assert(new_acc_delay <= CAP_SRPT_SBP * task_duration), " Chosen position: %r, length %r , offending  %r" % (pos,len(self.queued_probes), new_acc_delay)
                        else:
                            assert(new_acc_delay <= CAP_SRPT_SBP and new_acc_delay >= 0), " Chosen position: %r, length %r , offending  %r" % (pos,len(self.queued_probes), new_acc_delay)


        return events


    #Worker class
    def get_remaining_exec_time_for_job_alt(self, job_id, current_time):
        remaining_exec_time = 0
        job_info_hash       = Job.per_job_task_info[job_id]
        for task in job_info_hash:
            val = job_info_hash[task]
            if( val == -1 ):  #task not started yet
                remaining_exec_time +=  self.simulation.jobs[job_id].estimated_task_duration
            #else:             #task started but not finished
                #remaining_exec_time +=  self.simulation.jobs[job_id].estimated_task_duration - (current_time - val)
        return remaining_exec_time

    #Worker class
    def get_remaining_exec_time_for_job_dist(self, job_id, current_time):
        job = self.simulation.jobs[job_id]
        remaining_exec_time = job.remaining_exec_time
        return remaining_exec_time

    #Worker class
    def get_remaining_exec_time_for_job(self, job_id, current_time):
        job = self.simulation.jobs[job_id]
        if (len(job.unscheduled_tasks) == 0): #Improvement
            remaining_exec_time = -1
        else:
            remaining_exec_time =  len(job.unscheduled_tasks)*job.estimated_task_duration
        return remaining_exec_time

    #Worker class
    def get_next_probe_acc_to_sbp_srpt(self, current_time):
        min_remaining_exec_time = float('inf')
        position_in_queue       = -1
        estimated_delay         = 0
        chosen_is_big           = False    

        shortest_slack_in_front_short = float('inf')

        len_queue = len(self.queued_probes)
        position_it = 0
        while position_it < len_queue:
            job_id    = self.queued_probes[position_it][0]
            remaining = self.get_remaining_exec_time_for_job_dist(job_id, current_time)

            # Improvement: taking out probes of finished jobs
            if (remaining == -1):
                self.queued_probes.pop(position_it)
                len_queue = len(self.queued_probes)
            else:
                job_bydef_big = self.simulation.jobs[job_id].job_type_for_comparison == BIG
                estimated_task_duration = self.simulation.jobs[job_id].estimated_task_duration

                jump_ok = False
                if(job_bydef_big and position_it == 0):
                    jump_ok = True
                    chosen_is_big = True
                elif(remaining < min_remaining_exec_time):
                    assert(not chosen_is_big)
                    # Check CAP jobs in front, different for short
                    jump_ok = estimated_task_duration <= shortest_slack_in_front_short

                if(jump_ok):
                    position_in_queue = position_it
                    estimated_delay = estimated_task_duration
                    min_remaining_exec_time = remaining
                    chosen_is_big = job_bydef_big
                    if (chosen_is_big):
                        break;

                    # calculate shortest slack for next probes
                if (CAP_SRPT_SBP != float('inf')):
                    slack = CAP_SRPT_SBP*estimated_task_duration - self.queued_probes[position_it][3]
                    if(CAP_SRPT_SBP == 0):
                        assert(self.queued_probes[position_it][3]==0)
                    assert (slack>=0), " offending value slack: %r CAP %r" % (slack, CAP_SRPT_SBP)

                    if(not job_bydef_big and slack < shortest_slack_in_front_short):
                        shortest_slack_in_front_short = slack
                position_it += 1

        #assert(position_in_queue>=0)

        return position_in_queue

    #Worker class
    def get_next_probe_acc_to_srpt(self, current_time):
        min_remaining_exec_time = float('inf')
        position_in_queue       = -1
        estimated_delay         = 0        

        shortest_slack_in_front = float('inf')
        for position_it in range(0,len(self.queued_probes)):
            job_id    = self.queued_probes[position_it][0]
            remaining = self.get_remaining_exec_time_for_job(job_id, current_time)
            assert(remaining >= 0)

            estimated_task_duration = self.simulation.jobs[job_id].estimated_task_duration

            if(remaining < min_remaining_exec_time):
                # Check CAP jobs in front
                if(estimated_task_duration < shortest_slack_in_front):        
                    position_in_queue = position_it
                    estimated_delay = self.simulation.jobs[job_id].estimated_task_duration
                    min_remaining_exec_time = remaining # Optimization

            # calculate shortest slack for next probes
            if (CAP_SRPT_SBP != float('inf')):
                slack = CAP_SRPT_SBP*estimated_task_duration - self.queued_probes[position_it][3] # will be negative is estimated_task_duration = 0
                if(slack < shortest_slack_in_front): #improvement: if its 0, no task will be allowed to bypass it
                    shortest_slack_in_front = slack

        assert(position_in_queue >= 0)
        # Add estimated_delay to probes in front        
        for delay_it in range(0,position_in_queue):
            new_acc_delay = self.queued_probes[delay_it][3] + estimated_delay            
            self.queued_probes[delay_it][3] = new_acc_delay

        return position_in_queue


#####################################################################################################################
#####################################################################################################################
class ApplySchedulerUpdates:
    def __init__(self, machines_and_durations, origin_scheduler_index, scheduler_indices, cluster_status_keeper, history_time, increment):
        self.origin_scheduler_index  = origin_scheduler_index
        self.machines_and_durations = machines_and_durations
        self.history_time = history_time
        self.scheduler_indices = scheduler_indices
        self.status_keeper = cluster_status_keeper
        self.increment = increment

    def run(self, current_time):
        for worker_duration in self.machines_and_durations:
            machine_id = worker_duration[0]
            duration = worker_duration[1]
            num_slots = worker_duration[2]
            for rx_scheduler_id in self.scheduler_indices:
                self.status_keeper.update_scheduler_view(self.origin_scheduler_index, rx_scheduler_id, machine_id, current_time, self.history_time, duration, num_slots, self.increment)
        return []


#####################################################################################################################
#####################################################################################################################

class Simulation(object):
    def __init__(self, monitor_interval, stealing_allowed, SCHEDULE_BIG_CENTRALIZED, WORKLOAD_FILE,small_job_th,cutoff_big_small,ESTIMATION,off_mean_bottom,off_mean_top,nr_workers):

        CUTOFF_THIS_EXP = float(small_job_th)
        TOTAL_WORKERS = int(nr_workers)
        self.jobs = {}
        self.event_queue = PriorityQueue()
        self.workers = []
        self.scheduler_indices = []

        self.index_last_worker_of_small_partition = int(SMALL_PARTITION*TOTAL_WORKERS/100)-1
        self.index_first_worker_of_big_partition  = int((100-BIG_PARTITION)*TOTAL_WORKERS/100)

        self.total_free_slots = 0
        #Heterogeneity of machines in datacenter.
        dc_composition = []
        dc_composition.append([1]) # Homogeneous. 280 cores in 35 machines.
        dc_composition.append([8, 16, 24, 32])
        dc_composition.append([8, 8, 16, 16, 24, 32])
        dc_composition.append([8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,16,16,16,16,16,24,32]) # Heterogeneous. 280 cores in 25 machines.
        possible_slots = dc_composition[SLOTS_PER_WORKER]
        while len(self.workers) < TOTAL_WORKERS:
            num_slots_idx = len(self.workers) % len(possible_slots)
            num_slots = possible_slots[num_slots_idx]
            worker = Worker(self, num_slots, len(self.workers),self.index_last_worker_of_small_partition,self.index_first_worker_of_big_partition)
            self.total_free_slots += num_slots
            self.workers.append(worker)

        self.total_slots = self.total_free_slots
        #print("Total number of cores over all machines", self.total_slots)

        self.worker_indices = range(TOTAL_WORKERS)
        self.scheduler_indices = random.sample(self.worker_indices, NUMBER_OF_SCHEDULERS)
        self.worker_indices = list(self.worker_indices)
        #print("Worker IDs are", self.worker_indices)
        print("Scheduler IDs are", self.scheduler_indices)
        for worker_id in self.scheduler_indices:
            worker = self.workers[worker_id]
            worker.init_scheduler_queue()
        self.off_mean_bottom = off_mean_bottom
        self.off_mean_top = off_mean_top
        self.ESTIMATION = ESTIMATION
        self.shared_cluster_status = {}

        #print("self.index_last_worker_of_small_partition:         ", self.index_last_worker_of_small_partition)
        #print("self.index_first_worker_of_big_partition:          ", self.index_first_worker_of_big_partition)

        self.small_partition_workers_hash =  {}
        self.big_partition_workers_hash = {}
        self.small_not_big_partition_workers_hash = {}

        self.small_partition_workers = self.worker_indices[:self.index_last_worker_of_small_partition+1]    # so not including the worker after :
        for node in self.small_partition_workers:
            self.small_partition_workers_hash[node] = 1

        self.big_partition_workers = self.worker_indices[self.index_first_worker_of_big_partition:]         # so including the worker before :
        for node in self.big_partition_workers:
            self.big_partition_workers_hash[node] = 1

        self.small_not_big_partition_workers = self.worker_indices[:self.index_first_worker_of_big_partition]  # so not including the worker after: 
        for node in self.small_not_big_partition_workers:
            self.small_not_big_partition_workers_hash[node] = 1

        #print("Size of self.small_partition_workers_hash:         ", len(self.small_partition_workers_hash))
        #print("Size of self.big_partition_workers_hash:           ", len(self.big_partition_workers_hash))
        #print("Size of self.small_not_big_partition_workers_hash: ", len(self.small_not_big_partition_workers_hash))
        #print("Number of schedulers", len(self.scheduler_indices))


        self.free_slots_small_partition = len(self.small_partition_workers)
        self.free_slots_big_partition = len(self.big_partition_workers)
        self.free_slots_small_not_big_partition = len(self.small_not_big_partition_workers)
 
        self.jobs_scheduled = 0
        self.jobs_completed = 0
        self.scheduled_last_job = False

        self.cluster_status_keeper = ClusterStatusKeeper(self.scheduler_indices)
        self.stealing_allowed = stealing_allowed
        self.SCHEDULE_BIG_CENTRALIZED = SCHEDULE_BIG_CENTRALIZED
        self.WORKLOAD_FILE = WORKLOAD_FILE
        self.btmap_tstamp = -1
        self.clusterstatus_from_btmap = None

        self.hash_jobid_to_node = {}
        self.btmap = None
        self.jobs_affected_by_holb={}  

    #Simulation class
    def subtract_sets(self, set1, set2):
        used = {}
        difference = []
        ctr_long = 0

        for item in set2:
            used[item] = 1

        for worker in set1:
            if not worker in set2:
                difference.append(worker)

        return difference


    #Simulation class
    def find_workers_random(self, probe_ratio, nr_tasks, possible_worker_indices, min_probes):
        chosen_worker_indices = []
        nr_probes = max(probe_ratio*nr_tasks,min_probes)
        for it in range(0,nr_probes):
            rnd_index = random.randint(0,len(possible_worker_indices)-1)
            chosen_worker_indices.append(possible_worker_indices[rnd_index])
        return chosen_worker_indices


    #Simulation class
    def find_workers_long_job_prio(self, num_tasks, estimated_task_duration, workers_queue_status, current_time, simulation, hash_workers_considered):

        chosen_worker_indices = []
        workers_needed = num_tasks
        prio_queue = PriorityQueue()

        empty_nodes = []  #performance optimization
        for index in hash_workers_considered:
            qlen          = workers_queue_status[index]                
            worker_obj    = simulation.workers[index]
            worker_id     = index

            if qlen == 0 :
                empty_nodes.append(worker_id)
                if(len(empty_nodes) == workers_needed):
                    break
            else: 
                start_of_crt_big_task = worker_obj.tstamp_start_crt_big_task
                assert(current_time >= start_of_crt_big_task)
                adjusted_waiting_time = qlen

                if(start_of_crt_big_task != -1):
                    executed_so_far = current_time - start_of_crt_big_task
                    estimated_crt_task = worker_obj.estruntime_crt_task
                    adjusted_waiting_time = 2*NETWORK_DELAY + qlen - min(executed_so_far,estimated_crt_task)

                assert adjusted_waiting_time >= 0, " offending value for adjusted_waiting_time: %r" % adjusted_waiting_time                 
                prio_queue.put((adjusted_waiting_time,worker_id))

        #performance optimization 
        if(len(empty_nodes) == workers_needed):
            return empty_nodes
        else:
            chosen_worker_indices = empty_nodes
            for nodeid in chosen_worker_indices:
                prio_queue.put((estimated_task_duration,nodeid))

        
        queue_length,worker = prio_queue.get()
        while (workers_needed > len(chosen_worker_indices)):
            next_queue_length,next_worker = prio_queue.get()
            while(queue_length <= next_queue_length and len(chosen_worker_indices) < workers_needed):
                chosen_worker_indices.append(worker)
                queue_length += estimated_task_duration

            prio_queue.put((queue_length,worker))
            queue_length = next_queue_length
            worker = next_worker 

        assert workers_needed == len(chosen_worker_indices)
        return chosen_worker_indices

    #Simulation class
    def find_workers_dlwl(self, estimated_task_durations, workers_queue_status, current_time,simulation, hash_workers_considered):

        chosen_worker_indices = []
        workers_needed = len(estimated_task_durations)
        prio_queue = PriorityQueue()

        for index in hash_workers_considered:
            qlen          = workers_queue_status[index]                
            worker_obj    = simulation.workers[index]

            adjusted_waiting_time = qlen
            start_of_crt_big_task = worker_obj.tstamp_start_crt_big_task # PAMELA: it will always be considered big for DLWL
            assert(current_time >= start_of_crt_big_task)

            if(start_of_crt_big_task != -1):
                executed_so_far = current_time - start_of_crt_big_task
                estimated_crt_task = worker_obj.estruntime_crt_task
                adjusted_waiting_time = max(2*NETWORK_DELAY + qlen - min(executed_so_far,estimated_crt_task),0)

            rand_dlwl = random.uniform(0, HEARTBEAT_DELAY)
            adjusted_waiting_time += rand_dlwl
            prio_queue.put((adjusted_waiting_time,index))

        # For now all estimated task duration are the same , optimize performance
        #copy_estimated_task_durations = list(estimated_task_durations)

        queue_length,worker = prio_queue.get()
        while (workers_needed > len(chosen_worker_indices)):

            next_queue_length,next_worker = prio_queue.get()
            assert queue_length >= 0
            assert next_queue_length >= 0

            while(queue_length <= next_queue_length and len(chosen_worker_indices) < workers_needed):
                chosen_worker_indices.append(worker)
                queue_length += estimated_task_durations[0] #copy_estimated_task_durations.pop(0)

            prio_queue.put((queue_length,worker))
            queue_length = next_queue_length
            worker = next_worker 

        assert workers_needed == len(chosen_worker_indices)
        return chosen_worker_indices

    #Simulation class
    def find_workers_murmuration(self, job, current_time, scheduler_index):
        global num_collisions
        #print("Job", job.id,"task durations", job.actual_task_duration, file=finished_file,)
        best_fit_for_tasks = defaultdict(tuple)
        for task_index in reversed(range(job.num_tasks)):
            chosen_worker= self.cluster_status_keeper.get_worker_with_shortest_wait(scheduler_index, current_time)
            if chosen_worker == -1 :
                #Scheduler does not exist
                print("Job", job.id, "affected by scheduler",scheduler_index,"failure")
                return None
            self.cluster_status_keeper.update_local_scheduler_view(scheduler_index, chosen_worker, self.workers[chosen_worker].num_slots, current_time, job.estimated_task_duration, True)
            #Update est time at this worker and its cores. Check for collisions by querying the actual probes on the worker.
            best_fit_for_tasks[task_index] = chosen_worker
        return best_fit_for_tasks


    #Simulation class
    def send_probes(self, job, current_time, worker_indices, btmap):
        if SYSTEM_SIMULATED == "Hawk" or SYSTEM_SIMULATED == "IdealEagle":
            return self.send_probes_hawk(job, current_time, worker_indices, btmap)
        if SYSTEM_SIMULATED == "Eagle":
            return self.send_probes_eagle(job, current_time, worker_indices, btmap)
        if SYSTEM_SIMULATED == "CLWL":
            return self.send_probes_hawk(job, current_time, worker_indices, btmap)
        if SYSTEM_SIMULATED == "DLWL":
            return self.send_probes_hawk(job, current_time, worker_indices, btmap)
        if SYSTEM_SIMULATED == "Murmuration":
            return self.send_tasks_murmuration(job, current_time, worker_indices, btmap)
        if SYSTEM_SIMULATED == "SparrowPT":
            return self.send_probes_sparrowpt(job, current_time, worker_indices, btmap)


    #Simulation class
    def send_probes_hawk(self, job, current_time, worker_indices, btmap):
        self.jobs[job.id] = job

        probe_events = []
        for worker_index in worker_indices:
            probe_events.append((current_time + NETWORK_DELAY, ProbeEvent(self.workers[worker_index], job.id, job.estimated_task_duration, job.job_type_for_scheduling, btmap, -1)))
            job.probed_workers.add(worker_index)
        return probe_events

    #Simulation class
    def send_probes_sparrowpt(self, job, current_time, worker_indices, btmap):
        self.jobs[job.id] = job

        probe_events = []
        assert len(worker_indices) == PROBE_RATIO * job.num_tasks
        count = 0
        for task_index in list(range(job.num_tasks)):
            for pr in list(range(PROBE_RATIO)):
                worker_index = worker_indices[count]
                probe_events.append((current_time + NETWORK_DELAY, ProbeEvent(self.workers[worker_index], job.id, job.estimated_task_duration, job.job_type_for_scheduling, btmap, task_index)))
                #print("Job", job.id, "task", task_index, "probe", pr, "sending to worker", worker_index)
                count += 1
                job.probed_workers.add(worker_index)
        return probe_events


    # Simulation class
    def send_tasks_murmuration(self, job, current_time, scheduler_indices, btmap):
        self.jobs[job.id] = job
        task_arrival_events = []
        # Some safety checks
        if len(scheduler_indices) != 1:
            raise AssertionError('Murmuration received more than one scheduler for the job?')
        # scheduler_index denotes the exactly one scheduler node ID where this job request lands.
        scheduler_index = scheduler_indices[0]
        workers_durations = []
        worker_indices_duration = self.find_workers_murmuration(job, current_time, scheduler_index)
        if worker_indices_duration == None:
            #Scheduler has failed. Send job to a different scheduler.
            print("Job", job.id,"is affected by scheduler", scheduler_index,"failure",file=finished_file,)
            task_arrival_events.append((current_time, NoOpSchedulingEvents(self, job)))
            return task_arrival_events
        #print("Scheduler", scheduler_index,"- Started processing job", job.id,"at", current_time)
        current_time  += SCHED_PER_JOB_OVERHEAD
        for task_index, worker_id in worker_indices_duration.items():
            current_time += SCHED_PER_TASK_OVERHEAD
            workers_durations.append((worker_id, job.estimated_task_duration, self.workers[worker_id].num_slots))
            task_arrival_events.append((current_time + NETWORK_DELAY, ProbeEvent(self.workers[worker_id], job.id, job.estimated_task_duration, BIG, btmap, task_index)))
        task_arrival_events.append((current_time + NETWORK_DELAY + UPDATE_DELAY, ApplySchedulerUpdates(workers_durations, scheduler_index, self.scheduler_indices, self.cluster_status_keeper, current_time, True)))
        task_arrival_events.append((current_time, SchedulingDoneEvents(self, scheduler_index)))
        #print("Scheduler", scheduler_index,"-Finished processing job", job.id,"at", current_time)
        return task_arrival_events


    #Simulation class
    def try_round_of_probing(self, current_time, job, worker_list, probe_events, roundnr):
        successful_worker_indices = []
        id_worker_with_newest_btmap = -1
        freshest_btmap_tstamp = self.btmap_tstamp

        for worker_index in worker_list:
            if(not self.workers[worker_index].executing_big and not self.workers[worker_index].queued_big):
                probe_events.append((current_time + NETWORK_DELAY*(roundnr/2+1), ProbeEvent(self.workers[worker_index], job.id, job.estimated_task_duration, job.job_type_for_scheduling, None, -1)))
                job.probed_workers.add(worker_index)
                successful_worker_indices.append(worker_index)
            if (self.workers[worker_index].btmap_tstamp > freshest_btmap_tstamp):
                id_worker_with_newest_btmap = worker_index
                freshest_btmap_tstamp       = self.workers[worker_index].btmap_tstamp

        if (id_worker_with_newest_btmap != -1):                    
            self.btmap = copy.deepcopy(self.workers[id_worker_with_newest_btmap].btmap)
            self.btmap_tstamp = self.workers[id_worker_with_newest_btmap].btmap_tstamp

        missing_probes = len(worker_list)-len(successful_worker_indices)
        return len(successful_worker_indices), successful_worker_indices
        

    #Simulation class
    def get_list_non_long_job_workers_from_btmap(self,btmap):
        non_long_job_workers = []
            
        non_long_job_workers = list(self.small_not_big_partition_workers[:])

        for index in self.big_partition_workers:
            if not btmap.test(index):
                non_long_job_workers.append(index)
        return non_long_job_workers


    def get_list_non_long_job_workers_from_bp_from_btmap(self,btmap):
        non_long_job_workers = []
            
        for index in self.big_partition_workers:
            if not btmap.test(index):
                non_long_job_workers.append(index)
        return non_long_job_workers

    #Simulation class
    def send_probes_eagle(self, job, current_time, worker_indices, btmap):
        global stats
        self.jobs[job.id] = job
        probe_events = []

        if (job.job_type_for_scheduling == BIG):
            for worker_index in worker_indices:
                probe_events.append((current_time + NETWORK_DELAY, ProbeEvent(self.workers[worker_index], job.id, job.estimated_task_duration, job.job_type_for_scheduling, btmap, -1)))
                job.probed_workers.add(worker_index)

        else:
            missing_probes = len(worker_indices)
            self.btmap_tstamp = -1
            self.btmap = None
            ROUNDS_SCHEDULING = 2 

            #use local bitmap
            #self.btmap        = self.workers[self.hash_jobid_to_node[job.id]].btmap
            #self.btmap_tstamp = self.workers[self.hash_jobid_to_node[job.id]].btmap_tstamp
            #ROUNDS_SCHEDULING = 2
            
            #if(self.btmap != None):
             #   list_non_long_job_workers = self.get_list_non_long_job_workers_from_btmap(self.btmap)
              #  worker_indices = self.find_workers_random(1, missing_probes, list_non_long_job_workers, 0)
            #else:
             #   stats.STATS_RND_FIRST_ROUND_NO_LOCAL_BITMAP +=1 

             #small
            #worker_indices = self.find_workers_random(PROBE_RATIO,job.num_tasks,self.big_partition_workers,MIN_NR_PROBES)

 
            stats.STATS_ROUNDS_ATTEMPTS +=1
            for i in range(0,ROUNDS_SCHEDULING):
                ok_nr, ok_nodes = self.try_round_of_probing(current_time,job,worker_indices,probe_events,i+1)  
                if(i==0):
                    stats.STATS_PERC_1ST_ROUNDS+=ok_nr*1.0/missing_probes
                missing_probes -= ok_nr
                stats.STATS_ROUNDS +=1
                

                if(missing_probes == 0):
                    return probe_events
 
                assert(missing_probes >= 0)               
 
                list_non_long_job_workers = self.get_list_non_long_job_workers_from_btmap(self.btmap)
                #small
                #list_non_long_job_workers = self.get_list_non_long_job_workers_from_bp_from_btmap(self.btmap)
                #if(len(list_non_long_job_workers)==0):
                 #   break
                worker_indices = self.find_workers_random(1, missing_probes, list_non_long_job_workers,0)
                stats.STATS_REASSIGNED_PROBES += missing_probes

            if(missing_probes > 0):
                worker_indices = self.find_workers_random(1, missing_probes, self.small_not_big_partition_workers,0)
                self.try_round_of_probing(current_time,job,worker_indices,probe_events,ROUNDS_SCHEDULING+1)  
                stats.STATS_FALLBACKS_TO_SP +=1
        
        return probe_events



    #Simulation class
    #bookkeeping for tracking the load
    def increase_free_slots_for_load_tracking(self, worker):
        self.total_free_slots += 1
        if(worker.in_small):                self.free_slots_small_partition += 1
        if(worker.in_big):                  self.free_slots_big_partition += 1
        if(worker.in_small_not_big):        self.free_slots_small_not_big_partition += 1


    #Simulation class
    #bookkeeping for tracking the load
    def decrease_free_slots_for_load_tracking(self, worker):
        self.total_free_slots -= 1
        if(worker.in_small):                self.free_slots_small_partition -= 1
        if(worker.in_big):                  self.free_slots_big_partition -= 1
        if(worker.in_small_not_big):        self.free_slots_small_not_big_partition -= 1


    #Simulation class
    def get_task(self, job_id, worker, current_time, task_index, queue_start_time):
        job = self.jobs[job_id]
        #account for the fact that this is called when the probe is launched but it needs an RTT to talk to the scheduler
        get_task_response_time = current_time + 2 * NETWORK_DELAY
        
        if len(job.unscheduled_tasks) == 0 :
            #Redundant probe.
            return False, [(get_task_response_time, NoopGetTaskResponseEvent(worker))]

        task_duration = 0
        if task_index > -1:
            task_duration = job.actual_task_duration[task_index]
            if task_duration in  job.unscheduled_tasks:
                job.unscheduled_tasks.remove(task_duration)
            else:
                #Redundant probe.
                return False, [(get_task_response_time, NoopGetTaskResponseEvent(worker))]
        else:
            task_duration = job.unscheduled_tasks.pop()
        this_task_id=job.completed_tasks_count
        Job.per_job_task_info[job_id][this_task_id] = current_time
        events = []
        worker.busy_time += task_duration
        task_completion_time = task_duration + get_task_response_time
        task_wait_time = current_time - queue_start_time
        #print(current_time, " worker:", worker.id, " num_slots ", worker.num_slots, " task from job ", job_id, " task duration: ", task_duration, " will finish at time ", task_completion_time, file=finished_file,)
        '''
        qlens = []
        for worker in self.workers:
            qlens.append(worker.queue_length())
        print("Worker occupancy", qlens, file=finished_file,)
        '''
        is_job_complete = job.update_task_completion_details(task_completion_time, task_wait_time)

        if is_job_complete:
            self.jobs_completed += 1;
            print(job.end_time," estimated_task_duration: ",job.estimated_task_duration, " job_id: ",job.id, " total_job_running_time: ",(job.end_time - job.start_time), "job_start:", job.start_time, "job_end:", job.end_time, "average TCT" , job.tct / job.num_tasks, "tail TCT", job.tail_tct, "average w2x", job.w2x/ job.num_tasks, file=finished_file)
            #print(job.end_time," job", job.id, "JCT", (job.end_time - job.start_time))

        events.append((task_completion_time, TaskEndEvent(worker, self.SCHEDULE_BIG_CENTRALIZED, self.cluster_status_keeper, job.id, job.job_type_for_scheduling, job.estimated_task_duration, this_task_id, task_duration)))
        
        if SRPT_ENABLED and SYSTEM_SIMULATED == "Eagle":
                events.append((current_time + 2*NETWORK_DELAY, UpdateRemainingTimeEvent(job)))

        if SYSTEM_SIMULATED == "Murmuration":
            workers_durations  = tuple([worker.id, job.estimated_task_duration, worker.num_slots])
            if LOCAL_SCHEDULER_UPDATE and worker.id in self.scheduler_indices:
                #Apply instant update to this scheduler.
                self.cluster_status_keeper.update_local_scheduler_view(worker.id, worker.id,worker.num_slots, current_time, job.estimated_task_duration, False)
                #Apply delayed updates to all other schedulers.
                events.append((task_completion_time + NETWORK_DELAY + UPDATE_DELAY, ApplySchedulerUpdates([workers_durations], worker.id, self.scheduler_indices, self.cluster_status_keeper, current_time, False)))
            else:
                #Apply delayed updates to all schedulers.
                events.append((task_completion_time + NETWORK_DELAY + UPDATE_DELAY, ApplySchedulerUpdates([workers_durations], -1, self.scheduler_indices, self.cluster_status_keeper, current_time, False)))

        if len(job.unscheduled_tasks) == 0:
            logging.info("Finished scheduling tasks for job %s" % job.id)
        return True, events


    #Simulation class
    def get_probes(self, current_time, free_worker_id):
        worker_index = random.randint(self.index_first_worker_of_big_partition, len(self.workers)-1)
        if     (STEALING_STRATEGY ==  "ATC"):       probes = self.workers[worker_index].get_probes_atc(current_time, free_worker_id)
        elif (STEALING_STRATEGY == "RANDOM"):       probes = self.workers[worker_index].get_probes_random(current_time, free_worker_id)

        return worker_index,probes

    #Simulation class
    def run(self):
        global utilization
        global time_elapsed_in_dc
        global total_busyness
        global start_time_in_dc
        last_time = 0
        unique = count()

        self.jobs_file = open(self.WORKLOAD_FILE, 'r')

        self.task_distribution = TaskDurationDistributions.FROM_FILE

        estimate_distribution = EstimationErrorDistribution.MEAN
        if(self.ESTIMATION == "MEAN"):
            estimate_distribution = EstimationErrorDistribution.MEAN
            self.off_mean_bottom = self.off_mean_top = 0
        elif(self.ESTIMATION == "CONSTANT"):
            estimate_distribution = EstimationErrorDistribution.CONSTANT
            assert(self.off_mean_bottom == self.off_mean_top)
        elif(self.ESTIMATION == "RANDOM"):
            estimate_distribution = EstimationErrorDistribution.RANDOM
            assert(self.off_mean_bottom > 0)
            assert(self.off_mean_top > 0)
            assert(self.off_mean_top>self.off_mean_bottom)

        if(SYSTEM_SIMULATED == "DLWL"):
            self.shared_cluster_status = self.cluster_status_keeper.get_queue_status()
            self.event_queue.put((0, next(unique), WorkerHeartbeatEvent(self)))
        if FT_ENABLED:
            self.event_queue.put((0, next(unique), PeriodicSchedulerFailureAttempt(self)))

        line = self.jobs_file.readline()
        new_job = Job(self.task_distribution, line, estimate_distribution, self.off_mean_bottom, self.off_mean_top)
        start_time_in_dc = (float(line.split()[0])) / SPEEDUP
        self.event_queue.put((start_time_in_dc, next(unique), JobArrival(self, self.task_distribution, new_job, self.jobs_file)))
        self.jobs_scheduled = 1
        #self.event_queue.put((start_time_in_dc, next(unique), PeriodicTimerEvent(self)))

        while (not self.event_queue.empty()):
            current_time, num, event = self.event_queue.get()
            if current_time < last_time:
                raise AssertionError("Got current time "+ str(current_time)+" less than last time "+ str(last_time))
            last_time = current_time
            new_events = event.run(current_time)
            for priority, item in new_events:
                self.event_queue.put((priority, next(unique), item))

        for worker in self.workers:
            total_busyness += worker.busy_time


        print("Simulation ending, no more events. Jobs completed", self.jobs_completed)
        self.jobs_file.close()

        # Calculate utilizations of workers in DC
        time_elapsed_in_dc = current_time - start_time_in_dc
        utilization = 100 * (float(total_busyness) / float(time_elapsed_in_dc * self.total_slots))
        print("Total time elapsed in the DC is", time_elapsed_in_dc, "s and utilization is", utilization)
        print("Total time elapsed in the DC is", time_elapsed_in_dc, "s and utilization is", utilization, file=finished_file)

#####################################################################################################################
#globals
utilization = 0.0
time_elapsed_in_dc = 0.0
total_busyness = 0.0
start_time_in_dc = 0.0
num_collisions = 0
job_count = 1

finished_file   = open('finished_file', 'w')
load_file       = open('load_file', 'w')
stats_file      = open('stats_file', 'w')

NETWORK_DELAY = 0.0005
BIG = 1
SMALL = 0
SPEEDUP = 1000

job_start_tstamps = {}

random.seed(datetime.now().timestamp())
#random.seed(123456789)
if(len(sys.argv) != 28):
    print("Incorrect number of parameters.")
    sys.exit(1)


WORKLOAD_FILE                   = sys.argv[1]
stealing                        = (sys.argv[2] == "yes")
SCHEDULE_BIG_CENTRALIZED        = (sys.argv[3] == "yes")
CUTOFF_THIS_EXP                 = float(sys.argv[4])        #
CUTOFF_BIG_SMALL                = float(sys.argv[5])        #
SMALL_PARTITION                 = float(sys.argv[6])          #from the start of worker_indices
BIG_PARTITION                   = float(sys.argv[7])          #from the end of worker_indices
SLOTS_PER_WORKER                = int(sys.argv[8])
if SLOTS_PER_WORKER not in [0,1,2,3]:
    print("Heterogeneity options are 0,1,2,3.")
    sys.exit(1)
PROBE_RATIO                     = int(sys.argv[9])
MONITOR_INTERVAL                = int(sys.argv[10])
ESTIMATION                      = sys.argv[11]              #MEAN, CONSTANT or RANDOM
OFF_MEAN_BOTTOM                 = float(sys.argv[12])       # > 0
OFF_MEAN_TOP                    = float(sys.argv[13])       # >= OFF_MEAN_BOTTOM
STEALING_STRATEGY               = sys.argv[14]
STEALING_LIMIT                  = int(sys.argv[15])         #cap on the nr of tasks to steal from one node
STEALING_ATTEMPTS               = int(sys.argv[16])         #cap on the nr of nodes to contact for stealing
TOTAL_WORKERS                   = int(sys.argv[17])
SRPT_ENABLED                    = (sys.argv[18] == "yes")
HEARTBEAT_DELAY                 = float(sys.argv[19]) / SPEEDUP
MIN_NR_PROBES                   = int(sys.argv[20])
SBP_ENABLED                     = (sys.argv[21] == "yes")
SYSTEM_SIMULATED                = sys.argv[22]
NUMBER_OF_SCHEDULERS            = int(sys.argv[23])
UPDATE_DELAY                    = float(sys.argv[24])
LOCAL_SCHEDULER_UPDATE          = (sys.argv[25] == "yes")
if sys.argv[25] not in ["yes", "no"]:
    print("Local scheduler update should be a yes or a no")
    sys.exit(1)
SCHED_REORDER_TECHNIQUE         = sys.argv[26]
if SCHED_REORDER_TECHNIQUE not in ["FCFS", "SJF", "LRTF", "SRJF"]:
    print("Scheduler queue re-ordering options are FCFS, SJF, LRTF and SRJF")
    sys.exit(1)
FT_ENABLED                      = (sys.argv[27] == "yes")

SCHED_PER_JOB_OVERHEAD = 0.1
SCHED_PER_TASK_OVERHEAD = 0.005

#How much time does it take for a scheduler to restart?
SCHEDULER_RESTART_TIME = 10
#If there are no schedulers available, how often must a job check?
JOB_CHECK_SCHEDULER_AVAILABILITY = 1
#Maximum jitter in the rtt of a cache request and response
CACHE_RESPONSE_TIME_JITTER = 3

#MIN_NR_PROBES = 20 #1/100*TOTAL_WORKERS
CAP_SRPT_SBP = 5 #cap on the % of slowdown a job can tolerate for SRPT and SBP

t1 = time.time()

stats = Stats()
s = Simulation(MONITOR_INTERVAL, stealing, SCHEDULE_BIG_CENTRALIZED, WORKLOAD_FILE,CUTOFF_THIS_EXP,CUTOFF_BIG_SMALL,ESTIMATION,OFF_MEAN_BOTTOM,OFF_MEAN_TOP,TOTAL_WORKERS)
s.run()

print("Simulation ended in ", (time.time() - t1), " s ", file=finished_file,)
print("Simulation ended in ", (time.time() - t1), " s ")

finished_file.close()
load_file.close()


print("STATS_SH_PROBES_ASSIGNED_IN_BP:      ",    stats.STATS_SH_PROBES_ASSIGNED_IN_BP, file=stats_file)
print("STATS_SH_PROBES_QUEUED_BEHIND_BIG:      ",    stats.STATS_SH_PROBES_QUEUED_BEHIND_BIG, file=stats_file) 
print("STATS_TASKS_SH_EXEC_IN_BP:             ",     stats.STATS_TASKS_SH_EXEC_IN_BP, file=stats_file)
print("STATS_SHORT_TASKS_WAITED_FOR_BIG:         ",           stats.STATS_SHORT_TASKS_WAITED_FOR_BIG, file=stats_file)
print("STATS_SHORT_JOBS_HAVING_TASKS_THAT_WAITED_FOR_BIG:         ",           len(s.jobs_affected_by_holb), file=stats_file)
print("                                 ", file=stats_file)
print("STATS_TOTAL_STOLEN_PROBES:        ",           stats.STATS_TOTAL_STOLEN_PROBES, file=stats_file)
print("STATS_TOTAL_STOLEN_B_FROM_B_PROBES:        ",           stats.STATS_TOTAL_STOLEN_B_FROM_B_PROBES, file=stats_file) 
print("STATS_TOTAL_STOLEN_S_FROM_S_PROBES:        ",           stats.STATS_TOTAL_STOLEN_S_FROM_S_PROBES , file=stats_file)
print("STATS_TOTAL_STOLEN_S_FROM_B_PROBES:        ",           stats.STATS_TOTAL_STOLEN_S_FROM_B_PROBES , file=stats_file)
print("STATS_SHORT_UNSUCC_PROBES_IN_BIG:        ",           stats.STATS_SHORT_UNSUCC_PROBES_IN_BIG , file=stats_file)
    
print("STATS_SUCCESSFUL_STEAL_ATTEMPTS: ",           stats.STATS_SUCCESSFUL_STEAL_ATTEMPTS, file=stats_file)
print("STATS_STEALING_MESSAGES:         ",           stats.STATS_STEALING_MESSAGES, file=stats_file)
print("                                 ", file=stats_file)
print("STATS_STICKY_EXECUTIONS:             ",           stats.STATS_STICKY_EXECUTIONS, file=stats_file)
print("STATS_STICKY_EXECUTIONS_IN_BP:             ",           stats.STATS_STICKY_EXECUTIONS_IN_BP, file=stats_file)
print("STATS_REASSIGNED_PROBES:             ",           stats.STATS_REASSIGNED_PROBES, file=stats_file)
print("STATS_BYPASSEDBYBIG_AND_STUCK:             ",           stats.STATS_BYPASSEDBYBIG_AND_STUCK, file=stats_file)
print("STATS_FALLBACKS_TO_SP:             ",           stats.STATS_FALLBACKS_TO_SP, file=stats_file)
print("STATS_RND_FIRST_ROUND_NO_LOCAL_BITMAP:             ",           stats.STATS_RND_FIRST_ROUND_NO_LOCAL_BITMAP, file=stats_file)
if(stats.STATS_ROUNDS_ATTEMPTS!=0):
    print("STATS_ROUNDS/STATS_ROUNDS_ATTEMPTS:             ",           stats.STATS_ROUNDS*1.0/stats.STATS_ROUNDS_ATTEMPTS, file=stats_file)
    print("STATS_PERC_1ST_ROUNDS/STATS_ROUNDS_ATTEMPTS:    ",           stats.STATS_PERC_1ST_ROUNDS*1.0/stats.STATS_ROUNDS_ATTEMPTS, file=stats_file)
print("                                 ", file=stats_file)
print("STATS_TASKS_TOTAL_FINISHED:             ",          stats.STATS_TASKS_TOTAL_FINISHED, file=stats_file)
print("STATS_TASKS_SHORT_FINISHED:             ",          stats.STATS_TASKS_SHORT_FINISHED, file=stats_file)
print("STATS_TASKS_LONG_FINISHED:             ",          stats.STATS_TASKS_LONG_FINISHED, file=stats_file)
print("STATS_JOBS_FINISHED:             ",          s.jobs_scheduled, file=stats_file)

if(SYSTEM_SIMULATED=="Eagle" and stats.STATS_TASKS_SHORT_FINISHED > 0):
    print("%TASKS AFFECTED BY HOLB ",stats.STATS_SHORT_TASKS_WAITED_FOR_BIG*1.0/stats.STATS_TASKS_SHORT_FINISHED," %JOBS ",len(s.jobs_affected_by_holb)*1.0/s.jobs_scheduled, file=stats_file)

stats_file.close()
