import zmq
import sys

from logger import configure_logger

ctx = zmq.Context()
sock = ctx.socket(zmq.SUB)

log = configure_logger()

def launch_subscribers(ip_addr, master_port, event_sign=None, topic=''):
    print master_port, event_sign
    log.error('reciving the signal..')
    log.info('yes..info')

    """
    sock.connect("tcp://%s:%s" %(ip_addr, master_port))
    if topic:
        sock.setsockopt(zmq.SUBSCRIBE, topic)
    """
