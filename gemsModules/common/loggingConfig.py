import logging
import gemsModules
from gemsModules import common
from gemsModules.common import settings

loggers = {}

def createLogger(name):
    debugLevel=settings.LOGGING_LEVEL

    if(loggers.get(name)):
        log.debug("logger already exists with name: " + name)
    else:
        log = logging.getLogger(name)
        log.setLevel(debugLevel)
        logging.getLogger(name)
        log.setLevel(debugLevel)
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(debugLevel)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',  datefmt='%Y-%m-%d %I:%M:%S %p')
        streamHandler.setFormatter(formatter)
        log.addHandler(streamHandler)
        loggers[name] = log
        log.debug("created a new logger for: " + name)
    return log
