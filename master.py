"""
It is going to communicate to subscribers and sending event signature to all subscribers
via communication bus.

"""

import zmq
import time
import sys


ip_addr = "127.0.0.1"
port = "5678"

ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
sock.bind("tcp://%s:%s" %(ip_addr, port))

while 1:
    sock.send("hai i am publisher")
    print "sending master.."
