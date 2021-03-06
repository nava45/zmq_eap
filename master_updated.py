"""
It is going to communicate to subscribers and sending event signature to all subscribers
via communication bus.

1.launching the subscriber parallel, collecting subscriber info incase if send "kill" 
2.sending events to subscribers
3.closing the subscribers and collecting the results 

"""


from multiprocessing import Process
from datetime import datetime

from lib.helpers import stop_everything, \
    create_connection, get_obj_from_str
from controller import start_controller
from lib.logger import configure_logger

import zmq
import time
import sys
import logging

#Constants
from settings import *


def worker(pid):
    
    work_receiver = create_connection("PULL", CONTROLLER_IP, CONTROLLER_PORT, "connect")
    results_sender = create_connection("PUSH", RESULT_SENDER_IP, RESULT_SENDER_PORT, "connect")
    result_status_receiver = create_connection("SUB", RESULT_COLLECTOR_IP, RESULT_COLLECTOR_PORT, "connect", topic_filter="")

    poller = zmq.Poller()
    poller.register(work_receiver, zmq.POLLIN)
    poller.register(result_status_receiver, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())
        
        if socks.get(work_receiver) == zmq.POLLIN:
            work_message = work_receiver.recv_json()
       
            if work_message.get('quit',0):
                print "kill command received from controller..by worker-%s" %pid
                results_sender.send_json(work_message)
                results_sender.close()
                result_status_receiver.close()
                work_receiver.close()
                break
            
            
            task_func = get_obj_from_str(work_message['task'])
            if task_func:
                task_func(work_message['payload'])

            product = work_message['num'] * work_message['num']
            work_message['worker_name'] = pid
            work_message['result'] = product
            work_message['finished_at'] = str(datetime.utcnow())

            results_sender.send_json(work_message)

        if socks.get(result_status_receiver) == zmq.POLLIN:
            status_message = result_status_receiver.recv()
            
            if status_message == "DONE":
                print("Worker %i received FINSHED, quitting!" % pid)
                break


def result_manager():
    results_receiver = create_connection("PULL", RESULT_SENDER_IP, RESULT_SENDER_PORT, "bind")
    result_status_sender = create_connection("PUB", RESULT_COLLECTOR_IP, RESULT_COLLECTOR_PORT, "bind")

    for task_nbr in range(NUM_JOBS):
        result_message = results_receiver.recv_json()
        if result_message['quit']:
            result_status_sender.send("Quitting!!")
        else:
            print "Worker %i has done the job. =%i" % (result_message['worker_name'], result_message['result'])

    result_status_sender.send("DONE")
    time.sleep(5)


if __name__ == '__main__':
    
    worker_pool = range(NUM_WORKERS)

    #for i in range(10):
    #    worker(i)
    #Worker process
    for worker_id in worker_pool:
        Process(target=worker, args=(worker_id,)).start()

    #result collector
    result_manager = Process(target=result_manager, args=())
    result_manager.start()

   
