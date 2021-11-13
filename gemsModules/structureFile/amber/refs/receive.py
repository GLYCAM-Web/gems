#!/usr/bin/env python3
import os, sys, importlib.util
import pathlib
import urllib.request
import gemsModules
import gmml
import traceback

from collections import defaultdict
from collections import OrderedDict

from gemsModules.project.projectUtil import *
from gemsModules.common.logic import appendResponse, prettyPrint, updateResponse
from gemsModules.common import io as commonio
import gemsModules.structureFile.amber.io as amberIO

from gemsModules.common.loggingConfig import *
import gemsModules.structureFile.amber.settings as amberStructureSettings

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##  Evaluate a pdb for use with Amber.
#   @param thisTransaction A request containing either the path to an uploaded pdb, or a pdbID for sideloading.
def evaluatePdb(thisTransaction : commonio.Transaction):
    log.info("evaluatePdb() was called.")

    log.debug("\n\nthisTransaction.response_dict: " + str(thisTransaction.response_dict))
    uploadedFileName = thisTransaction.response_dict['project']['uploaded_file_name']
    log.debug("uploadedFileName: " + uploadedFileName)

    projectDir = thisTransaction.response_dict['project']['project_dir']
    uploadFile = projectDir + "/uploads/" + uploadedFileName
    log.debug("uploadFile: " + uploadFile)


    ### generate the processed pdb's content
    try:
        output = amberIO.EvaluationOutput(uploadFile)
        outputDict = output.dict(by_alias=True)
        log.debug("outputDict: \n\n")
        prettyPrint(outputDict)
    except Exception as error:
        log.error("There was a problem evaluating the uploaded file: " + str(error))
        log.error(traceback.format_exc())
        raise error

    ## Add the output to the response.
    try:
        inputs = []
        inputs.append(uploadedFileName)
        outputs = []
        outputs.append(outputDict)
        log.debug("Attempting to build the response.")
        log.debug("inputs: " + repr(inputs))
        log.debug("outputs: " + repr(outputs))
        responseObj = amberIO.ServiceResponse("Evaluate", inputs=inputs, outputs=outputs)
    except Exception as error:
        log.error("There was a problem building an evaluation response: " + str(error))
        log.error(traceback.format_exc())
        raise error

    updateResponse(thisTransaction, responseObj.dict(by_alias=True))
    try:
        log.debug("About to build the outgoing string.")
        thisTransaction.build_outgoing_string()
        
    except Exception as error:
        log.error("There was a problem building the outgoing string: " + str(error))
        log.error(traceback.format_exc())
        raise error

        


def preprocessPdbForAmber(thisTransaction : commonio.Transaction):
    log.info("preprocessPdbForAmber() was called. Still in Development!!!!!!!!")
    output = amberIO.PreprocessPdbForAmberOutput()

    ##TODO: write the logic to evaluate, and then write the processed pdb out to file.

    ## Keep this stuff for a reference, but replace it with better stuff. 
    ##VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
    
    # try:
    #     pdbFile = generatePdbFile(thisTransaction)
    #     log.debug("pdbFile output: " + str(pdbFile))
    # except Exception as error:
    #     log.error("There was a problem generating the PDB output.")
    #     raise error
    # else:

    #     ### Write the content to file
    #     try:
    #         writePdbOutput(thisTransaction, pdbFile)
    #     except Exception as error:
    #         log.error("There was a problem writing the pdb output." + str(error))
    #         raise error

    ##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    

        
    
