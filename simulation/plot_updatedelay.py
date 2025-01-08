from matplotlib import pyplot as plt, rcParams
import numpy as np
from palettable.colorbrewer.qualitative import Set2_7
import os

colors = Set2_7.mpl_colors
params = {
   'axes.labelsize': 16,
   'font.size': 16,
   'legend.fontsize': 12,
   'xtick.labelsize': 16,
   'ytick.labelsize': 16,
   'text.usetex': False,
   'figure.figsize': [7.6, 2.4]
}
rcParams.update(params)

jct_systems = {}
utilization = {}
dirname='results/update_delay'
delay = ["100ms","1s","10s", "100s"]
numschs = [25, 50, 75, 100]
ls = ['solid', 'dashed', 'dotted', 'dashdot']
for filename in os.listdir(dirname):
            delay_idx = -1
            numsch = -1
            if "_100ms" in filename:
               delay_idx = "100ms"
            elif "_1s" in filename:
               delay_idx = "1s"
            elif "_10s" in filename:
               delay_idx = "10s"
            elif "_100s" in filename:
               delay_idx = "100s"
            else:
               continue
            if "_0.25S_" in filename:
                numsch = 25
            elif "_0.5S_" in filename:
                numsch = 50
            elif "_0.75S_" in filename:
                numsch = 75
            elif "_1S_" in filename:
                numsch = 100
            else:
                continue
            if delay_idx not in jct_systems.keys():
                jct_systems[delay_idx] = {}
            if numsch not in jct_systems[delay_idx].keys():
                jct_systems[delay_idx][numsch] = []
            with open(os.path.join(dirname, filename), 'r') as infile:
                jct=[]
                for line in infile:
                    if "estimated_task_duration:" not in line:
                        continue
                    line = line.split()
                    completion_time = float(line[6])
                    jct.append(completion_time)
                print("JCT Percentiles for ",filename,"is",np.percentile(jct,50), np.percentile(jct,99))
            jct.sort()
            jct_systems[delay_idx][numsch] = jct

for delay_idx in delay:
    count = 0
    fig, ax1 = plt.subplots()
    jct_systems[delay_idx][25].sort()
    baseline = jct_systems[delay_idx][25]
    x = range(1, len(baseline)+1)
    ax1.plot(baseline, label=str(25)+"% schedulers", color=colors[count+1])
    count += 1
    for numsch in numschs:
        if numsch == 25:
            continue
        #ax1.plot(jct_systems[delay_idx][numsch], label=str(numsch)+"% schedulers", color=colors[count])
        jct_systems[delay_idx][numsch].sort()
        error = [a- b for a, b in zip(jct_systems[delay_idx][numsch], baseline)]
        #print(error)
        e1 = ax1.errorbar(x, baseline, yerr = error, label=str(numsch)+"% schedulers", color=colors[count+1], errorevery=(count*333,1000), fmt='none', capsize=5)
        e1[-1][0].set_linestyle(ls[count])
        count += 1
    ax1.set_xlabel("Jobs")
    ax1.set_ylabel("Job Completion Time (s)")
    ax1.locator_params(axis="both", nbins=5)
    ax1.legend(loc='upper left')
    name = "simulation_cdf_" + str(delay_idx) + ".pdf"
    fig.savefig(name, dpi=fig.dpi, bbox_inches='tight')
