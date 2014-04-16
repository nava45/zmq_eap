import zmq
import sys
import multiprocessing
import logging

from settings import *
from lib.logger import configure_logger


#log = logging.getLogger('myzmq')
log = configure_logger()


def stop_everything():
    """
    Stopping execution

     It has to stop all the context of zmq and terminate immediately.
     ****not working****
    """
    log.info("exit from everything..")
    sys.exit(0)



def create_connection(sock_type, address, port, \
                          connection_method, \
                          topic_filter=""):
    """
    This fn helps to create a websocket according to the args
    :sock_type = PUB, PUSH, PULL, SUB
    :address = "127.0.0.1"
    :port = 5376
    :connection_method = bind or connect
    :topic_filter = if the sock_type PULL, pass the topic filter

    """
    context = zmq.Context()
    ws = context.socket(SOCK_TYPES[sock_type])
    
    if connection_method == 'bind':
        ws.bind("tcp://%s:%s" %(address, port))
    else:
        ws.connect("tcp://%s:%s" %(address, port))

    if sock_type == 'SUB':
        ws.setsockopt(zmq.SUBSCRIBE, topic_filter)

    return ws
   

#Obsolete 
"""
def launch_subscribers(ip_addr, master_port, event_sign=None, topic=''):

    current_process = multiprocessing.current_process().name
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect("tcp://%s:%s" %(ip_addr, publisher_port))
    sock.setsockopt(zmq.SUBSCRIBE, topic)
  
    while True:
        recv_msg = sock.recv()
        log.info( "%s receiving %s" %(current_process, recv_msg))
"""
