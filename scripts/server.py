from socket import *
from select import *
import sys
import Queue
import threading
import time
import os

class SocketReceiver:
    def __init__(self, queue):
        self.queue = queue
        self.host = ''
        self.port = 50006
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

run = 0
syscmd = 0


def parse(msg):
    str = msg.split(' ')
    return str

def execc():
    global syscmd
    print 'exec' + syscmd
    os.system(syscmd)


def main():
    global run
    global syscmd
    startport = 12000
    con_dict = {}
    run = 1
    queue = Queue.Queue()
    sr = SocketReceiver(queue)
    sckt_thread = threading.Thread(target = sr.loop)
    sckt_thread.start()
    while True:
        time.sleep(3)
        syscmd = 'echo ' + str(con_dict)+ ' > con_dict'
        thread3 = threading.Thread(target = execc)
        thread3.start()
        while queue.qsize():
            try:
                add = queue.get(0)
                port = queue.get(0)
                msg = queue.get(0)
                command = parse(msg)
                print command[0]
                print command[0] == 'newCon'

                if command[0] == 'nPackets': #nPackets 123
                    avg_10000x = str(int(float(command[2])*10000))
                    con_dict[add] = (command[1], avg_10000x)
                    print 'a match report'
                    syscmd = 'echo ' + command[1] + ' > packets_per_min'
                    thread4 = threading.Thread(target = execc)
                    thread4.start()
                    
                    syscmd = 'echo ' + avg_10000x + ' > avg_time10000X'
                    thread5 = threading.Thread(target = execc)
                    thread5.start()
                elif command[0] == 'newCon': #newCon 12345
                    print 'a match newCon'
                    syscmd = './c_l2.sh ' + add + " " + str(startport) + " " + str(startport) + '.log'
                    startpot += 1
                    thread1 = threading.Thread(target = execc)
                    thread1.start()
                    time.sleep(3)
                    syscmd = './stats_avg_flow_time.sh ' + add + " 50006 " + command[1] + '.log'
                    thread2 = threading.Thread(target = execc)
                    thread2.start()
                    time.sleep(3)
                elif command[0] == 'localnPackets':
                    print 'local'
                    avg_10000x = str(int(float(command[3])*10000))
                    con_dict[command[1]] = (command[2], avg_10000x)
                elif command[0] == 'set':
                    print 'set'
                    syscmd = './reconnect_all.sh' + command[1] + command[2]
                    thread6 = threading.Thread(target = execc)
                    thread6.start()


                    
            except:
                pass


if __name__ == '__main__':
    main()
