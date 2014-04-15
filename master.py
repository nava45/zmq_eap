"""
It is going to communicate to subscribers and sending event signature to all subscribers
via communication bus.

1.launching the subscriber parallel, collecting subscriber info incase if send "kill" 
2.sending events to subscribers
3.closing the subscribers and collecting the results 

"""


from  multiprocessing import Process
from helpers import launch_subscribers, stop_everything
from settings import *
from logger import configure_logger

import zmq
import time
import sys
import logging

#Constants
ip_addr = publisher_address
port = publisher_port
TOT_WORKERS = total_workers
event_list = ("addition", "multiply",)
event_sign = event_list[0]
topic = "even"

#log = logging.getLogger('myzmq')
log = configure_logger()

def connect():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.bind("tcp://%s:%s" %(ip_addr, port))
    return sock


def init():
    context = zmq.Context()
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://%s:%s" %(controller_address, controller_port))
    while True:
        work_message = work_receiver.recv_json()

        log.info('control message received from controller: %s' %(work_message))
      
        if work_message and work_message.get('job') == 'start':
            exec_manager()
        elif work_message.get('job') == 'stop':
            stop_everything()
        else:
            print "##### enter the proper command #####"


#1. launch subscribers
def create_subscribers():
    for i in range(TOT_WORKERS):
        mp = Process(name='Worker-%s' %i, target=launch_subscribers, args=(ip_addr, port, event_sign, topic,))
        mp.start()
        time.sleep(0.3)
   

def send_events(sock):
    """
    sending events to the subscribers
    """
    i=0
    while i<10:
        log.info('Sending message from publisher..')
        sock.send("even - hai i am publisher")
        time.sleep(0.2)
        i += 1


def exec_manager():
    """
    The list of all real steps of this master process
    """
    socket = connect()
    create_subscribers()
    send_events(socket)


init()
