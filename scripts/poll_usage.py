#!/usr/bin/python
import psutil
import time
import sys
import getopt
import time

def parse_args(argv):
        global userName,processName,path
        #filters = {}
        try:
                opts, args = getopt.getopt(argv,"hu:p:l:",["user=","process=","fullpath="])
        except getopt.GetoptError:
                print 'usage: ./poll_usage.py -u <username> -p <processname> -l <path>'
                sys.exit(2)
        for opt, arg in opts:
                if opt == '-h':
                         print 'usage: ./poll_usage.py -u <username> -p <processname> -l <path>'
                         sys.exit()
                elif opt in ("-u", "--user"):
                         userName = arg
                         print("userName="+userName)
                         #filters.update({'user',arg})
                elif opt in ("-p", "--process"):
                         processName = arg
                         print("processName="+processName)
                         #filters.update({'process',arg})
                elif opt in ("-l", "--fullpath"):
                         path = arg
                         print("path="+path)
                         #filters.update({'path',arg})
        #return filters

if __name__ == "__main__":
        '''
        sample usage: ./poll_usage.py -u mininet -p python2.7 -l \/home\/mininet\/pox
        '''
        userName = ''
        processName = ''
        path = ''
        parse_args(sys.argv[1:])
        refreshrate = 20
        while(True):
                for proc in psutil.process_iter():
                        try:
                                if ((len(userName)==0 or proc.username()==userName)):
                                #if ((len(userName)==0 or proc.username()==userName) and (len(processName)==0 or proc.name()==processName) and (len(path)==0 or proc.cwd()==path) ):
                                        pinfo = proc.as_dict(attrs=['name','cwd'])
                                        if ((len(processName)==0 or pinfo['name'].find(processName,0)>=0) and (len(path)==0 or (str(pinfo['cwd'])).find(path,0)>=0)):
                                                pinfo = proc.as_dict(attrs=['pid', 'name','username','cwd','cpu_times','cpu_percent','memory_info_ex','memory_percent','open_files','connections','status','is_running','children','parent','threads','rlimit','num_fds','io_counters'])
                                                print(pinfo)
                        except psutil.NoSuchProcess:
                                pass
                #else:
                #       print(pinfo)
                print('-----------------------------------------------------------------------------------------------------------------------------------------------')
                time.sleep(refreshrate)
