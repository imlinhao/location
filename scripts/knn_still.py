import re
import matplotlib.pyplot as plt
import numpy as np
import math
DATA_ROOT = "../datasets/fingerprint_db/liang_mi"
STILLTIME_FN = DATA_ROOT+"/2013_11_29_22_31_31/stilltime.txt"
DB_FN = DATA_ROOT+"/2013_11_29_22_31_31/wifi.txt"
ONLINE_STILLTIME_FN = DATA_ROOT+"/2013_11_29_22_6_17/stilltime.txt"
QUERY_FN = DATA_ROOT+"/2013_11_29_22_6_17/wifi.txt"

#loc_list = [1,2,3,4,5]
loc_list = range(0,51)
#ap_list = ['AirJ,74:25:8a:47:39:30', 'AirJ,74:25:8a:47:3b:50', 'AirJ,74:25:8a:56:80:70']
ap_list = ['AirJ,74:25:8a:47:39:30', 'AirJ,74:25:8a:47:3b:50', 'AirJ,74:25:8a:56:80:70']
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
db_list = []
f_db = open(DB_FN)
while True:
	line = f_db.readline()
	if not line : break
	time = int(re.search("^(\d*);",line).group(1))
	loc_index = search_locindex(time,stilltime_list)
	if(loc_index<0): continue
	dump_loc_list.append(loc_list[loc_index])
	db_entry = []
	for ap in ap_list:
		rssi_search = re.search(ap+".*?,(-\d+?);",line)
		if rssi_search:
			db_entry.append(int(rssi_search.group(1)))
		else:
			db_entry.append(-100)
	db_list.append(db_entry)
f_db.close()

#print(len(dump_loc_list))
#print(len(dump_loc_list))
print(dump_loc_list)
print(db_list)

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
query_list = []
err_distance_list = []
f_query = open(QUERY_FN)
while True:
	distance_list = []
	line = f_query.readline()
	if not line: break
	time = int(re.search("^(\d*);",line).group(1))
	if(time>online_stilltime_list[2*locindex]):
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
		#print("cal loc: %d" % cal_loc)
		#print("real loc:%d" % real_loc)
		#print("distance:%d" % abs(cal_loc-real_loc))
		#print("rssi distance:%d" % min(distance_list))

		locindex += 1
		if(len(loc_list)==locindex): break
f_query.close()
zero_count = err_distance_list.count(0)
print(zero_count)
zero_count_percentage = zero_count*1.0/len(err_distance_list)
bins=np.linspace(0,10,11)
hist,bin_edges = np.histogram(err_distance_list,bins=bins)
print(hist)
pdf = 1.0*hist/len(err_distance_list)
cdf = np.cumsum(pdf)
print(cdf)
plt.plot(bins,np.append([zero_count_percentage],cdf),'r*-')
plt.show();

