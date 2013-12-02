#-*- coding: utf-8 -*-
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 
fig, ax = plt.subplots()
loc = np.arange(1,14)
colors = cm.jet(range(0,255,20))
#colors = ['r','b','g','y','r','b','g','y','r','b','g','y','r']
for i in range(1,14):
	plt.bar(loc-0.25,[1]*13,0.5,color=colors,bottom=[i-1]*13)
	plt.bar(14-0.25,1,0.5,color=colors[i-1],bottom=i-1)
#p1 = plt.bar(loc,counts_2teach,0.5,color='r')
#p2 = plt.bar(index-0.25,counts_iot,0.5,bottom=counts_2teach,color='b')
#p3 = plt.bar(index-0.25,counts_ju_to_2rest,0.5,bottom=counts_2teach+counts_iot,color='g')
#plt.legend( (p1[0], p2[0], p3[0]), (u'教学楼', u'学院大楼', u'宿舍楼至食堂') ,prop=font)
plt.xlabel(u'目标位置',fontproperties=font)
plt.ylabel(u'信道',fontproperties=font)
plt.xticks(np.arange(1,15))
loc = range(1,14)
loc.append('x')
ax.set_xticklabels(loc)
plt.yticks(np.arange(1,14)-0.5)
ax.set_yticklabels(np.arange(1,14))
#for i in range(0,len(counts_all)):
#	ax.annotate(counts_all[i],(index[i],counts_all[i]+1),va="bottom",ha="center")
ax.set_ylim(0,13.5)
ax.set_xlim(0,15)
plt.show()
	
