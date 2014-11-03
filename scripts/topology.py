#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
import sys

def multiControllerNet( number ):
    "Create a network from semi-scratch with multiple controllers."

    net = Mininet( controller=Controller, switch=OVSSwitch, build=False )

    print "*** Creating (reference) controllers"
    c0 = net.addController( 'c0' , port=(7700))

    s_count = int(number)
    h_count = s_count * 2

#    sys.exit("END");

    hosts = [0] * h_count
    switches = [0] * s_count

    for i in range(h_count):
        hosts[i] = net.addHost('h' + str(i))
 
    for i in range(s_count):
        switches[i] = net.addSwitch('s' + str(i))

    print "*** Creating links between hosts and #switch"
    for i in range(s_count):
        net.addLink( switches[i],hosts[i * 2] )
        net.addLink( switches[i],hosts[i * 2 + 1] )

    print "*** Creating links between switches"
    for i in range(s_count-1):
        net.addLink( switches[i],switches[i+1] )

 
    print "*** Starting network"
    net.build()

    c0.start()
    
    for i in range(s_count):
        switches[i].start( [c0] )
   

    
    print "*** Testing network"
#    net.pingAll()

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output

    if len(sys.argv) < 3:
        print "Usage: sudo ./topo1.py -s [switch number]\n"
        sys.exit(1)
    elif sys.argv[1] == "-s":
        multiControllerNet(sys.argv[2])
