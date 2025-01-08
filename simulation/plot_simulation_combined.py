from matplotlib import pyplot as plt, rcParams
import numpy as np
from palettable.colorbrewer.qualitative import Pastel2_7
import os

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

colors = Pastel2_7.mpl_colors
params = {
   'axes.labelsize': 10,
   'font.size': 10,
   'legend.fontsize': 9,
   'xtick.labelsize': 10,
   'ytick.labelsize': 10,
   'text.usetex': False,
   'figure.figsize': [7.6, 3]
}
rcParams.update(params)

jct_systems_50 = {}
utilization = {}
jct_systems_99 = {}
jct = []
system = ""
dirname='results_new/rebuttal/1000X_YH'
size = [1000, 5000,10000, 15000]
#Each contains 5 runs.
for run_dir in os.listdir(dirname):
        for filename in os.listdir(os.path.join(dirname, run_dir)):
            if "1000S." in filename:
               continue
            if "yaqc." in filename:
               continue
            size_idx = -1
            if ".10000N." in filename:
               size_idx=10000
            elif ".1000N." in filename:
               size_idx=1000
            elif ".5000N." in filename:
               size_idx=5000
            elif ".15000N." in filename:
               size_idx=15000
            assert size_idx > -1
            if "h.10000J." in filename:
                system = "Sparrow"
            if "eagle.10000J." in filename:
                system = "Eagle"
            if "m.10000J." in filename:
                if "fcfs" in filename:
                    system = "Murmuration-FCFS"
                if "srjf" in filename:
                    system = "Murmuration-SRJF"
            #if "yaqc.10000J." in filename:
            #    system="Yaq-c"
            if "yaqd.10000J." in filename:
                system="Yaq-d"
            if system not in jct_systems_50.keys():
                jct_systems_50[system] = {}
                jct_systems_99[system] = {}
                utilization[system] = {}
            if size_idx not in jct_systems_50[system].keys():
                jct_systems_50[system][size_idx] = []
                jct_systems_99[system][size_idx] = []
                utilization[system][size_idx] = []
            with open(os.path.join(dirname, run_dir, filename), 'r') as infile:
                jct=[]
                u = 0.0
                for line in infile:
                    if "Total time elapsed in the DC is" in line and "and utilization is" in line:
                        u = float((line.split())[12])
                        continue
                    if "estimated_task_duration:" not in line:
                        continue
                    line = line.split()
                    completion_time = float(line[6])
                    jct.append(completion_time)
                assert u > 0.0
                print("JCT Percentiles for ",filename,"is",np.percentile(jct,50), np.percentile(jct,90), np.percentile(jct,99))
            jct_systems_50[system][size_idx].append(np.percentile(jct, 50))
            jct_systems_99[system][size_idx].append(np.percentile(jct, 99))
            utilization[system][size_idx].append(u)
xsize=np.arange(len(size))
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
labels=[]
width=0.6
distance = 3.5
count = 0
error_bar_heights = []
systems = ["Murmuration-SRJF", "Murmuration-FCFS", "Sparrow", "Eagle", "Yaq-d"]
for system in systems:
    mean = []
    std = []
    util = []
    for dcsize in size:
        mean.append(np.mean(jct_systems_50[system][dcsize]))
        std.append(np.std(jct_systems_50[system][dcsize]))
        util.append(np.mean(utilization[system][dcsize]))
    print("System", system,mean, std)
    ax1.bar((xsize)*distance + count*width - 2*width, mean, yerr=std,width=width, label=system, color=colors[count], capsize=2)
    if system == "Murmuration-SRJF":
        murmuration = mean
    #Plot the utilization 
    ax2.scatter((xsize)*distance + count*width - 2*width, util, c=[colors[count]], edgecolors='black', alpha=1, marker='x')
    system_labels = [i/j for i,j in zip(mean,murmuration)]
    labels.extend(system_labels)
    error_bar_heights.extend(std)
    count += 1
ax1.set_xlabel("Cluster Size")
ax1.set_ylabel("JCT (10,000 seconds)")
ax2.set_ylabel("Utilization (%)")
xsize = [(i)*distance for i in xsize]
ax1.set_xticks(xsize)
ax1.set_yticks([0,50000, 100000, 150000, 200000, 250000, 300000])
ax1.set_yticklabels(['0', '5', '10', '15', '20', '25', '30'])
#ax1.set_yticks([0,500000, 1000000, 1500000, 2000000])
#ax1.set_yticklabels(['0', '50', '100', '150', '200'])
ax2.set_yticks([0,25, 50, 75, 100])
#ax1.legend(ncol=2, bbox_to_anchor=(1, 1.1))
ax1.legend(ncol=2, loc='center', bbox_to_anchor=(0.5, 0.4))
ax1.set_xticklabels([str(n) for n in size])
#Labels on other bars
rects = ax1.patches[0:24]
for rect,label, err_height in zip(rects, labels, error_bar_heights):
    height = rect.get_height() + err_height
    ax1.text(rect.get_x() + rect.get_width() / 2, height + 4, "{:.0f}".format(label), ha="center", va="bottom", fontsize='small')
fig.savefig('simulation_jcts_yh_50.pdf', dpi=fig.dpi, bbox_inches='tight')
