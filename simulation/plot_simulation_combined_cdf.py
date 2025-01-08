from matplotlib import pyplot as plt, rcParams
import numpy as np
from palettable.colorbrewer.qualitative import Set2_7
import os

colors = Set2_7.mpl_colors
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

jct_systems = {}
utilization = {}
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
            if size_idx not in jct_systems.keys():
                jct_systems[size_idx] = {}
            if system not in jct_systems[size_idx].keys():
                jct_systems[size_idx][system] = []
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
                sorted(jct)
                print("JCT Percentiles for ",filename,"is",np.percentile(jct,50), np.percentile(jct,90), np.percentile(jct,99))
            #Over-write rundirs
            jct_systems[size_idx][system] = jct

systems = ["Murmuration-SRJF", "Murmuration-FCFS", "Sparrow", "Eagle", "Yaq-d"]
for dcsize in size:
    count = 0
    fig, ax1 = plt.subplots()
    for system in systems:
        ax1.plot(jct_systems[dcsize][system], label=system, color=colors[count])
        count += 1
    ax1.set_xlabel("Jobs")
    ax1.set_ylabel("Job Completion Time (s)")
    ax1.legend()
    name = "simulation_cdf_" + str(dcsize) + ".pdf"
    fig.savefig(name, dpi=fig.dpi, bbox_inches='tight')
