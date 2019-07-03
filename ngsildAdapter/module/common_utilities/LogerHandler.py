import logging
import sys,os
sys.path.append('/root/TRANSFORMER/Next_transform/fogflow/ngsildAdapter/module')
from consts import constant
class Handler:
    def __init__(self):
        pass
    def get_logger(self):
        logger_format='[ %(asctime)s ]  %(levelname)s   %(filename)s        %(message)s'
        logging.basicConfig(filename=constant.log_path,
                    format=logger_format,
                    filemode='a')
        logger=logging.getLogger()
        logger.setLevel(constant.logging_level)
        return logger
logger_obj=Handler()
logger=logger_obj.get_logger()
print(logger.level)
