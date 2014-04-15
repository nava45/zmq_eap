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




def control_manager():
    context = zmq.Context()
    control_receiver = context.socket(zmq.PULL)
    control_receiver.bind("tcp://%s:%s" %(controller_ip, controller_port))

    data_sender = context.socket(zmq.PUSH)
    data_sender.bind("tcp://127.0.0.1:5557")

    task_sender = context.socket(zmq.PUB)
    task_sender.bind("tcp://%s:%s" %(task_sender_ip, task_sender_port))

    while True:
        control_msg = control_receiver.recv_json()
        if control_msg.get('job') == 'start':
            task_sender.send_json({'quit':False,
                                   'task':'send_email', 
                                   'payload':{'receipients':
                                                  ['navaneethanit@gmail.com']
                                              }
                                   })
        elif control_msg.get('job') == 'stop':
            task_sender.send_json({'quit':True})
            time.sleep(0.5)
        else:
            pass

  
def suscriber_manager(sub_id):
    context = zmq.Context()
    task_receiver = context.socket(zmq.SUB)
    task_receiver.connect("tcp://127.0.0.1:5559")
    task_receiver.setsockopt(zmq.SUBSCRIBE, "")
    


def init():
    context = zmq.Context()
    control_receiver = context.socket(zmq.PULL)
    control_receiver.connect("tcp://%s:%s" %(controller_address, controller_port))

    
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://%s:%s" %(controller_address, controller_port))


    poller = zmq.Poller()
    poller.register(work_receiver, zmq.POLLIN)
    poller.register(control_receiver, zmq.POLLIN)


    while True:
        socks = dict(poller.poll())

        if socks.get(work_receiver) == zmq.POLLIN:
            work_message = work_receiver.recv_json()
            task = work_message['task_name'] 
            results_sender.send_json(answer_message)

        # If the message came over the control channel, shut down the worker.
        if socks.get(control_receiver) == zmq.POLLIN:
            control_message = control_receiver.recv()
            if control_message == "FINISHED":
                log.info("Worker %i received FINSHED, quitting!" % wrk_num)
                break







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
    The list of all real steps of this master processt ("tcp://localhost:
    """
    socket = connect()
    create_subscribers()
    send_events(socket)


init()
