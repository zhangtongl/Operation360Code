#!/usr/bin/env python 
# python �ű���Ҳ�ǵ�һ�νӴ��������������Ҫ�󣬸��˸о�python�ű��﷨�Ƚϼ�࣬������copy��һ��
#���ö��̣߳�ͬʱ������¼�����Ҿ�������ssh �Ĺ�Կ��Ȼ������python �ű��ѹ�Կ������ȥ��Ȼ��д������ԱȽ��ɵĽű������Բ������ƶ�̨������ssh�ĵ�¼���˳����ܡ�
import paramiko 
import threading 
def ssh2(ip,username,passwd,cmd): 
try: 
ssh = paramiko.SSHClient() 
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
ssh.connect(ip,22,username,passwd,timeout=5) 
for m in cmd: 
stdin, stdout, stderr = ssh.exec_command(m) 
out = stdout.readlines() 
#��Ļ��� 
for o in out: 
print o, 
print '%s\tOK\n'%(ip) 
ssh.close() 
except : 
print '%s\tError\n'%(ip) 
if __name__=='__main__': 
cmd = ['cal','echo hello!']#��Ҫִ�е������б� 
username = "" #�û��� 
passwd = "" #���� 
threads = [] #���߳� 
print "Begin......" 
for i in range(1,254): 
ip = '192.168.1.'+str(i) 
a=threading.Thread(target=ssh2,args=(ip,username,passwd,cmd)) 
a.start() 