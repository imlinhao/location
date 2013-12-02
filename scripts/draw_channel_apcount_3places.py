#-*- coding: utf-8 -*-
import matplotlib
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import re
import numpy as np

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 
def get_apcount_dict(filename):
	channel_aplist_dict = {'2412':[],'2417':[],'2422':[],'2427':[],'2432':[],'2437':[],'2442':[],'2447':[],'2452':[],'2457':[],'2462':[], '2467':[], '2472':[], '2484':[]}
	#need to delete last line for the error partial record
	f = open(filename)
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

	#print(channel_aplist_dict)
	print(channel_apcount_dict)
	f.close()
	return channel_apcount_dict

channel_apcount_dict_2teach = get_apcount_dict("../datasets/wardriving/bao_coolpad/wifi_2teach.txt")
channel_apcount_dict_iot = get_apcount_dict("../datasets/wardriving/bao_coolpad/wifi_iot.txt")
channel_apcount_dict_ju_to_2rest = get_apcount_dict("../datasets/wardriving/bao_coolpad/wifi_ju_to_2rest.txt")
channel_freq_dict = {'1':['2412'],'6':['2437'],'11':['2462'],'other':['2417','2422','2427','2432','2442','2447','2452','2457','2467','2472','2484']}
channels = ['1','6','11','other']
counts_all = []
counts_2teach = []
counts_iot = []
counts_ju_to_2rest = []
for channel in channels:
	sum_all = 0; sum_2teach = 0; sum_iot = 0; sum_ju_to_2rest = 0;
	for freq in channel_freq_dict[channel]:
		sum_2teach += channel_apcount_dict_2teach[freq]
		sum_iot += channel_apcount_dict_iot[freq]
		sum_ju_to_2rest += channel_apcount_dict_ju_to_2rest[freq]
	sum_all += sum_2teach + sum_iot + sum_ju_to_2rest 
	counts_all.append(sum_all)
	counts_2teach.append(sum_2teach)
	counts_iot.append(sum_iot)
	counts_ju_to_2rest.append(sum_ju_to_2rest)

index = np.arange(1,len(counts_all)+1,1)
print(index-0.25)
print(channels)
print(counts_all)
counts_all = np.array(counts_all)
counts_2teach = np.array(counts_2teach)
counts_iot = np.array(counts_iot)
counts_ju_to_2rest = np.array(counts_ju_to_2rest)

fig, ax = plt.subplots()
p1 = plt.bar(index-0.25,counts_2teach,0.5,color='r')
p2 = plt.bar(index-0.25,counts_iot,0.5,bottom=counts_2teach,color='b')
p3 = plt.bar(index-0.25,counts_ju_to_2rest,0.5,bottom=counts_2teach+counts_iot,color='g')
plt.legend( (p1[0], p2[0], p3[0]), (u'教学楼', u'学院大楼', u'宿舍楼至食堂') ,prop=font)
plt.xlabel(u'信道',fontproperties=font)
plt.ylabel(u'AP数目',fontproperties=font)
plt.xticks(index)
ax.set_xticklabels(channels)
for i in range(0,len(counts_all)):
	ax.annotate(counts_all[i],(index[i],counts_all[i]+1),va="bottom",ha="center")
ax.set_ylim(0,max(counts_all)+10)
plt.show()
	
