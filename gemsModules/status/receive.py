import sys, os, re, importlib.util
import gemsModules
import gmml
#from gemsModules.common.services import *
from gemsModules.common import services as commonservices  # this is too broken
from gemsModules.common import logic as commonlogic
#from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common import transaction # REFACTOR NOTE:  this code is being deprecated.  use common.jsoninterface
from gemsModules.common.loggingConfig import *
from gemsModules.status import settings as statussettings
from gemsModules.status import statusResponse
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


## REFACTOR NOTE:  Many things have changed.  Leaving only traces of what was.


def receive(thisTransaction : transaction.Transaction):
    log.info("receive() was called.\n")

def doDefaultService(thisTransaction : transaction.Transaction):
    log.info("doDefaultService() was called.\n")
    generateReport(thisTransaction)

## Reports on every gemsModule and their corresponding services.
def generateReport(thisTransaction : transaction.Transaction):
    log.info("doDefaultService() was called.\n")

def buildStatusResponseConfig(responses):
    log.info("buildStatusResponseConfig() was called.\n")

##Append a status from a module's settings file to a json response object
def getModuleStatus(response, settings, settingsAttributes):
    log.info("getModuleStatus() was called.\n")

##Append a module status detail from a module's settings file to a json response object
def getModuleStatusDetail(response, settings, settingsAttributes):
    log.info("getModuleStatusDetail() was called.\n")

##Append a list of module services and their statuses to a json response object
def getServiceStatuses(response, settings, settingsAttributes):
    log.info("getServiceStatuses() was called.\n")

##Update a response with the entities an entity uses.
def getSubEntities(response, settings, settingsAttributes):
    log.info("getSubEntities() was called.\n")

def main():
    ## TODO:  Write this to do something
    pass

if __name__ == "__main__":
    main()
