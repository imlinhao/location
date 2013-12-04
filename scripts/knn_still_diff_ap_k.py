#-*- coding: utf-8 -*-
#first using find_aps_in_1_6_11_channel_cover_begin_mid_end.py to find which aps we can use
import re
import math
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 

DATA_ROOT = "../datasets/fingerprint_db/liang_mi"
STILLTIME_FN = DATA_ROOT+"/2013_11_29_22_31_31/stilltime.txt"
DB_FN = DATA_ROOT+"/2013_11_29_22_31_31/wifi.txt"
ONLINE_STILLTIME_FN = DATA_ROOT+"/2013_11_29_22_6_17/stilltime.txt"
QUERY_FN = DATA_ROOT+"/2013_11_29_22_6_17/wifi.txt"

#DATA_ROOT = "../datasets/fingerprint_db/hao_nexus7"
#STILLTIME_FN = DATA_ROOT+"/2013_11_29_21_26_4_offline/stilltime.txt"
#DB_FN = DATA_ROOT+"/2013_11_29_21_26_4_offline/wifi.txt"
#ONLINE_STILLTIME_FN = DATA_ROOT+"/2013_11_29_21_26_4_online/stilltime.txt"
#QUERY_FN = DATA_ROOT+"/2013_11_29_21_26_4_online/wifi.txt"


stilltime_list = []
f_stilltime = open(STILLTIME_FN)
while True:
	line = f_stilltime.readline()
	if not line: break
	stilltime_list.append(int(line))
f_stilltime.close()

def search_locindex(time, timelist):
	#TODO:use binary search
	if time < timelist[0]: return -1
	if time > timelist[-1]: return -2
	for i in range(0,len(timelist)/2):
		if timelist[2*i]<time<timelist[2*i+1]:
			return i

def set_apset(line, apset):
	it1 = re.finditer(";2412,(.*?,.*?),",line)
	it6 = re.finditer(";2437,(.*?,.*?),",line)
	it11 = re.finditer(";2462,(.*?,.*?),",line)
	for it in it1:
		apset.add(it.group(1))
	for it in it6:
		apset.add(it.group(1))
	for it in it11:
		apset.add(it.group(1))

f_db = open(DB_FN)
lines = f_db.readlines()
apset_start = set()
apset_mid = set()
apset_end = set()
start_time_begin = stilltime_list[0]; start_time_end = stilltime_list[1]
mid_time_begin = stilltime_list[len(stilltime_list)/2]; mid_time_end = stilltime_list[len(stilltime_list)/2+1]
#end_time_begin = stilltime_list[-2]; end_time_end = stilltime_list[-1]
#sampling program may have some bug
end_time_begin = stilltime_list[-4]; end_time_end = stilltime_list[-3]
for line in lines:
	time_searched = re.search("^(\d*);",line)
	time = int(time_searched.group(1))
	if(start_time_begin<time and time<start_time_end):
		set_apset(line, apset_start)
	elif(mid_time_begin<time and time<mid_time_end):
		set_apset(line, apset_mid)
	elif(end_time_begin<time and time<end_time_end):
		set_apset(line, apset_end)

f_db.close()

#print(apset_start)
#print(apset_mid)
#print(apset_end)
apset = apset_start.intersection(apset_mid,apset_end)
print(apset)



ap_list_all = list(apset)
ap_list_1 = ap_list_all[0:1]
ap_list_2 = ap_list_all[0:2]
ap_list_3 = ap_list_all[0:3]
ap_list_4 = ap_list_all[0:4]
ap_list_5 = ap_list_all[0:5]
ap_list_6 = ap_list_all[0:6]
ap_list_7 = ap_list_all[0:7]
#loc_list = [1,2,3,4,5]
loc_list = range(0,51)
#ap_list = ['AirJ,74:25:8a:47:39:30', 'AirJ,74:25:8a:47:3b:50', 'AirJ,74:25:8a:56:80:70']
stilltime_list = []
f_stilltime = open(STILLTIME_FN)
while True:
	line = f_stilltime.readline()
	if not line: break
	stilltime_list.append(int(line))
f_stilltime.close()

def search_locindex(time, timelist):
	#TODO:use binary search
	if time < timelist[0]: return -1
	if time > timelist[-1]: return -2
	for i in range(0,len(timelist)/2):
		if timelist[2*i]<time<timelist[2*i+1]:
			return i

dump_loc_list = []
db_list_1 = []; db_list_2 = []; db_list_3 = [];
db_list_4 = []; db_list_5 = []; db_list_6 = [];
db_list_7 = []
f_db = open(DB_FN)
while True:
	line = f_db.readline()
	if not line : break
	time = int(re.search("^(\d*);",line).group(1))
	loc_index = search_locindex(time,stilltime_list)
	if(loc_index<0): continue
	dump_loc_list.append(loc_list[loc_index])
	list_for_loop = [(ap_list_1,db_list_1),(ap_list_2,db_list_2),(ap_list_3,db_list_3),(ap_list_4,db_list_4),(ap_list_5,db_list_5),(ap_list_6,db_list_6),(ap_list_7,db_list_7)]
	for ap_list,db_list in list_for_loop:
		db_entry = []
		for ap in ap_list:
			rssi_search = re.search(ap+".*?,(-\d+?);",line)
			if rssi_search:
				db_entry.append(int(rssi_search.group(1)))
			else:
				db_entry.append(-100)
		db_list.append(db_entry)
		#print(db_list)
f_db.close()
#print(dump_loc_list)

online_stilltime_list = []
f_online_stilltime = open(ONLINE_STILLTIME_FN)
while True:
	line = f_online_stilltime.readline()
	if not line: break
	online_stilltime_list.append(int(line))
f_online_stilltime.close()

def distance(query_entry, db_entry):
	sum = 0
	for i in range(0,len(query_entry)):
		sum += (query_entry[i]-db_entry[i])**2
	return math.sqrt(sum)	

locindex = 0
query_list_1 = [];query_list_2 = []
query_list_3 = [];query_list_4 = []
query_list_5 = [];query_list_6 = []
query_list_7 = [];
err_distance_list_1 = [];err_distance_list_2 = []
err_distance_list_3 = [];err_distance_list_4 = []
err_distance_list_5 = [];err_distance_list_6 = []
err_distance_list_7 = [];
f_query = open(QUERY_FN)
while True:
	line = f_query.readline()
	if not line: break
	time = int(re.search("^(\d*);",line).group(1))
	if(time>online_stilltime_list[2*locindex]):
		list_for_loop = [(ap_list_1,query_list_1,db_list_1,err_distance_list_1),(ap_list_2,query_list_2,db_list_2,err_distance_list_2),(ap_list_3,query_list_3,db_list_3,err_distance_list_3),(ap_list_4,query_list_4,db_list_4,err_distance_list_4),(ap_list_5,query_list_5,db_list_5,err_distance_list_5),(ap_list_6,query_list_6,db_list_6,err_distance_list_6),(ap_list_7,query_list_7,db_list_7,err_distance_list_7)]
		for ap_list, query_list, db_list, err_distance_list in list_for_loop:
			distance_list = []
			query_entry = []
			for ap in ap_list:
				rssi_search = re.search(ap+",(-\d+?);",line)
				if rssi_search:
					query_entry.append(int(rssi_search.group(1)))
				else:
					query_entry.append(-100)
			query_list.append(query_entry)
			for db_entry in db_list:
				distance_list.append(distance(db_entry,query_entry))
			cal_loc = dump_loc_list[distance_list.index(min(distance_list))]
			real_loc = loc_list[locindex]
			err_distance_list.append(abs(cal_loc-real_loc))
		locindex += 1
		if(len(loc_list)==locindex): break
f_query.close()

fig, ax = plt.subplots()
color_style = ["r*-","g+-","bo-","k*--","r+--","go--","b*-."]
i = 0
plt_list = []
for err_distance_list in [err_distance_list_1,err_distance_list_2,err_distance_list_3,err_distance_list_4,err_distance_list_5,err_distance_list_6,err_distance_list_7]:
	zero_count = err_distance_list.count(0)
	print(zero_count)
	zero_count_percentage = zero_count*1.0/len(err_distance_list)
	bins=np.linspace(0,12,13)+0.001 #plus 0.001 to include 1 meter in [0.001,1.001)
	hist,bin_edges = np.histogram(err_distance_list,bins=bins)
	print(hist)
	pdf = 1.0*hist/len(err_distance_list)
	cdf = np.cumsum(pdf)
	print(cdf)
	p = plt.plot(bins,np.append([zero_count_percentage],cdf),color_style[i])
	plt_list.append(p)
	i += 1
ax.set_xlim(0,12)
plt.xlabel(u'定位误差(米)',fontproperties=font)
plt.ylabel(u'CDF',fontproperties=font)
plt.legend((plt_list[0][0],plt_list[1][0],plt_list[2][0],plt_list[3][0],plt_list[4][0],plt_list[5][0],plt_list[6][0]),('k=1','k=2','k=3','k=4','k=5','k=6','k=7'))
plt.show();

