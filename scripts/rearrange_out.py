"""
1.rearrange the file format to
-----------------------CHx1-----------...------------CHxn------
  time_label;   ap1_label;ap2_label    ...  apn-1_label;apn_label
system timestamp; ap1_tsf;ap2tsf       ...    apn-1_tsf;apn_tsf

in order to see the channel dwell time more convniently
"""
#extract system timestamp is file format dependent
#now we use
#time = re.search('^(\d+?);',line).group(1)
import re

channel_aplist_dict = {'2412':[],'2417':[],'2422':[],'2427':[],'2432':[],'2437':[],'2442':[],'2447':[],'2452':[],'2457':[],'2462':[], '2467':[], '2472':[], '2484':[]}

#need to delete last line for the error partial record
INPUT_FILENAME = "../datasets/wardriving/"+"bao_coolpad/2013_10_27_13_45_50/wifi.txt"
OUTPUT_FILENAME = "../datasets/wardriving/"+"bao_coolpad/2013_10_27_13_45_50/wifi.out.txt"
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
channel_ap_tsf = {}
for channel in channel_aplist_dict.keys():
	channel_apcount_dict[channel] = len(channel_aplist_dict[channel])
	channel_ap_tsf[channel] = {}
	for ap in channel_aplist_dict[channel]:
		channel_ap_tsf[channel][ap]=[]

#print(channel_ap_tsf)
time_list = []
f.seek(0)
while True:
	line = f.readline()
	if not line : break
	time = re.search('^(\d+?);',line).group(1)
	time_list.append(time)
	for channel in channel_aplist_dict.keys():
		for ap in channel_aplist_dict[channel]:
			tsf_raw = re.search(ap+',(\d+?),',line)
			if tsf_raw:
				channel_ap_tsf[channel][ap].append(tsf_raw.group(1))
			else:
				channel_ap_tsf[channel][ap].append('-1')

print(channel_aplist_dict)
print(channel_apcount_dict)
f.close()


#channels = ['2412','2417','2422','2427','2432','2437','2442','2447','2452','2457','2462']
fout = open(OUTPUT_FILENAME,'w')
fout.write('time;')
channels = channel_ap_tsf.keys()
for channel in channels:
	for ap in channel_ap_tsf[channel]:
		fout.write(channel+','+ap+';')
fout.write('\n')
for i in range(0,len(time_list)):
	fout.write(time_list[i]+';')
	for channel in channels:
		for ap in channel_ap_tsf[channel]:
			fout.write(channel_ap_tsf[channel][ap][i]+';')
	fout.write('\n')

fout.close()
