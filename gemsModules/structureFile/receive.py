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
        
        # log.debug("receivedTransaction: " + str(receivedTransaction))
        # log.debug("Transaction:")
        # log.debug(dir(receivedTransaction))
        log.debug("request_dict: ")
        prettyPrint(pdbTransaction.request_dict)
        # log.debug("pdbTransaction: " + str(pdbTransaction))
        # log.debug("pdbTransaction:")
        # log.debug(dir(pdbTransaction))

    except Exception as e:
        log.error("There was a problem instantiating the PdbTransaction: " + str(e))
        log.error(traceback.format_exc())
        pdbTransaction.generateCommonParserNotice(noticeBrief='UnknownError')
        return

    try:    
        pdbTransaction.populate_transaction_in()
    except Exception as e:
        log.error("There was a problem populating the the PdbTransaction in: " + str(e))
        log.error(traceback.format_exc())
        pdbTransaction.generateCommonParserNotice(noticeBrief='UnknownError')
        return

    ## TODO: need to call the service.
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

