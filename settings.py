CONTROLLER_IP = "127.0.0.1"
CONTROLLER_PORT = 5676

WORKER_IP = "127.0.0.1"
WORKER_PORT = 5677

RESULT_SENDER_IP = "127.0.0.1"
RESULT_SENDER_PORT = 5672

RESULT_COLLECTOR_IP = "127.0.0.1"
RESULT_COLLECTOR_PORT = 5678 

NUM_WORKERS = 10
NUM_JOBS = 10

LOG_FILE = "app_logger.log"


import zmq
SOCK_TYPES = {
    "PULL" : zmq.PULL,
    "PUSH" : zmq.PUSH,
    "PUB" : zmq.PUB,
    "SUB" : zmq.SUB,
    "REQ" : zmq.REQ,
    "REP" : zmq.REP,
    }
