import numpy as np
import sys

jct = []
infile = open(sys.argv[1], 'r')
for line in infile:
        if "estimated_task_duration:" not in line:
            continue
        line = line.split()
        #print(line)
        completion_time = float(line[6])
        jct.append(completion_time)
#print("JCT is", jct)
print("JCT Percentiles -",np.percentile(jct,50), np.percentile(jct,90), np.percentile(jct,99))
