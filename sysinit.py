import argparse
import paramiko
"""
sysversion controlip 
"""

class Client(object):
    '''connect  client , send file  default mode, exec  cmd'''
    def __init__(self,host='',password=None,port=4344,username='root'):
        print locals()
        self.trans=paramiko.Transport((host,port))
        self.trans.connect(username=username,password=password)
        self.ssh=paramiko.SSHClient()
        self.ssh._transport = self.trans
        self.sftp=paramiko.SFTPClient.from_transport(self.trans)
    
    def file(self,local,remote,ip,sysver,hostname):
        import jinja2
        with open('sys_init/moudle') as f:
            data=jinja2.Template(f.read())
        with open(local,'w') as l:
            l.write(data.render(controlip=ip,sysversion=sysver,hostname=hostname))
        self.sftp.put(localpath=local,remotepath=remote)

    def cmd(self,cmdline):
        stdin, stdout, stderr = self.ssh.exec_command(cmdline)

    def close(self):
        self.trans.close()

class File(object):
    def  __init__(self,filename):
        self.data=[]
        with open(filename) as conf:
             for line in conf.readlines():
                 self.data.append(line.split())
    


def main(filename):
    #conf file , script
    data=File(filename).data
    for client in data:
        '''hostname,ip,mima,sysversion,networkstyle'''
        print client
        ip = 'xxxxx' if client[4]=='public' else 'xxxxx'
        a=Client(client[1],client[2])       
        a.file('sys_init/temp.sh','/tmp/temp.sh',ip,client[3],client[0])
        a.cmd('bash /tmp/temp.sh &')
        a.close()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H','--hostname',help='''a host name or a hostlist
                 example1:  host1
                 example2:  host1,host2,host3 ''')
    parser.add_argument('-IP','--host',help='''system ip or a iplist''')			 
    parser.add_argument('-P','--password',help='''the root password for system
                 example1:  password1
                 example2:  password2,password3''')
    parser.add_argument('-V','--version',help='system version centos6 or centos7,default 6',default='6')
    parser.add_argument('-N','--network',help='network style,its can be the default yum use private network or public network',default='private')
    parser.add_argument('-F','--file',help='''all args  in this file
    file example:
    host1 1.1.1.1 sec1  6  private''')
    args = parser.parse_args()
    if args.file:
        main(args.file)
    else:
        a=Client(host=args.host,password=args.password)
        a.file('/root/haha.sh','/tmp/haha.sh')
        a.cmd('/tmp/haha.sh')
        a.close()
