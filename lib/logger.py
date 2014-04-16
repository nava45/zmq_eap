import logging
from settings import LOG_FILE

def configure_logger():
    lgr = logging.getLogger('myzmq')
    lgr.setLevel(logging.DEBUG)
    fh = logging.FileHandler('%s' %LOG_FILE)
    fh.setLevel(logging.DEBUG)
    frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(frmt)
    lgr.addHandler(fh)

    return lgr


def _configure_logger():
    return logging.getLogger()
