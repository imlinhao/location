import re
import matplotlib.pyplot as plt
import numpy as np
import math

def get_err_distance_list(query_list, db):
	err_distance_list = []
	real_loc_list = range(0,len(query_list))
	loc_list = range(0,len(db))
	i = 0
	for real_loc in real_loc_list:
		distance_list = []
		query_entry = query_list[i]
		i += 1
		for db_entry in db:
			distance_list.append(distance(query_entry,db_entry))
		cal_loc = loc_list[distance_list.index(min(distance_list))]
		err_distance_list.append(abs(cal_loc-real_loc))
	return err_distance_list
	

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



def search_locindex(time, timelist):
	#TODO:use binary search
	if time < timelist[0]: return -1
	if time > timelist[-1]: return -2
	for i in range(0,len(timelist)/2):
		if timelist[2*i]<time<timelist[2*i+1]:
			return i

def get_stilltime_list(filename):
	stilltime_list = []
	stilltime_file = open(filename)
	while True:
		line = stilltime_file.readline()
		if not line: break
		stilltime_list.append(int(line))
	stilltime_file.close()
	return stilltime_list

def get_movetime_list(filename):
	movetime_list = []
	movetime_file = open(filename)
	while True:
		line = movetime_file.readline()
		if not line: break
		movetime_list.append(int(line))
	movetime_file.close()
	return movetime_list

def construct_3channel_db(filename, stilltime_list):
	db = []
	db_file = open(filename)
	prev_loc_index = 0
	ap_rssilist_dict = {}
	while True:
		line = db_file.readline()
		if not line : break
		time = 1000*float(re.search("^(\d*.\d*);",line).group(1))
		loc_index = search_locindex(time,stilltime_list)
		if(loc_index<0): continue
		if(loc_index==prev_loc_index):
			for freq in ["2412","2437","2462"]:
				ap_rssi_all = re.findall(freq+',(..:..:..:..:..:..),.*?(-\d*);',line)
				for ap,rssi in ap_rssi_all:
					if(ap not in ap_rssilist_dict.keys()): ap_rssilist_dict[ap] = [int(rssi)]
					else: ap_rssilist_dict[ap].append(int(rssi))
		else: 
			prev_loc_index=loc_index
			db_entry = {}
			for ap in ap_rssilist_dict.keys():
				db_entry[ap] = [np.mean(ap_rssilist_dict[ap]),np.std(ap_rssilist_dict[ap])]
			db.append(db_entry)
			ap_rssilist_dict = {}
	#the db_entry for last location, TODO:sames not optimal for program
	db_entry = {}
	for ap in ap_rssilist_dict.keys():
		db_entry[ap] = [np.mean(ap_rssilist_dict[ap]),np.std(ap_rssilist_dict[ap])]
	db.append(db_entry)
	ap_rssilist_dict = {}
	db_file.close()
	return db

def construct_allchannel_db(filename, stilltime_list):
	db = []
	db_file = open(filename)
	prev_loc_index = 0
	ap_rssilist_dict = {}
	while True:
		line = db_file.readline()
		if not line : break
		time = int(re.search("^(\d*);",line).group(1))
		loc_index = search_locindex(time,stilltime_list)
		if(loc_index<0): continue
		if(loc_index==prev_loc_index):
			ap_rssi_all = re.findall(',(.*?,..:..:..:..:..:..),.*?(-\d*);',line)
			for ap,rssi in ap_rssi_all:
				if(ap not in ap_rssilist_dict.keys()): ap_rssilist_dict[ap] = [int(rssi)]
				else: ap_rssilist_dict[ap].append(int(rssi))
		else: 
			prev_loc_index=loc_index
			db_entry = {}
			for ap in ap_rssilist_dict.keys():
				db_entry[ap] = [np.mean(ap_rssilist_dict[ap]),np.std(ap_rssilist_dict[ap])]
			db.append(db_entry)
			ap_rssilist_dict = {}
	#the db_entry for last location, TODO:sames not optimal for program
	db_entry = {}
	for ap in ap_rssilist_dict.keys():
		db_entry[ap] = [np.mean(ap_rssilist_dict[ap]),np.std(ap_rssilist_dict[ap])]
	db.append(db_entry)
	ap_rssilist_dict = {}
	db_file.close()
	return db

def get_3channel_move_query_list(filename, movetime_list, loc_list):
	locindex = 0
	query_list = []
	query_file = open(filename)
	while True:
		distance_list = []
		line = query_file.readline()
		if not line: break
		time = 1000*float(re.search("^(\d*.\d*);",line).group(1))
		if(time>movetime_list[locindex]):
			query_entry = {}
			for freq in ["2412","2437","2462"]:
				ap_rssi_all = re.findall(freq+',(..:..:..:..:..:..),.*?(-\d*);',line)
				for ap,rssi in ap_rssi_all:
					query_entry[ap] = int(rssi)
			query_list.append(query_entry)
			locindex += 1
			if(len(loc_list)==locindex): break
	return query_list

def get_allchannel_move_query_list(filename, movetime_list, loc_list):
	locindex = 0
	query_list = []
	query_file = open(filename)
	while True:
		distance_list = []
		line = query_file.readline()
		if not line: break
		time = int(re.search("^(\d*);",line).group(1))
		if(time>movetime_list[locindex]):
			query_entry = {}
			ap_rssi_all = re.findall(',(.*?,..:..:..:..:..:..),.*?(-\d*);',line)
			for ap,rssi in ap_rssi_all:
				query_entry[ap] = int(rssi)
			query_list.append(query_entry)
			locindex += 1
			if(len(loc_list)==locindex): break
	return query_list

def get_3channel_still_query_list(filename, stilltime_list, loc_list):
	db = []
	locindex = 0
	query_list = []
	query_file = open(filename)
	while True:
		line = query_file.readline()
		if not line: break
		time = 1000*float(re.search("^(\d*\.\d*);",line).group(1))
		if(time>stilltime_list[2*locindex]):
			query_entry = {}
			for freq in ["2412","2437","2462"]:
				ap_rssi_all = re.findall(freq+',(..:..:..:..:..:..),.*?(-\d*);',line)
				for ap,rssi in ap_rssi_all:
					query_entry[ap] = int(rssi)
			query_list.append(query_entry)
			locindex += 1
			if(len(loc_list)==locindex): break
	query_file.close()
	return query_list

def get_allchannel_still_query_list(filename, stilltime_list, loc_list):
	db = []
	locindex = 0
	query_list = []
	query_file = open(filename)
	while True:
		line = query_file.readline()
		if not line: break
		time = int(re.search("^(\d*);",line).group(1))
		if(time>stilltime_list[2*locindex]):
			query_entry = {}
			ap_rssi_all = re.findall(',(.*?,..:..:..:..:..:..),.*?(-\d*);',line)
			for ap,rssi in ap_rssi_all:
				query_entry[ap] = int(rssi)
			query_list.append(query_entry)
			locindex += 1
			if(len(loc_list)==locindex): break
	query_file.close()
	return query_list

def plt_cdf(err_distance_list, color_style, label):
	zero_count = err_distance_list.count(0)
	print(zero_count)
	zero_count_percentage = zero_count*1.0/len(err_distance_list)
	#bins=np.linspace(0,12,13)+0.001 #plus 0.001 to include 1 meter in [0.001,1.001)
	bins=np.linspace(0,12,20) #plus 0.001 to include 1 meter in [0.001,1.001)
	hist,bin_edges = np.histogram(err_distance_list,bins=bins)
	print(hist)
	pdf = 1.0*hist/len(err_distance_list)
	cdf = np.cumsum(pdf)
	print(cdf)
	p = plt.plot(bins,np.append([zero_count_percentage],cdf),color_style,label=label)
	return p

if __name__ == '__main__':
	DATA_ROOT = "../datasets/fingerprint_db/liang_mi"
	OFFLINE_STILLTIME_FN = DATA_ROOT+"/2013_12_4_21_42_49/stilltime.txt" 
	OFFLINE_DB_FN = DATA_ROOT+"/2013_12_4_21_42_49/wifi.txt"

	ALLCHANNEL_ONLINE_STILLTIME_FN = DATA_ROOT+"/2013_12_4_21_53_6/stilltime.txt"
	ALLCHANNEL_ONLINE_STILL_QUERY_FN = DATA_ROOT+"/2013_12_4_21_53_6/wifi.txt"
	ALLCHANNEL_ONLINE_MOVETIME_FN = DATA_ROOT+"/2013_12_4_21_57_17/movetime.txt"
	ALLCHANNEL_ONLINE_MOVE_QUERY_FN = DATA_ROOT+"/2013_12_4_21_57_17/wifi.txt"

	THREECHANNEL_ONLINE_STILLTIME_FN = DATA_ROOT+"/2013_12_4_21_1_46/stilltime.txt"
	THREECHANNEL_ONLINE_STILL_QUERY_FN = DATA_ROOT+"/2013_12_4_21_1_46/getscanJNI.txt"
	THREECHANNEL_ONLINE_MOVETIME_FN = DATA_ROOT+"/2013_12_4_21_37_52/movetime.txt"
	THREECHANNEL_ONLINE_MOVE_QUERY_FN = DATA_ROOT+"/2013_12_4_21_37_52/getscanJNI.txt"



	#DATA_ROOT = "../datasets/fingerprint_db/zhang_mi"
	#OFFLINE_STILLTIME_FN = DATA_ROOT+"/2013_12_4_21_42_15/stilltime.txt" 
	#OFFLINE_DB_FN = DATA_ROOT+"/2013_12_4_21_42_15/wifi.txt"

	#ALLCHANNEL_ONLINE_STILLTIME_FN = DATA_ROOT+"/2013_12_4_21_52_50/stilltime.txt"
	#ALLCHANNEL_ONLINE_STILL_QUERY_FN = DATA_ROOT+"/2013_12_4_21_52_50/wifi.txt"
	#ALLCHANNEL_ONLINE_MOVETIME_FN = DATA_ROOT+"/2013_12_4_21_57_15/movetime.txt"
	#ALLCHANNEL_ONLINE_MOVE_QUERY_FN = DATA_ROOT+"/2013_12_4_21_57_15/wifi.txt"

	#THREECHANNEL_ONLINE_STILLTIME_FN = DATA_ROOT+"/2013_12_4_21_19_38/stilltime.txt"
	#THREECHANNEL_ONLINE_STILL_QUERY_FN = DATA_ROOT+"/2013_12_4_21_19_38/getscanJNI.txt"
	#THREECHANNEL_ONLINE_MOVETIME_FN = DATA_ROOT+"/2013_12_4_21_37_53/movetime.txt"
	#THREECHANNEL_ONLINE_MOVE_QUERY_FN = DATA_ROOT+"/2013_12_4_21_37_53/getscanJNI.txt"
	loc_list = range(0,51)

	fig, ax = plt.subplots()
	color_style = ["r*-","g+-","bo-","k*--","r+--","go--","b*-."]

	offline_stilltime_list = get_stilltime_list(OFFLINE_STILLTIME_FN)
	db = construct_allchannel_db(OFFLINE_DB_FN, offline_stilltime_list)
	online_stilltime_list = get_stilltime_list(ALLCHANNEL_ONLINE_STILLTIME_FN)
	query_list = get_allchannel_still_query_list(ALLCHANNEL_ONLINE_STILL_QUERY_FN, online_stilltime_list, loc_list)
	allchannel_still_err_distance_list = get_err_distance_list(query_list, db)
	plt_cdf(allchannel_still_err_distance_list, color_style[0],label="all channel still")

	offline_stilltime_list = get_stilltime_list(OFFLINE_STILLTIME_FN)
	db = construct_allchannel_db(OFFLINE_DB_FN, offline_stilltime_list)
	online_movetime_list = get_movetime_list(ALLCHANNEL_ONLINE_MOVETIME_FN)
	query_list = get_allchannel_move_query_list(ALLCHANNEL_ONLINE_MOVE_QUERY_FN, online_movetime_list, loc_list)
	allchannel_move_err_distance_list = get_err_distance_list(query_list, db)
	plt_cdf(allchannel_move_err_distance_list, color_style[1],label="all channel move")

	offline_stilltime_list = get_stilltime_list(OFFLINE_STILLTIME_FN)
	threechannel_db = construct_3channel_db(OFFLINE_DB_FN, offline_stilltime_list)
	threechannel_online_stilltime_list = get_stilltime_list(THREECHANNEL_ONLINE_STILLTIME_FN)
	threechannel_query_list = get_3channel_still_query_list(THREECHANNEL_ONLINE_STILL_QUERY_FN, threechannel_online_stilltime_list, loc_list)
	threechannel_err_distance_list = get_err_distance_list(threechannel_query_list, threechannel_db)
	plt_cdf(threechannel_err_distance_list, color_style[2], label="three channel still")

	offline_stilltime_list = get_stilltime_list(OFFLINE_STILLTIME_FN)
	threechannel_db = construct_3channel_db(OFFLINE_DB_FN, offline_stilltime_list)
	threechannel_online_movetime_list = get_movetime_list(THREECHANNEL_ONLINE_MOVETIME_FN)
	threechannel_query_list = get_3channel_move_query_list(THREECHANNEL_ONLINE_MOVE_QUERY_FN, threechannel_online_movetime_list, loc_list)
	threechannel_err_distance_list = get_err_distance_list(threechannel_query_list, threechannel_db)
	plt_cdf(threechannel_err_distance_list, color_style[3], label="three channel move")

	plt.legend()
	ax.set_xlim(0,12)
	plt.show()


