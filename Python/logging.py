import logging

FORMAT = '%(asctime)s %(name)s %(levelname)s:\n\t%(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    #datefmt='%d/%b/%y %H:%M:%S.%f'
)
logger = logging.getLogger('encoding')