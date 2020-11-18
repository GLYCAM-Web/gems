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
    from gemsModules.sequence import build as sequenceBuild
    ##  Start a project, if needed
    try:
        if sequenceProjects.projectExists(thisTransaction):
            log.debug("Existing project.")
        else:
            startProject(thisTransaction)
    except Exception as error:
        log.error("There was a problem creating a project: " + str(error))
        raise error
    ##  Build structureInfo object
    try:
        structureInfo = buildStructureInfoOliver(thisTransaction)
        log.debug("structureInfo: " + str(structureInfo))
    except Exception as error:
        log.error("There was a problem building structureInfo: " + str(error))
        raise error
    ##  Save some copies of structureInfo for status tracking.
    try:
        ## Determine whether to save or update.
        projectDir = getProjectDir(thisTransaction)
        filename = projectDir + "logs/structureInfo_request.json"
        if os.path.exists(filename):
            log.debug("\n\nstructureInfo_request.json found. Updating both the request and the status file.\n\n")
            updateStructureInfotWithUserOptions(thisTransaction, structureInfo, filename)
            statusFile = projectDir + "logs/structureInfo_status.json"
            if os.path.exists(statusFile):
                updateStructureInfotWithUserOptions(thisTransaction, structureInfo, statusFile)
            else:   
                ##Create new files for tracking this project.
                saveRequestInfo(structureInfo, projectDir)
    except Exception as error:
        log.error("There was a problem saving the request info: " + str(error))
        raise error
    try:
        ## Here we need to setup project folder, create some symLinks etc, before we get into each buildState
        ## Not happy with the organization of this logic. Too much state being passed around and similar code!
        ## Smells like it should be a class and this stuff goes in the initializer. 
        this_pUUID = sequenceProjects.getProjectpUUID(thisTransaction)
        this_sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
        this_seqID = getSeqIDForSequence(this_sequence)
        buildStrategyID = "buildStrategyID1" # TODO implement getCurrentBuildStrategyID().
        sequenceProjects.setupInitialSequenceFolders(this_seqID, this_pUUID, buildStrategyID)

        ## Regardless if requesting default or not, I think I need to generate a default. Otherwise I get into madness
        ## with figuring out exist status and which conformerID to use in place of default. Then when a default 
        ## request does come, should it overwrite previous default for old projects?
        ## A default request is always first, this is now implemented in buildStructureInfo
        for buildState in structureInfo.buildStates:
            log.debug("Checking if a structure has been built in this buildState: ")
            log.debug("buildState: " + repr(buildState))
            conformerID = buildState.structureDirectoryName # May return "default" or a conformerID
            ##  check if requested structures exitst, update structureInfo_status.json and project when exist
            if sequenceProjects.structureExists(buildState, thisTransaction, buildStrategyID):
                ## Nothing in Sequence/ needs to change. In Builds/ProjectID/
                ## add symLink in Existing to Sequences/SequenceID/defaults/All_builds/conformerID.
                log.debug("Found an existing structure.")
                buildDir = "Existing_Builds/"
                sequenceProjects.addBuildFolderSymLinkToExistingConformer(this_seqID, buildStrategyID, this_pUUID, conformerID)
            else: # Doesn't already exist.
                log.debug("Need to build this structure.")
                buildDir = "New_Builds/"
                sequenceProjects.createConformerDirectoryInBuildsDirectory(projectDir, conformerID)
                sequenceBuild.build3DStructure(buildState, thisTransaction, projectDir + buildDir + conformerID)
                sequenceProjects.addSequenceFolderSymLinkToNewBuild(this_seqID, buildStrategyID, this_pUUID, conformerID)
                if conformerID == "default": # And doesn't already exist.
                    sequenceProjects.createDefaultSymLinkSequencesDirectory(this_seqID, conformerID, buildStrategyID)
            # buildDir is either New_Builds/ or Existing_Builds/
            sequenceProjects.createSymLinkInRequestedStructures(projectDir, buildDir, conformerID)
            sequenceProjects.addResponse(buildState, thisTransaction, projectDir + buildDir + conformerID)
            # This probably needs work    
            sequenceProjects.registerBuild(buildState, thisTransaction)


        #sequenceProjects.createDefaultSymLinkBuildsDirectory(projectDir, buildDir + conformerID)
            ##  create downloadUrl
            ##  submit to amber for minimization, 
            ##      update structureInfo_status.json again
            ##      update project again                    
            ##  append response to transaction           
    except Exception as error:
        log.error("There was a problem managing this sequence request: " + str(error))
        raise error


def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

