import logging

FORMAT = '%(asctime)s %(name)s %(levelname)s:\n\t%(message)s\n'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
)

#example context:
logger = logging.getLogger('')
