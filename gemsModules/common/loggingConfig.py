import logging
import gemsModules
from gemsModules import common
from gemsModules.common import settings

##TODO Create custom logging levels for critical errors to be able to specify
##  email recipient.

##TO set the global logging verbosity, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
##  Note: this is overridden by the logLevel set in individual files.
LOGGING_LEVEL = logging.ERROR

loggers = {}

"""
Creates a logging solution for writing to the console. Can add handlers if
we want to write logs to file, send emails, etc...
"""
def createLogger(name, logLevel = LOGGING_LEVEL):
    #print("name: " + name + ", LOGGING_LEVEL: " + str(LOGGING_LEVEL))
    debugLevel=logLevel


    if(loggers.get(name)):
        log.debug("logger already exists with name: " + name)
    else:
        log = logging.getLogger(name)
        log.setLevel(debugLevel)

        ##StreamHandler sends logs to std out.
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(debugLevel)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',  datefmt='%Y-%m-%d %I:%M:%S %p')
        streamHandler.setFormatter(formatter)

        log.addHandler(streamHandler)

        loggers[name] = log
        log.debug("created a new logger for: " + name + ", LOGGING_LEVEL: " + str(LOGGING_LEVEL))
    return log
