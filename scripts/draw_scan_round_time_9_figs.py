#-*- utf-8 -*-
import re
import matplotlib.pyplot as plt
import numpy as np

BASE = "../datasets/scantime"
fig_index = 0
mean_time = []
std_time = []
for folder in ["a","b","c","d","e","f","g","h"]:
	INPUT_FILENAME = BASE+"/"+folder+"/wifi.txt"
	f = open(INPUT_FILENAME)
	time_list = []
	while True:
		line = f.readline()
		if not line: break
		time_search = re.search("^(\d+?);",line)
		time_list.append(int(time_search.group(1)))
	f.close()

	round_time_list = []
	prev_time = time_list[0]
	for i in range(1,len(time_list)):
		round_time_list.append((time_list[i]-prev_time)/1000.0)
		prev_time = time_list[i]

	#print(round_time_list)
	first_time = (time_list[1]-time_list[0])/1000.0
	last_time = (time_list[-1]-time_list[0])/1000.0
	x = np.linspace(first_time,last_time,len(round_time_list),endpoint=True)
	fig_index += 1
	mean_time.append(np.mean(round_time_list))
	std_time.append(np.std(round_time_list))
	plt.subplot(3,3,fig_index)
	plt.plot(x,round_time_list)

plt.subplot(3,3,9)
#plt.plot(range(1,9),mean_time)
plt.errorbar(range(1,9),mean_time,yerr=std_time,ecolor='g')
print(np.min(mean_time))
print(np.max(mean_time))
print(np.mean(mean_time))
plt.xlabel("scan time(s)")
plt.ylabel("time per round(s)")
plt.show()

