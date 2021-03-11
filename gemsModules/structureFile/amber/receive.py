import os, sys, importlib.util
import pathlib
import urllib.request
import gemsModules
import gmml
import traceback

from collections import defaultdict
from collections import OrderedDict

from gemsModules.common.transaction import *
from gemsModules.common.logic import appendResponse
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *
import gemsModules.structureFile.amber.settings as amberStructureSettings

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##  Evaluate a pdb for use with Amber.
#   @param thisTransaction A request containing either the path to an uploaded pdb, or a pdbID for sideloading.
def evaluatePdb(thisTransaction):
    log.info("evaluatePdb() was called.\n")
    try:
        ### Some projects will already have been created. 
        #   However, these two conditions need new projects.
        if thisTransaction.response_dict == None: 
            project = startProject(thisTransaction)
        elif 'project' not in thisTransaction.response_dict.keys():
            project = startProject(thisTransaction)
        else:
            log.debug("response_dict or project already exists, not starting a project.")

        prettyPrint(thisTransaction.request_dict)

    except Exception as error:
        log.error("There was a problem starting a pdb project." + str(error))
        raise error
    else:
        log.debug("\n\nthisTransaction.response_dict: " + str(thisTransaction.response_dict))
        uploaded_file_name = thisTransaction.response_dict['project']['uploaded_file_name']
        log.debug("completed uploaded_file_name: " + uploaded_file_name)

        ### generate the processed pdb's content
        
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




def preprocessPdbForAmber(thisTransaction):
    log.info("preprocessPdbForAmber() was called. Still in Development!!!!!!!!" 
    

        
    
