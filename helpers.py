import zmq
import sys
import multiprocessing
import logging

from settings import publisher_port, publisher_address
from logger import configure_logger

ip_addr = publisher_address
publisher_port = publisher_port
ctx = zmq.Context()
sock = ctx.socket(zmq.SUB)
sock.connect("tcp://%s:%s" %(ip_addr, publisher_port))

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


def launch_subscribers(ip_addr, master_port, event_sign=None, topic=''):

    current_process = multiprocessing.current_process().name
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect("tcp://%s:%s" %(ip_addr, publisher_port))
    sock.setsockopt(zmq.SUBSCRIBE, topic)
  
    while True:
        recv_msg = sock.recv()
        log.info( "%s receiving %s" %(current_process, recv_msg))
