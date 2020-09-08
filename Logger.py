
import logging
import datetime
import string
temp = string.Template("WOOJUNG LOG ${var}.log")
filename = temp.substitute(var=datetime.datetime.now())
logFormat = '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(filename="WOOJUNG's LOG.log", level=logging.DEBUG, format=logFormat)
logger = logging.getLogger()
#formatter = logging.Formatter(logFormat)

streamHandler = logging.StreamHandler()
#fileHandler = logging.FileHandler('./WOOJUNG\'s LOG.log')
#fileHandler.setFormatter(formatter)
logger.setLevel(level=logging.DEBUG)
logger.addHandler(streamHandler)
#logger.addHandler(fileHandler)
