from LogerHandler import Handler
obj=Handler()
logger=obj.get_logger()
print(logger.level)
current_number = 0
logger.debug(current_number)
logger.info('Still clearing number!!')


