"""
1.Controls the master by sending commands like
       python controller.py start_master
       python controller.py stop_master
"""


import zmq
import time
import logging

from multiprocessing import Process
from optparse import OptionParser
from settings import *

log = logging.getLogger()

controller_port = 5557


def connect():
    cctx = zmq.Context()
    csock = cctx.socket(zmq.PUSH)
    csock.bind('tcp://%s:%s' %(controller_address, controller_port))
    return csock


def start_controller(job_type):
    controller_send = connect()
    time.sleep(1)
    
    for num in range(TOT_JOBS):
        task = { 'task':'send_email',
                 'payload':{'sender':'',
                            'recipient':['navaneethanit@gmail.com']
                            },
                 'task_id' : num,
                 'job_type': job_type,
                 'num': num,
                 }
        controller_send.send_json(task)

    time.sleep(1)
    log.info('sent task.')


def exemanager():
    parser = OptionParser()
    parser.add_option("-c", "--command",
                      action="store", type="string", dest="command")
    (options, args) = parser.parse_args()

    ventilator = None
    if options.command is not None:
        ventilator = Process(target=start_controller, args=(options.command,))
        ventilator.start()

exemanager()
