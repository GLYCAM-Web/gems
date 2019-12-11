import gemsModules
from gemsModules.project.settings import *
from gemsModules.common.transaction import *
from gemsModules.common import utils
from datetime import datetime

import  os, logging, sys, uuid

##TO set logging verbosity, edit this var to one of the following:
##  logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
debugLevel=logging.DEBUG

loggers = {}

def receive(thisTransaction : Transaction):
    log.info("receive() was called.")
    myProject = Project()
    myProject.buildProject(thisTransaction)
    log.debug("myProject: " + str(myProject))
    # project.input_dir =
    # project.output_dir = settings.output_data_root + "tools/" + str(uuid.uuid4())
    # project.requesting_agent = "Command line"
    # log.debug("project: " + str(project))

def main():
    log.info("main() was called.")
    log.debug("number of args: " + str(len(sys.argv)))
    if len(sys.argv) == 2:
        jsonObjectString = utils.JSON_From_Command_Line(sys.argv)
        log.debug("jsonObjectString: " + jsonObjectString)
        thisTransaction=Transaction(jsonObjectString)
        receive(thisTransaction)
    else:
        log.error("You must provide a path to a json request file.")

if __name__ == "__main__":
    if loggers.get(__name__):
        pass
    else:
        log = logging.getLogger(__name__)
        log.setLevel(debugLevel)
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(debugLevel)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',  datefmt='%m/%d/%Y %I:%M:%S %p')
        streamHandler.setFormatter(formatter)
        log.addHandler(streamHandler)
        loggers[__name__] = log
    main()
