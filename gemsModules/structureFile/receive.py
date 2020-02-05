import os, sys, importlib.util
import gemsModules
from gemsModules.common.services import *
from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *
from gemsModules.structureFile.amber import receive as amberReceive
import gemsModules.structureFile.settings as structureFileSettings
import traceback

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.ERROR

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

def receive(thisTransaction):
    log.info("receive() was called.")
    log.debug("thisTransaction: " + str(thisTransaction))

    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}
    thisTransaction.response_dict['entity'] = {}
    thisTransaction.response_dict['entity']['type'] = "StructureFile"
    thisTransaction.response_dict['responses'] = []

    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doDefaultService(thisTransaction)
    else:
        services = getTypesFromList(thisTransaction.request_dict['entity']['services'])

        for requestedService in services:
            log.debug("requestedService: " + str(requestedService))
            if requestedService not in structureFileSettings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                log.error("services: " + str(mmSettings.serviceModules.keys()))
                common.settings.appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity', requestedService)
            else:
                log.warning("The rest of this module needs to be written.")

def doDefaultService(thisTransaction):
    log.info("doDefaultService() was called.")
    ##Preprocess PDB will be the default. Given a request to the StructureFile entity,
    ##  with no services or options defined, look for a pdb file and preprocess it for Amber.
    amberReceive.receive(thisTransaction)





def main():
    GemsPath = getGemsHome()
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            inputFile = sys.argv[1]
        else:
            log.error("No input file provided.")

    with open(inputFile, 'r') as file:
        jsonObjectString = file.read().replace('\n', '')

    thisTransaction = Transaction(jsonObjectString)

    try:
        parseInput(thisTransaction)
    except Exception as error:
        log.error("Error parsing input.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
    receive(thisTransaction)

    responseObjectString = thisTransaction.outgoing_string
    return responseObjectString

if __name__ == "__main__":
    main()

