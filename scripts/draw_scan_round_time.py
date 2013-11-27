import re
import matplotlib.pyplot as plt
import numpy as np

INPUT_FILENAME = "../datasets/wardriving/"+"bao_coolpad/2013_10_27_13_45_50/wifi.txt"
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

print(round_time_list)
first_time = (time_list[1]-time_list[0])/1000.0
last_time = (time_list[-1]-time_list[0])/1000.0
x = np.linspace(first_time,last_time,len(round_time_list),endpoint=True)
plt.plot(x,round_time_list)
plt.xlabel("scan time(s)")
plt.ylabel("time per round(s)")
plt.show()

