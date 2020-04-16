import os, sys, importlib.util
import gemsModules
from gemsModules.common.services import *
from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *
from gemsModules.structureFile.amber.receive import preprocessPdbForAmber
import gemsModules.structureFile.settings as structureFileSettings
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

def receive(thisTransaction):
    log.info("receive() was called.\n")
    #log.debug("thisTransaction: " + str(thisTransaction.__dict__))

    #Look to see if services are specified, else do default.
    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doDefaultService(thisTransaction)
    else:
        services = getTypesFromList(thisTransaction.request_dict['entity']['services'])
        log.debug("requestedServices: " + str(services))
        for requestedService in services:
            log.debug("requestedService: " + str(requestedService))
            if requestedService not in structureFileSettings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                log.error("services: " + str(structureFileSettings.serviceModules.keys()))
                appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity', requestedService)
                raise AttributeError(requestedService)
            elif requestedService == "PreprocessPdbForAmber":
                try:
                    preprocessPdbForAmber(thisTransaction)
                except Exception as error:
                    log.error("There was a problem preprocessing the PDB for amber: " + str(error))
                    raise error
                else:
                    thisTransaction.build_outgoing_string()

def doDefaultService(thisTransaction):
    log.info("doDefaultService() was called.\n")
    ##Preprocess PDB will be the default. Given a request to the StructureFile entity,
    ##  with no services or options defined, look for a pdb file and preprocess it for Amber.
    try:
        preprocessPdbForAmber(thisTransaction)
    except Exception as error:
        log.error("There was a problem doing the default service in the structureFile module.")
        raise error
    else:
        thisTransaction.build_outgoing_string()


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

