from socket import *
from select import *
import sys
import Queue
import threading
import time

class SocketReceiver:
    def __init__(self, queue):
        self.queue = queue
        self.host = ''
        self.port = 50006
        self.serverObj = socket(AF_INET, SOCK_STREAM)
        self.serverObj.bind((self.host, self.port))
        self.serverObj.listen(5)

    def loop(self):
        global runZZ
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
                        self.queue.put(str(address))
                        self.queue.put(str(buf))
                        connection.send('Echo:' + buf)
                connection.close()

run = 0
def parseAdd(add):
    str = add.split(',', '(', ')')
    return str

def parse(msg):
    str = msg.split(' ')
    return str

def main():
    global run
    run = 1
    queue = Queue.Queue()
    sr = SocketReceiver(queue)
    sckt_thread = threading.Thread(target = sr.loop)
    sckt_thread.start()

    while True:
        time.sleep(3)
        while queue.qsize():
            try:
                add = queue.get(0)
                msg = queue.get(0)

                command = parse(msg)
                print command[0]
                print command[0] == "nPackets"
                address = parseAdd(add)
                if(command[0] == "nPackets"):
		    print 'a match report'
		    print address[0],":",  command[1]
                print "From queue, get msg:", add, avg
            except:
                pass


if __name__ == '__main__':
    main()
