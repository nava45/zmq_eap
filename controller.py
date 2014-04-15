"""
1.Controls the master by sending commands like
       python controller.py start_master
       python controller.py stop_master
"""


import zmq
import time
import logging

from optparse import OptionParser
from settings import *

log = logging.getLogger()

def connect():
    cctx = zmq.Context()
    csock = cctx.socket(zmq.PUSH)
    csock.bind('tcp://%s:%s' %(controller_address, controller_port))
    return csock

def send_command(socket, user_command):
    socket.send_json({ 'job':user_command })
    time.sleep(0.1)

def manager():
    parser = OptionParser()
    parser.add_option("-c", "--command",
                      action="store", type="string", dest="command")
    (options, args) = parser.parse_args()
   
    if options.command is not None:
        socket = connect()
        send_command(socket, options.command)

manager()
