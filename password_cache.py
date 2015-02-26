#!/usr/bin/env python 
# python 脚本我也是第一次接触，按照面试题的要求，个人感觉python脚本语法比较简洁，在网上copy了一个
#利用多线程，同时发出登录请求，我觉得设置ssh 的公钥，然后利用python 脚本把公钥共享出去，然后写个耦合性比较松的脚本，可以并发控制多台机器的ssh的登录且退出功能。
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
#屏幕输出 
for o in out: 
print o, 
print '%s\tOK\n'%(ip) 
ssh.close() 
except : 
print '%s\tError\n'%(ip) 
if __name__=='__main__': 
cmd = ['cal','echo hello!']#你要执行的命令列表 
username = "" #用户名 
passwd = "" #密码 
threads = [] #多线程 
print "Begin......" 
for i in range(1,254): 
ip = '192.168.1.'+str(i) 
a=threading.Thread(target=ssh2,args=(ip,username,passwd,cmd)) 
a.start() 