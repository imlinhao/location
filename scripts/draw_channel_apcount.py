import re
import numpy as np
import matplotlib.pyplot as plt

channel_aplist_dict = {'2412':[],'2417':[],'2422':[],'2427':[],'2432':[],'2437':[],'2442':[],'2447':[],'2452':[],'2457':[],'2462':[], '2467':[], '2472':[], '2484':[]}

#need to delete last line for the error partial record
INPUT_FILENAME = "../datasets/wardriving/"+"bao_coolpad/wifi_2teach.txt"
#INPUT_FILENAME="../datasets/fingerprint_db/liang_mi/2013_10_26_20_22_9/wifi.txt"
f = open(INPUT_FILENAME)
while True:
	line = f.readline()
	if not line : break
	results = line.rstrip(';\n').split(';')
	for i in range(1,len(results)):
		fields = results[i].split(',')
		if (fields[1]+','+fields[2] not in channel_aplist_dict[fields[0]]):
			channel_aplist_dict[fields[0]].append(fields[1]+','+fields[2])

channel_apcount_dict = {}
for channel in channel_aplist_dict.keys():
	channel_apcount_dict[channel] = len(channel_aplist_dict[channel])

print(channel_aplist_dict)
print(channel_apcount_dict)

f.close()


channel_freq_dict = {'1':['2412'],'6':['2437'],'11':['2462'],'other':['2417','2422','2427','2432','2442','2447','2452','2457','2467','2472','2484']}
channels = ['1','6','11','other']
counts = []
for channel in channels:
	sum = 0
	for freq in channel_freq_dict[channel]:
		sum += channel_apcount_dict[freq]
	counts.append(sum)

#index = range(1,len(counts)+1)
index = np.arange(1,len(counts)+1,1)
print(index-0.25)
print(channels)
print(counts)
fig, ax = plt.subplots()
plt.bar(index-0.25,counts,0.5)
plt.xlabel('Channel')
plt.ylabel('AP Counts')
plt.xticks(index)
ax.set_xticklabels(channels)
for i in range(0,len(counts)):
	ax.annotate(counts[i],(index[i],counts[i]+1),va="bottom",ha="center")
ax.set_ylim(0,max(counts)+10)
plt.show()
	
