import re
import math

DATA_ROOT = "../datasets/fingerprint_db/liang_mi"
STILLTIME_FN = DATA_ROOT+"/2013_11_29_22_31_31/stilltime.txt"
DB_FN = DATA_ROOT+"/2013_11_29_22_31_31/wifi.txt"

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


