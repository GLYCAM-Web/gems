#!/usr/bin/env python3
import os, sys, importlib.util
import gemsModules
from gemsModules.common.services import *
from gemsModules.common.logic import updateResponse
from gemsModules.common import io as commonio
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *
from gemsModules.structureFile.amber.receive import preprocessPdbForAmber, evaluatePdb
from gemsModules.structureFile.amber import io as amberIO

import gemsModules.structureFile.settings as structureFileSettings
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

def receive(receivedTransaction : amberIO.Transaction):
    log.info("structureFile receive() was called.")
    log.debug("structureFile transaction.request_dict: " )
    # ## Ensure that our Transacation is the Sequence variety
    thisTransaction=amberIO.Transaction(receivedTransaction.incoming_string)
    prettyPrint(thisTransaction.request_dict)
    try:
        thisTransaction.populate_transaction_in()
    except Exception as e:
        log.error("There was a problem populating transaction_in: " + str(e))
        log.error(traceback.format_exc())
        thisTransaction.generateCommonParserNotice(noticeBrief='UnknownError')
        return


    #Look to see if services are specified, else do default.
    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doDefaultService(thisTransaction)
        
    else:
        services = thisTransaction.request_dict['entity']['services']
        log.debug("requestedServices: " + str(services))

        for requestedService in services:
            log.debug("requestedService: " + str(requestedService))

            if requestedService not in structureFileSettings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                log.error("services: " + str(structureFileSettings.serviceModules.keys()))
                thisTransaction.generateCommonParserNotice(noticeBrief='ServiceNotKnownToEntity')
                raise AttributeError(requestedService)
            elif requestedService == "PreprocessPdbForAmber":
                try:
                    log.debug("This is still in development.")
                    preprocessPdbForAmber(thisTransaction)
                except Exception as error:
                    log.error("There was a problem preprocessing the PDB for amber: " + str(error))
                    log.error(traceback.format_exc())
                    raise error

            elif requestedService == "Evaluate":
                try:
                    evaluatePdb(thisTransaction)
                except Exception as error:
                    log.error("There was a problem evaluating the pdb: " + str(error))
                    log.error(traceback.format_exc())
                    raise error

            elif requestedService == "Schema":
                ## This one is unique. No inputs are needed. Used by website only.
                try:
                    output = amberIO.StructureFileSchemaForWebOutput()
                    log.debug("output generated. obj type: " + repr(output))
                    thisTransaction.createStructureFileResponse(serviceType="Schema", inputs={}, outputs=[output])
                    thisTransaction.build_outgoing_string()
                    log.debug("thisTransaction now: ")
                    prettyPrint(thisTransaction.__dict__)
                except Exception as error:
                    log.error("There was a problem generating the structureFile schema response: " + str(error))
                    log.error(traceback.format_exc())
                    thisTransaction.generateCommonParserNotice(noticeBrief='UnknownError')

    return thisTransaction

            

def doDefaultService(thisTransaction : commonio.Transaction):
    log.info("doDefaultService() was called.\n")
    ##Preprocess PDB will be the default. Given a request to the StructureFile entity,
    ##  with no services or options defined, look for a pdb file and preprocess it for Amber.
    try:
        evaluatePdb(thisTransaction)
    except Exception as error:
        log.error("There was a problem doing the default service in the structureFile module.")
        raise error
    
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

    thisTransaction = commonio.Transaction(jsonObjectString)

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

