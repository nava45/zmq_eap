"""
It is going to communicate to subscribers and sending event signature to all subscribers
via communication bus.

1.launching the subscriber parallel, collecting subscriber info incase if send "kill" 
2.sending events to subscribers
3.closing the subscribers and collecting the results 

"""


from multiprocessing import Process
from helpers import launch_subscribers, stop_everything
from controller import start_controller
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
TOT_JOBS = TOT_JOBS


def worker(pid):
    context = zmq.Context()

    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://127.0.0.1:5557")

    results_sender = context.socket(zmq.PUSH)
    results_sender.connect("tcp://127.0.0.1:5558")

    control_receiver = context.socket(zmq.SUB)
    control_receiver.connect("tcp://127.0.0.1:5559")
    control_receiver.setsockopt(zmq.SUBSCRIBE, "")

    poller = zmq.Poller()
    poller.register(work_receiver, zmq.POLLIN)
    poller.register(control_receiver, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())
        
        if socks.get(work_receiver) == zmq.POLLIN:
            work_message = work_receiver.recv_json()
            product = work_message['num'] * work_message['num']
            answer_message = { 'worker' : pid, 'result' : product }
            results_sender.send_json(answer_message)

        if socks.get(control_receiver) == zmq.POLLIN:
            control_message = control_receiver.recv()
            if control_message == "DONE":
                print("Worker %i received FINSHED, quitting!" % pid)
                break


def result_manager():
    context = zmq.Context()
   
    results_receiver = context.socket(zmq.PULL)
    results_receiver.bind("tcp://127.0.0.1:5558")

    control_sender = context.socket(zmq.PUB)
    control_sender.bind("tcp://127.0.0.1:5559")

    for task_nbr in range(TOT_JOBS):
        result_message = results_receiver.recv_json()
        print "Worker %i answered: %i" % (result_message['worker'], result_message['result'])

    control_sender.send("DONE")
    time.sleep(5)


if __name__ == '__main__':
    
    worker_pool = range(TOT_WORKERS)

    #Worker process
    for worker_id in range(len(worker_pool)):
        Process(target=worker, args=(worker_id,)).start()

    #result collector
    result_manager = Process(target=result_manager, args=())
    result_manager.start()

   
