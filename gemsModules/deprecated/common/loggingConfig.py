import logging, os
import gemsModules.deprecated
from gemsModules.deprecated import common
from gemsModules.deprecated.common import settings

##TODO Create custom logging levels for critical errors to be able to specify
##  email recipient.

## Set the verbosity via the GEMS_LOGGING_LEVEL environment var.
def getGemsLoggingLevel():
    try:
        loggingLevel = os.environ.get('GEMS_LOGGING_LEVEL')
        
        if loggingLevel == None:
            loggingLevel = logging.ERROR
        elif loggingLevel == "error":
            loggingLevel = logging.ERROR
        elif loggingLevel == "info":
            loggingLevel = logging.INFO
        elif loggingLevel == "debug":
            loggingLevel = logging.DEBUG
        else:
            print("The only valid values for GEMS_LOGGING_LEVEL are: error, info, or debug: " + str(loggingLevel))
        return loggingLevel
    except Exception as error:
        return logging.ERROR

LOGGING_LEVEL = getGemsLoggingLevel()
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

        ##File Handlers
        logsDir = getLogsDir()
        errorFileHandler = logging.FileHandler(logsDir + "git-ignore-me_gemsError.log")
        errorFileHandler.setLevel(logging.ERROR)
        
        if LOGGING_LEVEL > 10:
            infoFileHandler = logging.FileHandler(logsDir + "/git-ignore-me_gemsInfo.log")
            infoFileHandler.setLevel(logging.INFO)
        elif LOGGING_LEVEL > 0:
            debugFileHandler = logging.FileHandler(logsDir + "/git-ignore-me_gemsDebug.log")
            debugFileHandler.setLevel(logging.DEBUG)
            infoFileHandler = logging.FileHandler(logsDir + "/git-ignore-me_gemsInfo.log")
            infoFileHandler.setLevel(logging.INFO)


        ##Formatters
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',  datefmt='%Y-%m-%d %I:%M:%S %p')
        errorFileHandler.setFormatter(formatter)
        
        if LOGGING_LEVEL > 10:
            infoFileHandler.setFormatter(formatter)
        elif LOGGING_LEVEL > 0:
            debugFileHandler.setFormatter(formatter)
            infoFileHandler.setFormatter(formatter)

        #log.addHandler(streamHandler)
        log.addHandler(errorFileHandler)
        if LOGGING_LEVEL > 10:
            log.addHandler(infoFileHandler)
        elif LOGGING_LEVEL > 0:
            log.addHandler(debugFileHandler)
            log.addHandler(infoFileHandler)

        loggers[name] = log
        # log.debug("created a new logger for: " + name + ", LOGGING_LEVEL: " + str(LOGGING_LEVEL))
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
