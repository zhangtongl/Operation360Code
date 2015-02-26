#!/usr/bin/env python 
# 这个例子也是东拼西凑 出来的。
import time           
def readCpuInfo():
           
    f = open('/proc/stat')
           
    lines = f.readlines();
           
    f.close()
           
           
           
    for line in lines:
           
        line = line.lstrip()
           
        counters = line.split()
           
        if len(counters) < 5:
           
            continue
           
        if counters[0].startswith('cpu'):
           
            break
           
    total = 0
           
    for i in xrange(1, len(counters)):
           
        total = total + long(counters[i])
           
    idle = long(counters[4])
           
    return {'total':total, 'idle':idle}
           
           
           
def calcCpuUsage(counters1, counters2):
           
    idle = counters2['idle'] - counters1['idle']
           
    total = counters2['total'] - counters1['total']
           
    return 100 - (idle*100/total)
           
           
           
if __name__ == '__main__':
           
    counters1 = readCpuInfo()
           
    time.sleep(0.1)
           
    counters2 = readCpuInfo()
     
	str  = calcCpuUsage(counters1, counters2):
	
	f=open('/out.txt','w')
	
	print >>f,str
	
	f.close()
    