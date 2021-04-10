#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import gemsModules
import gmml
import traceback
import gemsModules.common.utils
from multiprocessing import Process
from gemsModules.project import projectUtilPydantic as projectUtils
from gemsModules.project import settings as projectSettings
from gemsModules.project import io as projectio
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
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
def getOptionsFromTransaction(thisTransaction: sequenceio.Transaction):
    log.info("getOptionsFromTransaction() was called.")
    if "options" in thisTransaction.request_dict.keys():
        log.debug("Found options.")
        return thisTransaction.request_dict['options']
    else:
        log.debug("No options found.")
        return None

class EverLastingProcess(Process):
    def join(self, *args, **kwargs):
        pass # Overwrites join so that it doesn't block. Otherwise parent waits.

    def __del__(self):
        pass

##  @brief Logs requests, makes decisions about what to build or reuse, builds a response.
##  @detail This is a bit of a butler method, it looks over the process and calls only what
#       is needed, depending on the request and whether an existing structure fits the request.
#def manageSequenceRequest(thisTransaction : sequenceio.Transaction):
#    log.info("manageSequenceRequest() was called.")
#    from gemsModules.sequence import build as sequenceBuild
#    ##  Start a project, if needed
#    try:
#        if sequenceProjects.projectExists(thisTransaction):
#            log.debug("Existing project.")
#        else:
#            log.debug("Starting a new project.")
#            projectUtils.startProject(thisTransaction)
#    except Exception as error:
#        log.error("There was a problem creating a project: " + str(error))
#        log.error(traceback.format_exc())
#        raise error
#
#    ##  Build structureInfo object
#    try:
#        structureInfo = buildStructureInfoOliver(thisTransaction)
#        log.debug("structureInfo: " + str(structureInfo))
#    except Exception as error:
#        log.error("There was a problem building structureInfo: " + str(error))
#        log.error(traceback.format_exc())
#        raise error
#    ##  Save some copies of structureInfo for status tracking.
#    try:
#        ## Determine whether to save or update.
#        projectDir = projectUtils.getProjectDir(thisTransaction)
#        filename = projectDir + "logs/structureInfo_request.json"
#        if os.path.exists(filename):
#            log.debug("\n\nstructureInfo_request.json found. Updating both the request and the status file.\n\n")
#            updateStructureInfoWithUserOptions(thisTransaction, structureInfo, filename)
#            statusFile = projectDir + "logs/structureInfo_status.json"
#            if os.path.exists(statusFile):
#                updateStructureInfoWithUserOptions(thisTransaction, structureInfo, statusFile)
#            else:   
#                ##Create new files for tracking this project.
#                saveRequestInfo(structureInfo, projectDir)
#    except Exception as error:
#        log.error("There was a problem saving the request info: " + str(error))
#        log.error(traceback.format_exc())
#        raise error
#    try:
#        ## Here we need to setup project folder, create some symLinks etc, before we get into each buildState
#        ## Not happy with the organization of this logic. Too much state being passed around and similar code!
#        ## Smells like it should be a class and this stuff goes in the initializer. 
#        this_pUUID = projectUtils.getProjectpUUID(thisTransaction)
#        this_sequence = thisTransaction.getSequenceVariantOut('indexOrdered')
#        this_seqID = projectUtils.getSeqIDForSequence(this_sequence)
#        buildStrategyID = "buildStrategyID1" # TODO implement getCurrentBuildStrategyID().
#        sequenceProjects.setupInitialSequenceFolders(this_seqID, this_pUUID, buildStrategyID)
#        #Can generate the response already:
#        for buildState in structureInfo.buildStates:
#            conformerID = buildState.structureDirectoryName
#            sequenceProjects.addResponse(buildState, thisTransaction, conformerID, buildState.conformerLabel)
#        log.debug("response_dict, after evaluation: ")
#        prettyPrint(thisTransaction.response_dict)
#        ## Regardless if requesting default or not, I think I need to generate a default. Otherwise I get into madness
#        ## with figuring out exist status and which conformerID to use in place of default. Then when a default 
#        ## request does come, should it overwrite previous default for old projects?
#        ## A default request is always first, this is now implemented in buildStructureInfo
#        #sequenceBuild.buildEach3DStructureInStructureInfo(structureInfo, buildStrategyID, thisTransaction, this_seqID, this_pUUID, projectDir)
#        p = EverLastingProcess(target=sequenceBuild.buildEach3DStructureInStructureInfo, args=(structureInfo, buildStrategyID, thisTransaction, this_seqID, this_pUUID, projectDir,), daemon=False)
#        p.start()
#        #sequenceProjects.createDefaultSymLinkBuildsDirectory(projectDir, buildDir + conformerID)
#            ##  create downloadUrl
#            ##  submit to amber for minimization, 
#            ##      update structureInfo_status.json again
#            ##      update project again                    
#            ##  append response to transaction           
#    except Exception as error:
#        log.error("There was a problem managing this sequence request: " + str(error))
#        log.error(traceback.format_exc())
#        raise error


def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

