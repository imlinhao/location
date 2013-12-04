#-*- coding: utf-8 -*-
#first using find_aps_in_1_6_11_channel_cover_begin_mid_end.py to find which aps we can use
import re
import math
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 

#DATA_ROOT = "../datasets/fingerprint_db/hao_nexus7"
#STILLTIME_FN = DATA_ROOT+"/2013_11_29_21_26_4_offline/stilltime.txt"
#DB_FN = DATA_ROOT+"/2013_11_29_21_26_4_offline/wifi.txt"
#ONLINE_STILLTIME_FN = DATA_ROOT+"/2013_11_29_21_26_4_online/stilltime.txt"
#QUERY_FN = DATA_ROOT+"/2013_11_29_21_26_4_online/wifi.txt"

DATA_ROOT = "../datasets/fingerprint_db/liang_mi"
STILLTIME_FN = DATA_ROOT+"/2013_11_29_22_31_31/stilltime.txt"
DB_FN = DATA_ROOT+"/2013_11_29_22_31_31/wifi.txt"
ONLINE_STILLTIME_FN = DATA_ROOT+"/2013_11_29_22_6_17/stilltime.txt"
QUERY_FN = DATA_ROOT+"/2013_11_29_22_6_17/wifi.txt"

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
	it1 = re.finditer("2412,(.*?,.*?),",line)
	it6 = re.finditer("2437,(.*?,.*?),",line)
	it11 = re.finditer("2462,(.*?,.*?),",line)
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



def search_ap_rssi(ap_list, line, add_otherchannel):
	entry = {}
	for ap in ap_list:
		rssi_search = re.search(ap+",(-\d+?);",line)
		if rssi_search:
			entry[ap] = int(rssi_search.group(1))
		else:
			entry[ap] = -100
	if add_otherchannel:
		for freq in ['2417','2422','2427','2432','2442','2447','2452','2457','2467','2472','2484']:
			it = re.finditer(freq+",(.*?,.*?),.*?(-\d+?);",line)
			for i in it:
				entry[i.group(1)] = int(i.group(2))
	return entry

ap_list_all = list(apset)
ap_list_2 = ap_list_all[0:2]
ap_list_add_otherchannel = list(ap_list_2)
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

db_list_add_otherchannel = []
db_list_2 = []
f_db = open(DB_FN)
prev_loc_index = 0
db_entry_add_otherchannel_ap_rssilist = {}
db_entry_2_ap_rssilist = {}
while True:
	line = f_db.readline()
	if not line : break
	time = int(re.search("^(\d*);",line).group(1))
	loc_index = search_locindex(time,stilltime_list)
	if(loc_index<0): continue
	db_entry_2 = {}
	db_entry_add_otherchannel = {}
	if(loc_index==prev_loc_index):
		for ap in ap_list_2:
			rssi_search = re.search(ap+",(-\d+?);",line)
			if rssi_search:
				rssi = rssi_search.group(1)
				if (ap not in db_entry_2_ap_rssilist.keys()) : 
					db_entry_2_ap_rssilist[ap] = [int(rssi)]; db_entry_add_otherchannel_ap_rssilist[ap] = [int(rssi)]
				else: 
					db_entry_2_ap_rssilist[ap].append(int(rssi)); db_entry_add_otherchannel_ap_rssilist[ap].append(int(rssi))
		for freq in ['2417','2422','2427','2432','2442','2447','2452','2457','2467','2472','2484']:
			#it = re.finditer(";"+freq+",(.*?,.*?),.*?(-\d+?);",line) #it looks like the first simicolon have some problem
			it = re.finditer(freq+",(.*?,.*?),.*?(-\d+?);",line)
			for i in it:
				ap = i.group(1); rssi = i.group(2)
				#print(ap);print(rssi)
				if(ap not in db_entry_add_otherchannel_ap_rssilist.keys()): db_entry_add_otherchannel_ap_rssilist[ap] = [int(rssi)]
				else: db_entry_add_otherchannel_ap_rssilist[ap].append(int(rssi))
	else: 
		#print(line)
		print(db_entry_2_ap_rssilist);print(db_entry_add_otherchannel_ap_rssilist)
		prev_loc_index=loc_index
		for ap in db_entry_2_ap_rssilist.keys():
			db_entry_2[ap] = [np.mean(db_entry_2_ap_rssilist[ap]),np.std(db_entry_2_ap_rssilist[ap])]
		for ap in db_entry_add_otherchannel_ap_rssilist.keys():
			db_entry_add_otherchannel[ap] = [np.mean(db_entry_add_otherchannel_ap_rssilist[ap]),np.std(db_entry_add_otherchannel_ap_rssilist[ap])]
		db_list_2.append(db_entry_2)
		db_list_add_otherchannel.append(db_entry_add_otherchannel)
		db_entry_2_ap_rssilist = {}
		db_entry_add_otherchannel_ap_rssilist = {}
		db_entry_2 = {}
		db_entry_add_otherchannel = {}
#the db_entry for last location, TODO:sames not optimal for program
db_entry_2 = {}
db_entry_add_otherchannel = {}
for ap in db_entry_2_ap_rssilist.keys():
	db_entry_2[ap] = [np.mean(db_entry_2_ap_rssilist[ap]),np.std(db_entry_2_ap_rssilist[ap])]
for ap in db_entry_add_otherchannel_ap_rssilist.keys():
	db_entry_add_otherchannel[ap] = [np.mean(db_entry_add_otherchannel_ap_rssilist[ap]),np.std(db_entry_add_otherchannel_ap_rssilist[ap])]
db_list_2.append(db_entry_2)
db_list_add_otherchannel.append(db_entry_add_otherchannel)
db_entry_2_ap_rssilist = {}
db_entry_add_otherchannel_ap_rssilist = {}
f_db.close()
#print(dump_loc_list)
print(db_list_2)
print(db_list_add_otherchannel)

online_stilltime_list = []
f_online_stilltime = open(ONLINE_STILLTIME_FN)
while True:
	line = f_online_stilltime.readline()
	if not line: break
	online_stilltime_list.append(int(line))
f_online_stilltime.close()

def distance(query_entry, db_entry):
	query_entry_aps = query_entry.keys()
	db_entry_aps = db_entry.keys()
	ap_set = set(query_entry_aps+db_entry_aps)
	sum = 0
	for ap in ap_set:
		query_rssi = -100; db_rssi = -100
		if ap in query_entry_aps: query_rssi = query_entry[ap];#print(query_entry[ap])
		if ap in db_entry_aps: db_rssi = db_entry[ap][0];#print(db_entry[ap])
		sum += (query_rssi-db_rssi)**2
	return math.sqrt(sum)	

locindex = 0
query_list_2 = []
query_list_add_otherchannel = []
err_distance_list_2 = []
err_distance_list_add_otherchannel = []
f_query = open(QUERY_FN)

while True:
	line = f_query.readline()
	if not line: break
	time = int(re.search("^(\d*);",line).group(1))
	if(time>online_stilltime_list[2*locindex]):
		list_for_loop = [(ap_list_2,query_list_2,False,db_list_2,err_distance_list_2),(ap_list_add_otherchannel,query_list_add_otherchannel,True,db_list_add_otherchannel,err_distance_list_add_otherchannel)]
		for ap_list, query_list, add_otherchannel, db_list, err_distance_list in list_for_loop:
			distance_list = []
			query_entry = search_ap_rssi(ap_list, line, add_otherchannel)
			query_list.append(query_entry)
			for db_entry in db_list:
				distance_list.append(distance(query_entry,db_entry))
			cal_loc = loc_list[distance_list.index(min(distance_list))]
			real_loc = loc_list[locindex]
			err_distance_list.append(abs(cal_loc-real_loc))
		locindex += 1
		if(len(loc_list)==locindex): break
f_query.close()
print(query_list_2)
print(query_list_add_otherchannel)

fig, ax = plt.subplots()
color_style = ["r*-","g+-","bo-","k*--","r+--","go--","b*-."]
i = 0
plt_list = []
for err_distance_list in [err_distance_list_2,err_distance_list_add_otherchannel]:
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
plt.legend((plt_list[0][0],plt_list[1][0]),('k=2','k=2 add other channel'))
plt.show();

