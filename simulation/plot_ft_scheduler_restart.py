import csv
import numpy as np
import collections
import random
from matplotlib import pyplot as plt, rcParams
from collections import defaultdict
from palettable.colorbrewer.qualitative import Set2_7
from bisect import bisect
import os
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

colors = Set2_7.mpl_colors
params = {
   'axes.labelsize': 14,
   #'font.size': 10,
   'legend.fontsize': 14,
   'xtick.labelsize': 14,
   'ytick.labelsize': 14,
   'text.usetex': False,
   'figure.figsize': [4, 2]
}
rcParams.update(params)

jct_systems = defaultdict(list)
dirname="./results_new/ft2/"
#Ensure failed is parsed before the corresponding notfailed.
for filename in os.listdir(dirname):
    if "notfailed" in filename:
        system = 0
    else:
        system = 1
    jct = []
    with open(os.path.join(dirname, filename), 'r') as infile:
        for line in infile:
            if "total_job_running_time" not in line:
                continue
            line = line.split()
            completion_time = float(line[6])
            jct.append(completion_time)
    jct.sort()
    if len(jct) > 0:
        print("Processing", filename, ":",np.percentile(jct,50), np.percentile(jct,99))
        jct_systems[system].append(jct)

fig, ax1 = plt.subplots()
systems=["No New Schedulers", "1 New Scheduler"]
styles=["--",":"]
for system in range(len(systems)):
    mean = np.mean(jct_systems[system], axis=0)
    std = np.std(jct_systems[system], axis=0)
    x = range(len(mean))
    #Plot the mean of the runs
    ax1.plot(x, mean, label=systems[system], color=colors[system], linewidth=2,  alpha=0.5, linestyle=styles[system])
    print(systems[system],":", np.percentile(mean, 50), np.percentile(mean, 90), np.percentile(mean, 99))
    #Plot the std
    ax1.fill_between(x,mean+std, mean-std, facecolor=colors[system], alpha=0.4)
ax1.set_xlabel("Jobs")
ax1.set_ylabel("JCT (1,000 seconds)")
ax1.set_yticks([0,25000, 50000, 75000])
ax1.set_yticklabels([0,25, 50, 75])
ax1.legend()
fig.savefig('ftjct_newsched.pdf', dpi=fig.dpi, bbox_inches='tight')
