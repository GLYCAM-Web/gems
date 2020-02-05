import os, sys, importlib.util
import gemsModules
from gemsModules.common.services import *
from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *
import gemsModules.mmservice.settings as mmSettings
import traceback

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.DEBUG

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

def amberProcessPDB(thisTransaction):
    log.info("amberProcessPDB() was called.")
    ## Check the files, if not happy with the file type return error.
    requestDict = thisTransaction.request_dict
    log.debug("requestDict: " + str(requestDict))

    entity = requestDict['entity']['type']
    log.debug("entity: " + entity)

    if "project" in requestDict.keys():
        project = requestDict['project']

        if "uploaded_file_name" in project.keys():
            uploadFileName = project['uploaded_file_name']
            log.debug("uploadFileName: " + uploadFileName)
        else:
            log.error("No uploaded_file_name found in project.")

        if "upload_path" in project.keys():
            uploadPath = project['upload_path']
            log.debug("uploadPath: " + uploadPath)
            uploadFileName = uploadPath + uploadFileName
            log.debug("Updated uploadFileName: " + uploadFileName)
        else:
            log.error("No upload_path found in project.")

        if os.path.exists(uploadFileName):
            log.debug("Found the upload file")
            if uploadFileName.endswith(".pdb"):
                log.debug("File extension agrees this is a pdb file.")
                startProject(thisTransaction)
            else:
                log.error("File extension is not '.pdb' not sure what to do.")
                ##TODO: Add logic to validate pdb file type if no extension exists.
        else:
            log.error("Upload file could not be found.")
    else:
        log.error("No project found in request.")


    ## If file is valid type, start a project.
    ## Proect app will copy upload files into project dir:
    ## pUUID/Uploads/uUUID/

    ##Need to reverse engineer some tendrils to see what happens next.


def doDefaultService(thisTransaction):
    log.info("doDefaultService() was called.")
    ##Preprocess PDB will be the default
    amberProcessPDB(thisTransaction)
