#!/usr/bin/env python3
import os, sys, importlib.util
import gemsModules
from gemsModules.common.services import *
from gemsModules.common.logic import updateResponse
from gemsModules.common import io as commonIO
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

## Receives requests related to preprocessing files 

def receive(receivedTransaction : commonIO.Transaction):
    log.info("structureFile receive() was called.")
    ## This transaction pattern is strange. We take a generic transaction and instantiate that in 
    ##  the delegator, then use that here to create a new object that is a typed version
    ##  of the same class? 
    try:
        # ## Ensure that our Transacation is the Sequence variety
        pdbTransaction=amberIO.PdbTransaction(receivedTransaction.incoming_string)
        log.debug("pdbTransaction: " )
        prettyPrint(pdbTransaction.request_dict)
        pdbTransaction.populate_transaction_in()
    except Exception as e:
        log.error("There was a problem instantiating the PdbTransaction: " + str(e))
        log.error(traceback.format_exc())
        pdbTransaction.generateCommonParserNotice(noticeBrief='UnknownError')
        return


    log.debug("Looky here!!!")

    #Look to see if services are specified, else do default.
    if 'services' not in pdbTransaction.request_dict['entity'].keys():
        doDefaultService(pdbTransaction)
        
    else:
        services = pdbTransaction.request_dict['entity']['services']
        log.debug("requestedServices: " + str(services))

        for requestedService in services:
            log.debug("requestedService: " + str(requestedService))

            if requestedService not in structureFileSettings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                log.error("services: " + str(structureFileSettings.serviceModules.keys()))
                pdbTransaction.generateCommonParserNotice(noticeBrief='ServiceNotKnownToEntity')
                raise AttributeError(requestedService)
            elif requestedService == "PreprocessPdbForAmber":
                try:
                    log.debug("This is still in development.")
                    preprocessPdbForAmber(pdbTransaction)
                except Exception as error:
                    log.error("There was a problem preprocessing the PDB for amber: " + str(error))
                    log.error(traceback.format_exc())
                    raise error

            elif requestedService == "Evaluate":
                try:
                    evaluatePdb(pdbTransaction)
                except Exception as error:
                    log.error("There was a problem evaluating the pdb: " + str(error))
                    log.error(traceback.format_exc())
                    raise error

            elif requestedService == "Schema":
                ## This one is unique. No inputs are needed. Used by website only.
                try:
                    output = amberIO.StructureFileSchemaForWebOutput()
                    log.debug("output generated. obj type: " + repr(output))
                    pdbTransaction.createStructureFileResponse(serviceType="Schema", inputs={}, outputs=[output])
                    pdbTransaction.build_outgoing_string()
                    log.debug("pdbTransaction now: ")
                    prettyPrint(pdbTransaction.__dict__)
                except Exception as error:
                    log.error("There was a problem generating the structureFile schema response: " + str(error))
                    log.error(traceback.format_exc())
                    pdbTransaction.generateCommonParserNotice(noticeBrief='UnknownError')

    return pdbTransaction

            

def doDefaultService(receivedTransaction : commonIO.Transaction):
    log.info("doDefaultService() was called.\n")
    ##Preprocess PDB will be the default. Given a request to the StructureFile entity,
    ##  with no services or options defined, look for a pdb file and preprocess it for Amber.
    try:
        evaluatePdb(receivedTransaction)
    except Exception as error:
        log.error("There was a problem doing the default service in the structureFile module.")
        raise error
    
    receivedTransaction.build_outgoing_string()


def main():
    GemsPath = getGemsHome()
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            inputFile = sys.argv[1]
        else:
            log.error("No input file provided.")

    with open(inputFile, 'r') as file:
        jsonObjectString = file.read().replace('\n', '')

    receivedTransaction = commonIO.Transaction(jsonObjectString)

    try:
        parseInput(receivedTransaction)
    except Exception as error:
        log.error("Error parsing input.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
    receive(receivedTransaction)

    responseObjectString = receivedTransaction.outgoing_string
    return responseObjectString

if __name__ == "__main__":
    main()

