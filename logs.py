import logging

def get_logging(logging_name):
    logging.basicConfig(filename='stdout.log',
                        format='%(asctime)s %(levelname)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.debug("test debug")
    return logger