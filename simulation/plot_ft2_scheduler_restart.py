import csv
import numpy as np
import collections
import random
from matplotlib import pyplot as plt, rcParams
from collections import defaultdict
from palettable.colorbrewer.qualitative import Set2_7
from bisect import bisect
import os

colors = Set2_7.mpl_colors
params = {
   'axes.labelsize': 14,
   #'font.size': 10,
   'legend.fontsize': 14,
   'xtick.labelsize': 14,
   'ytick.labelsize': 14,
   'text.usetex': False,
   'figure.figsize': [6.4, 2.4]
}
rcParams.update(params)

jct_systems = defaultdict(dict)
#dirname="./results_new/ft/"
dirname="./results_new/ft2/"
#Ensure failed is parsed before the corresponding notfailed.
jobids_considered = []
for filename in os.listdir(dirname):
    if "finished.failed.10000.3" in filename:
        system = 1
    else:
        continue
    with open(os.path.join(dirname, filename), 'r') as infile:
        print("Processing", filename)
        failed_sched_id = -1
        for line in infile:
            if system == 1:
                #First look for the failed scheduler's id
                if line.startswith("0 Scheduler") and "failed" in line:
                    failed_sched_id = int((line.split())[2])
                assert failed_sched_id != -1
                #Look for all jobs that have been assigned to this restarted scheduler
                search = "assigned to scheduler " + str(failed_sched_id)
                if search in line:
                    jobid = int((line.split())[3])
                    jobids_considered.append(jobid)
                    continue
                if "total_job_running_time" not in line:
                    continue
                line = line.split()
                jobid = int(line[4])
                if jobid not in jobids_considered:
                    continue
                completion_time = float(line[6])
                if jobid not in jct_systems[system].keys():
                    jct_systems[system][jobid] = []
                jct_systems[system][jobid].append(completion_time)

assert len(jobids_considered) == len(jct_systems[1].keys())

for filename in os.listdir(dirname):
    if "finished.notfailed.10000.3" in filename:
        system = 0
    else:
        continue
    with open(os.path.join(dirname, filename), 'r') as infile:
        print("Processing", filename)
        for line in infile:
            if system == 0:
                if "total_job_running_time" not in line:
                    continue
                line = line.split()
                jobid = int(line[4])
                if jobid in jobids_considered:
                    completion_time = float(line[6])
                    if jobid not in jct_systems[system].keys():
                        jct_systems[system][jobid] = []
                    jct_systems[system][jobid].append(completion_time)

assert len(jobids_considered) == len(jct_systems[0].keys())
fig, ax1 = plt.subplots()
systems=["No New Schedulers", "1 New Scheduler"]
'''
for system in reversed(range(len(systems))):
    #mean = np.mean(jct_systems[system], axis=0)
    #std = np.std(jct_systems[system], axis=0)
    #x = range(len(jct_systems[system]))
    #Plot the mean of the runs
    jct = []
    jobids = []
    for jobid in sorted(jct_systems[system].keys()):
        jobids.append(jobid)
        jct.append(jct_systems[system][jobid])
    ax1.plot(jobids, jct, label=systems[system], color=colors[system], linewidth=2,  alpha=0.5)
    #print(systems[system],":", np.percentile(mean, 50), np.percentile(mean, 90), np.percentile(mean, 99))
    #Plot the std
    #ax1.fill_between(x,mean+std, mean-std, facecolor=colors[system], alpha=0.4)
'''
for system in (range(len(systems))):
    jct = []
    for jobid in sorted(jct_systems[system].keys()):
        jct.append(jct_systems[system][jobid])
    jct = sorted(jct)
    ax1.plot(jct, label=systems[system], color=colors[system], linewidth=2,  alpha=0.5)
    print(systems[system],":", np.percentile(jct, 50), np.percentile(jct, 90), np.percentile(jct, 99))
    #Plot the std
    #ax1.fill_between(x,mean+std, mean-std, facecolor=colors[system], alpha=0.4)
ax1.set_xlabel("Jobs")
ax1.set_ylabel("Job Completion Time (s)")
#ax1.set_yticks([0,200, 400, 600])
ax1.legend()
fig.savefig('ftjct_newsched2_r3.pdf', dpi=fig.dpi, bbox_inches='tight')
