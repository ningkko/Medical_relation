lengths=[]
with open("multi_str.txt",'r') as fp:
	line = fp.readline()
	while line:
		strings = line.split("\t")[1]
		lengths.append(len(strings.split("||")))
		line = fp.readline()

lengths[:] = (value for value in lengths if value != 2 and value!=3)
import matplotlib.pyplot as plt
plt.hist(lengths, color = 'pink', edgecolor = 'black', bins = len(set(lengths)))
plt.xlabel('Number of strings')
plt.ylabel('Freq')
plt.savefig("freq_dist.png")

import statistics as sss

print("Mean: %i, median: %i, std: %f"%(sss.mean(lengths),sss.median(lengths),sss.stdev(lengths)))
