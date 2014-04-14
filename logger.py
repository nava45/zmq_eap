import logging

def configure_logger(file_path='myzmq_eapp.log'):
    lgr = logging.getLogger('myzmq')
    lgr.setLevel(logging.DEBUG)
    fh = logging.FileHandler('%s' %file_path)
    fh.setLevel(logging.WARNING)
    frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(frmt)
    lgr.addHandler(fh)

    return lgr
