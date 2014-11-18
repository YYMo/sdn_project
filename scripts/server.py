from socket import *
from select import *
import sys
import Queue
import threading
import time

class SocketReceiver:
    def __init__(self, queue):
        print 'init server'
        self.queue = queue
        self.host = ''
        self.port = int(sys.argv[1])
        self.serverObj = socket(AF_INET, SOCK_STREAM)
        self.serverObj.bind((self.host, self.port))
        self.serverObj.listen(5)

    def loop(self):
        global run
        while True:
            infds,outfds,errfds = select([self.serverObj,],[],[],5)   
            if(run == 0):
                print 'close'
                #connection.close()
                self.serverObj.close()
                sys.exit()
                break
            if len(infds) != 0:   
                connection, address = self.serverObj.accept()
                infds_c,outfds_c,errfds_c = select([connection,],[],[],3)
                print 'Server Connected by: ', address

                if len(infds_c) != 0:   
                    buf = connection.recv(8196)   
                    if len(buf) != 0:   
                        print str(buf)
                        print address
                        self.queue.put(str(address[0]))
                        self.queue.put(str(address[1]))
                        self.queue.put(str(buf))
                        connection.send('Echo:' + buf)
                connection.close()

run = 1


def parse(msg):
    str = msg.split(' ')
    return str

def outputfile(fileName, Str, bNew):
    print ">> " + Str
    output = open(fileName, bNew)
    try:
        output.write(Str + '\n')
    finally:    
        output.close()


def main():
    startport = 12000
    con_dict = {}
    addr_dict = {}
    run = 1
    queue = Queue.Queue()
    sr = SocketReceiver(queue)
    sckt_thread = threading.Thread(target = sr.loop)
    sckt_thread.start()
    outputfile('command.txt', '#!/bin/bash', 'w+')
    outputfile('connect_info.txt', 'Contrller info:', 'w+')
    while True:
        while queue.qsize():
            try:
                add = queue.get(0)
                port = queue.get(0)
                msg = queue.get(0)
                command = parse(msg)


                if command[0] == 'nPackets': #nPackets 123
                    avg_10000x = str(int(float(command[2])*10000))
                    outputfile('avg_time', avg_10000x, 'w+')
                    con_dict[add] = (command[1], avg_10000x)
                    #print con_dict
                elif command[0] == 'newCon3': #newCon 12345
                    startport = 12001
                    cmd = './c_l2.sh ' + str(startport) + " " + str(startport) + '.log' + " &"
                    outputfile('command.txt', cmd, 'a')
                    
                    cmd = 'python send.py ' + add + ' ' + sys.argv[1] + ' ' + "\"set " + str(startport) + "\"" + " &"
                    outputfile('connect_info.txt', 'controller on local:' + str(startport) +' connected to '+ add , 'a')
                    outputfile('command.txt', cmd, 'a')

                    cmd = './stats_avg_flow_time.sh ' + add + ' ' + sys.argv[1] + ' ' + str(startport) + '.log' + " &"
                    outputfile('command.txt', cmd, 'a')


                elif command[0] == 'newCon': #newCon 12345
                    tmin = 100000
                    tindex = False
                    b = False

                    if startport == 12001:
                        cmd = 'python send.py ' + add + ' ' + sys.argv[1] + ' '  + "\"set " + str(12000) + "\"" + " &"
                        outputfile('connect_info.txt', 'Mininets switches on '+ add + ' lost connection to controller', 'a')
                        outputfile('connect_info.txt', 'Controller on port '+ str(12000) + ' is available', 'a')
                        outputfile('connect_info.txt', 'controller on local:' + str(12000) +' connected to '+ add , 'a')
                        outputfile('command.txt', cmd, 'a')
                        continue

                    cmd = './c_l2.sh ' + str(startport) + " " + str(startport) + '.log' + " &"
                    outputfile('command.txt', cmd, 'a')
                    outputfile('connect_info.txt', 'Mininets switches on '+ add + ' lost connection to controller', 'a')
                    outputfile('connect_info.txt', 'No controller running now ... ' + str(startport), 'a')
                    outputfile('connect_info.txt', 'Create a new controller on port' + str(startport), 'a')

                    addr_dict[add] = startport
                    #print con_dict
                    
                    cmd = 'python send.py ' + add + ' ' + sys.argv[1] + ' '  + "\"set " + str(startport) + "\"" + " &"
                    outputfile('command.txt', cmd, 'a')

                    outputfile('connect_info.txt', 'controller on local:' + str(startport) +' connected to '+ add , 'a')

                    cmd = './stats_avg_flow_time.sh ' + add + ' ' + sys.argv[1] + ' '  + str(startport) + '.log' + " &"
                    outputfile('command.txt', cmd, 'a')

                    startport += 1

                elif command[0] == 'localnPackets':
                    avg_10000x = str(int(float(command[3])*10000))
                    con_dict[command[1]] = (command[2], avg_10000x)
                
                elif command[0] == 'set':
                    cmd = './disconnect_all.sh '+ " &"
                    outputfile('command.txt', cmd, 'a') 
                    cmd = './reconnect_all.sh ' + add + " " + command[1] + " &"

                    outputfile('command.txt', cmd, 'a')       
            except:
                pass


if __name__ == '__main__':
    main()
