#!/usr/bin/python

"""
This example creates a multi-controller network from semi-scratch by
using the net.add*() API and manually starting the switches and controllers.

This is the "mid-level" API, which is an alternative to the "high-level"
Topo() API which supports parametrized topology classes.

Note that one could also create a custom switch class and pass it into
the Mininet() constructor.
"""

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def multiControllerNet():
    "Create a network from semi-scratch with multiple controllers."

    net = Mininet( controller=Controller, switch=OVSSwitch, build=False )

    print "*** Creating (reference) controllers"
    c0 = net.addController( 'c0' , port=7700 )

    h1 = net.addHost('h0')
    h2 = net.addHost('h1') 
 
    s0 = net.addSwitch('s0')
    s1 = net.addSwitch('s1')   

    print "*** Creating links between hosts and #switch"
    net.addLink( s0,h1 )
    net.addLink( s1,h2 )
    net.addLink( s0,s1 )


    print "*** Creating links between switches"
    #net.addLink( s00,s01 )
 
        
    print "*** Starting network"
    net.build()
    c0.start()
    

    s0.start( [c0] )
    s1.start( [c0] )
   

    
    print "*** Testing network"
    #net.pingAll()

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    multiControllerNet()
