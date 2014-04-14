"""
It is going to communicate to subscribers and sending event signature to all subscribers
via communication bus.

1.launching the subscriber parallel, collecting subscriber info incase if send "kill" 
2.sending events to subscribers
3.closing the subscribers and collecting the results 

"""


from  multiprocessing import Process
from helpers import launch_subscribers

import zmq
import time
import sys

#Constants
ip_addr = "127.0.0.1"
port = "5678"
event_list = ("addition", "multiply",)
event_sign = event_list[0]
topic = "even"


def connect():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.bind("tcp://%s:%s" %(ip_addr, port))
    return sock


#1. launch subscribers
def create_subscribers():
    mp = Process(target=launch_subscribers, args=(ip_addr, port, event_sign, topic,))
    mp.start()
    return mp


def send_events(sock):
    """
    sending events to the subscribers
    """
    i=0
    while i<10:
        sock.send("hai i am publisher")
        print "sending master.."
        time.sleep(2)
        i += 1


def exec_manager():
    socket = connect()
    sub_id = create_subscribers()
    send_events(socket)


exec_manager()
