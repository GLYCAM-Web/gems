import os, sys, importlib.util
import gemsModules
from gemsModules.common.services import *
from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *
from gemsModules.structureFile.amber.receive import preprocessPdbForAmber
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
    log.info("receive() was called.\n")
    #log.debug("thisTransaction: " + str(thisTransaction.__dict__))

    ##Begin building a response dict for holding output.
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}
    thisTransaction.response_dict['entity'] = {}
    thisTransaction.response_dict['entity']['type'] = "StructureFile"
    thisTransaction.response_dict['responses'] = []

    #Look to see if services are specified, else do default.
    if 'services' not in thisTransaction.request_dict['entity'].keys():
        try:
            doDefaultService(thisTransaction)
        except Exception as error:
            log.error("There was a problem doing the default service.")
            log.error("Error type: " + str(type(error)))
            log.error(traceback.format_exc())
    else:
        services = getTypesFromList(thisTransaction.request_dict['entity']['services'])
        log.debug("requestedServices: " + str(services))
        for requestedService in services:
            log.debug("requestedService: " + str(requestedService))
            if requestedService not in structureFileSettings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                log.error("services: " + str(structureFileSettings.serviceModules.keys()))
                common.settings.appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity', requestedService)
            elif requestedService == "PreprocessPdbForAmber":
                try:
                    preprocessPdbForAmber(thisTransaction)
                except Exception as error:
                    log.error("There was a problem preprocessing this file for Amber.")
                    log.error("Error type: " + str(type(error)))
                    log.error(traceback.format_exc())
                    ##TODO: Figure out what sort of errors get caught here,
                    ##  Then figure out appropriate error types to return
                    ##common.settings.appendCommonParserNotice(thisTransaction, "UnknownError", requestedService)
            else:
                log.warning("The rest of this module needs to be written.")

def doDefaultService(thisTransaction):
    log.info("doDefaultService() was called.\n")
    ##Preprocess PDB will be the default. Given a request to the StructureFile entity,
    ##  with no services or options defined, look for a pdb file and preprocess it for Amber.
    preprocessPdbForAmber(thisTransaction)

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

