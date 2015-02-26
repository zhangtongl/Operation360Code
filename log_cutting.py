#!/usr/bin/env python 

 
def split(filename, size):

    fp = open(filename, 'rb')
    i = 0
    n = 0
    temp = open(filename+'.part'+str(i),'wb')
    buf = fp.read(1024)
    while(True):
        temp.write(buf)
        buf = fp.read(1024)
        if(buf == ''):
            print filename+'.part'+str(i)+';'
            temp.close()
            fp.close()
            return
        n += 1
        if(n == size):
            n = 0
            print filename+'.part'+str(i)+';'
            i += 1
            temp.close()
            temp = open(filename+'.part'+str(i),'wb')
 

if __name__ == '__main__':

    name = raw_input('input filename:')

    split(name, 307200)        #分割后每个文件300M


