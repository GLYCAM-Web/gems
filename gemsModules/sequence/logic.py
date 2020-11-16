#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import gemsModules
import gmml
import traceback
import gemsModules.common.utils
from gemsModules.project.projectUtil import *
from gemsModules.project import settings as projectSettings
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.delegator import io as delegatorio
#from gemsModules.common.services import *
#from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from . import settings as sequenceSettings
from gemsModules.sequence import projects as sequenceProjects
from .structureInfo import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  @brief convenience method. pass transaction, get options dict.
##  TODO: evaluate for deprecation. Not terribly useful.
def getOptionsFromTransaction(thisTransaction: Transaction):
    log.info("getOptionsFromTransaction() was called.")
    if "options" in thisTransaction.request_dict.keys():
        log.debug("Found options.")
        return thisTransaction.request_dict['options']
    else:
        log.debug("No options found.")
        return None


##  @brief Logs requests, makes decisions about what to build or reuse, builds a response.
##  @detail This is a bit of a butler method, it looks over the process and calls only what
#       is needed, depending on the request and whether an existing structure fits the request.
def manageSequenceRequest(thisTransaction : Transaction):
    log.info("manageSequenceRequest() was called.")
    ##  Start a project, if needed
    try:
        if sequenceProjects.projectExists(thisTransaction):
            log.debug("Existing project.")
        else:
            startProject(thisTransaction)
    except Exception as error:
        log.error("There was a problem creating a project: " + str(error))
        raise error
    else:
        ##  Build structureInfo object
        try:
            structureInfo = buildStructureInfo(thisTransaction)
            log.debug("structureInfo: " + str(structureInfo))
        except Exception as error:
            log.error("There was a problem building structureInfo: " + str(error))
            raise error
        else:
            ##  Save some copies of structureInfo for status tracking.
            try:
                ## Determine whether to save or update.
                projectDir = getProjectDir(thisTransaction)
                filename = projectDir + "logs/structureInfo_request.json"
                if os.path.exists(filename):
                    log.debug("\n\nstructureInfo_request.json found. Updating both the request and the status file.\n\n")
                    updateStructureInfoWithUserOptions(thisTransaction, structureInfo, filename)
                    statusFile = projectDir + "logs/structureInfo_status.json"
                    if os.path.exists(statusFile):
                        updateStructureInfoWithUserOptions(thisTransaction, structureInfo, statusFile)
                else:   
                    ##Create new files for tracking this project.
                    saveRequestInfo(structureInfo, projectDir)
            except Exception as error:
                log.error("There was a problem saving the request info: " + str(error))
            else:
                ## Each buildState represents a single build request.
                for buildState in structureInfo.buildStates:
                    log.debug("Checking if a structure has been built in this buildState: ")
                    log.debug("buildState: " + repr(buildState))
                    ##  check if requested structures exitst, update structureInfo_status.json and project when exist
                    try:
                        if sequenceProjects.structureExists(buildState, thisTransaction):
                            log.debug("Found an existing structure.")
                            this_pUUID = sequenceProjects.getProjectpUUID(thisTransaction)
                            this_sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
                            this_seqID = getSeqIDForSequence(this_sequence)
                            sequenceProjects.createProjectDirectoryStructure(projectDir)
                            sequenceProjects.createSequenceSymLinks(this_seqID, this_pUUID)
                            sequenceProjects.createProjectSymlinks(projectDir)
                            ##TODO: Make this next method more generic, so it can handle rotamers too.
                            sequenceProjects.respondWithExistingDefaultStructure(thisTransaction)
                            ##TODO: Update the structureInfo_status.json
                        else:
                            log.debug("Need to build this structure.")
                            try: 
                                # old:  sequenceProjects.createProjectDirectoryStructure(buildState, thisTransaction)
                                sequenceProjects.createProjectDirectoryStructure(projectDir)
                                from gemsModules.sequence import build
                                build.build3DStructure(buildState, thisTransaction)
                            except Exception as error:
                                log.error("There was a problem building the 3D structure: " + str(error))
                                log.error(traceback.format_exc())
                                raise error
                            else:
                                try:
                                    this_pUUID = sequenceProjects.getProjectpUUID(thisTransaction)
                                    this_sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
                                    this_seqID = getSeqIDForSequence(this_sequence)
                                    sequenceProjects.createSequenceSymLinks(this_seqID, this_pUUID)
                                    sequenceProjects.createProjectSymlinks(projectDir)
                                except Exception as error:
                                    log.error("There was a problem creating the symbolic links: " + str(error))
                                    raise error
                                else:
                                    try:
                                        #Updates the statuses in various files and the project
                                        sequenceProjects.registerBuild(buildState, thisTransaction)
                                    except Exception as error:
                                        log.error("There was a problem registering this build: " + str(error))
                                        raise error
                                    
                                    ##  create downloadUrl
                                    ##  submit to amber for minimization, 
                                    ##      update structureInfo_status.json again
                                    ##      update project again
                                
                                ##  append response to transaction
                            
                    except Exception as error:
                        log.error("There was a problem checking if the structure exists: " + str(error))
                        raise error




def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

