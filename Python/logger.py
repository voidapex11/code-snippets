import logging

FORMAT = '%(asctime)s %(name)s:%(process)d %(levelname)s:\n\t%(message)s\n'  # logging format
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,  # set to DEBUG to show debug mesages
    handlers=[
        logging.FileHandler("app.log"),  # writes to file and console
        logging.StreamHandler()
    ])

# example context:
#logger = logging.getLogger('')
