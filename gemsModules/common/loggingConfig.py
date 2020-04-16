import logging, os
import gemsModules
from gemsModules import common
from gemsModules.common import settings

##TODO Create custom logging levels for critical errors to be able to specify
##  email recipient.

##TO set the global logging verbosity, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
##  Note: this is overridden by the logLevel set in individual files.
LOGGING_LEVEL = logging.DEBUG

loggers = {}

"""
Creates a logging solution for writing to the console. Can add handlers if
we want to write logs to file, send emails, etc...
"""
def createLogger(name):
    #print("name: " + name + ", LOGGING_LEVEL: " + str(LOGGING_LEVEL))

    if(loggers.get(name)):
        log.debug("logger already exists with name: " + name)
    else:
        log = logging.getLogger(name)
        log.setLevel(LOGGING_LEVEL)

        ##StreamHandler sends logs to std out.
        # streamHandler = logging.StreamHandler()
        # streamHandler.setLevel(LOGGING_LEVEL)
        ##Logging to file.
        logsDir = getLogsDir()
        debugFileHandler = logging.FileHandler(logsDir + "/git-ignore-me_gemsDebug.log")
        debugFileHandler.setLevel(logging.DEBUG)
        infoFileHandler = logging.FileHandler(logsDir + "/git-ignore-me_gemsInfo.log")
        infoFileHandler.setLevel(logging.INFO)
        errorFileHandler = logging.FileHandler(logsDir + "git-ignore-me_gemsError.log")
        errorFileHandler.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',  datefmt='%Y-%m-%d %I:%M:%S %p')
        #streamHandler.setFormatter(formatter)
        debugFileHandler.setFormatter(formatter)
        infoFileHandler.setFormatter(formatter)
        errorFileHandler.setFormatter(formatter)

        #log.addHandler(streamHandler)
        log.addHandler(debugFileHandler)
        log.addHandler(infoFileHandler)
        log.addHandler(errorFileHandler)

        loggers[name] = log
        log.debug("created a new logger for: " + name + ", LOGGING_LEVEL: " + str(LOGGING_LEVEL))
    return log

def getLogsDir():
    GEMSHOME = os.environ.get('GEMSHOME')
    if GEMSHOME == None:
        ##Print statements break the website. However, so does a delgator container that 
        #   cannot find GEMSHOME, and logs do not exist at the point this is called.
        print("""

        GEMSHOME environment variable is not set.

        Set it using somthing like:

          BASH:  export GEMSHOME=/path/to/gems
          SH:    setenv GEMSHOME /path/to/gems
        """)
    logsDir = GEMSHOME + "/logs/"
    if not os.path.exists(logsDir):
        os.makedirs(logsDir)
    return logsDir
