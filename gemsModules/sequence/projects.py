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

from datetime import datetime
from .structureInfo import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)



def projectExists(thisTransaction : Transaction):
    log.info("projectExists() was called.")
    try:
        projectDir = getProjectDir(thisTransaction)
        log.debug("projectDir: " + projectDir)
    except Exception as error:
        log.error("There was a problem getting the projectDir: " + str(error))
        raise error
    else:
        if os.path.exists(projectDir):
            log.debug("Found an existing project dir.")
            return True
        else:
            log.debug("No projectDir found.")
            return False









def registerBuild(buildState : BuildState, thisTransaction : Transaction):
    log.debug("registerBuild() was called.")
    try:
        ##TODO: get the path for structureInfo.json
        structureInfoFilename = getStructureInfoFilename(thisTransaction)
        log.debug("structureInfoFilename:" + str(structureInfoFilename))
    except Exception as error:
        log.error("There was a problem getting the path for structureInfo.json: " + str(error))
    else:
        try:
            ##TODO: get the path for structureInfo_status.json 
            statusFilename = getStatusFilename(thisTransaction)
            log.debug("statusFilename:" + str(statusFilename))
        except Exception as error:
            log.error("There was a problem getting the status filename: " + str(error))
            raise error
        else:
            try:
                updateBuildStatus(structureInfoFilename, buildState, "submitted")
            except Exception as error:
                log.error("There was a problem updating the structureInfo.json: " + str(error))
                raise error
            else:
                try:
                    updateBuildStatus(statusFilename, buildState, "submitted")
                except Exception as error:
                    log.error("There was a problem updating the status file: " + str(error))
                    raise error



##  @brief Return true if this structure has been built previously, otherwise false.
#   @oaram
#   @return
def structureExists(buildState: BuildState, thisTransaction : Transaction):
    log.info("structureExists() was called.")

    structureExists = False
    try:
        sequence = getSequenceFromTransaction(thisTransaction)
        log.debug("Checking for previous builds of this sequence: \n" + sequence)
    except Exception as error:
        log.error("There was a problem getting the sequence from structureInfo: " + str(error))
        raise error
    else:
        ## Check if this sequence has been built before.
        userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"
        seqID = getSeqIDForSequence(sequence)
        sequenceDir = userDataDir + seqID

        log.debug("sequenceDir: " + sequenceDir)
        if os.path.isdir(sequenceDir):
            log.debug("This sequence has previous builds.")
            structureLabel = buildState.structureLabel
            if structureLabel == "default":
                ## Easy. Just check the path. If it exists, return true.
                defaultBuildDir = sequenceDir + "/default/"
                if os.path.isdir(defaultBuildDir):
                    log.debug("default structure found.")
                    return True
                else:
                    log.debug("default structure not found.")
                    return False
            else:
###
### START HERE -- add this logic
###
                log.error("Need to write the logic that checks for existing builds that are not the defaults.")
                ## Need to write a buildStateExists() method that compares BuildStates that have
                ##  been logged to file to requested BuildStates.
        else:
            log.debug("No directory exists for this sequence, there cannot be any previous builds.")
            return False




##TODO Make this work for structures that are not the default.
##  @brief Call this if the default structure for a sequence already exists.
#   @detail Builds a project and a response config object. Updates the transaction.
#   @param Transaction
def respondWithExistingDefaultStructure(thisTransaction: Transaction):
    log.info("respondWithExistingDefaultStructure() was called.")

    try:
        sequence = getSequenceFromTransaction(thisTransaction)
    except Exception as error:
        log.error("There was a problem getting the sequence from the request: " + str(error))
        raise error
    else:
        try:
            seqID = getSeqIDForSequence(sequence)
        except Exception as error:
            log.error("There was a problem getting the seqID for this sequence: " + str(error))
            raise error
        else:
            try:
                ##Grab the projectId from the gemsProject.
                projID = getProjectpUUID(thisTransaction)
            except Exception as error:
                log.error("There was a problem getting the pUUID from the GemsProject: " + str(error))
                raise error
            else:
                config = {
                    "entity":"Sequence",
                    "respondingService":"Build3DStructure",
                    "responses": [{
                        'payload': projID,
                        'download' : getDownloadUrl(seqID, "cb"),
                        'seqID' : seqID
                    }]
                }
                appendResponse(thisTransaction, config)



## TODO: Rewrite this to a smaller scope: symlinks, and folder creation 

##  @brief  Creates the directories and files needed to store a file that can be
#           reused via symlink.
#   @detail Still being worked on, but works for default structures.
#   @param  Transaction
def createSymLinks(buildState : BuildState, thisTransaction : Transaction):
    log.info("createSymLinks() was called.")

    sequence = getSequenceFromTransaction(thisTransaction)
    seqID = getSeqIDForSequence(sequence)

    ## userDataDir is the top level dir that holds all projects, not a specific user's data.
    userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"
    seqIDPath = userDataDir + seqID
    
    log.debug("Checking to see if the seqIDPath already exists for this sequence: " + seqIDPath)
    if not os.path.exists(seqIDPath):
        log.debug("seqIDPath does not exist. Creating it now.")
        try:
            os.makedirs(seqIDPath)
        except Exception as error:
            log.error("There was a problem creating the seqIDPath: " + str(error))
            raise error
        else:
            try:
                createSeqLog(sequence, seqIDPath)
            except Exception as error:
                log.error("There was a problem creating the SeqLog: " + str(error))
                raise error
            else:
                projectDir = getProjectDir(thisTransaction)
                try:
                    isDefault = checkIfDefaultStructureRequest(thisTransaction)
                    log.debug("isDefault: " + str(isDefault))
                    if isDefault:
                        link = seqIDPath + "/default"
                        projectDir = projectDir + "default"
                    else:
                        link = seqIDPath + "/" + buildState.structureLabel
                    
                    if os.path.exists(projectDir):
                        target = projectDir
                        ##What is being linked to is the projecDir or the 
                        log.debug("target: " + target)
                        ##This will be the symbolic link
                        log.debug("link: " + link)
                        os.symlink(target, link)
                    else:
                        log.error("Failed to find the target dir for the symbolic link.")
                        raise FileNotFoundError(projectDir)
                    
                except Exception as error:
                    log.error("There was a problem creating the symbolic link.")
                    raise error
            
                



##  @brief Looks at a transaction to determine if the user is requesting the default structure
#   @param Transaction thisTransaction
#   @return Boolean isDefault
def checkIfDefaultStructureRequest(thisTransaction):
    log.info("checkIfDefaultStructureRequest was called().")
    from gemsModules.sequence import logic
    options  = logic.getOptionsFromTransaction(thisTransaction)
    log.debug("options: " + str(options))

    if options == None:
        log.debug("No options found, returning true.")
        return True
    else:
        log.debug("options.keys(): " + str(options.keys()))
        ## The presense of rotamers in options means this is not a request
        # for the default structure.
        if "geometryOptions" in options.keys():
            log.debug("geometryOptions found, returning False.")
            return False
        else:
            log.debug("No geometryOptions found, returning True.")
            return True


##  @brief gets the path of the default dir for a project. 
##  @TODO: Evaluate if this is necessary. Possibly deprecate this. 
def getProjectSubdir(thisTransaction: Transaction):
    log.info("getProjectSubdir() was called.")
    project_dir = thisTransaction.response_dict['gems_project']['project_dir']
    log.debug("project_dir: " + project_dir)

    ## If default structure, subdir name is 'default'
    if checkIfDefaultStructureRequest(thisTransaction):
        project_dir = project_dir + "default/"
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

    else:
        log.error("Still writing the logic to handle builds with selectedRotamers.")
        ##TODO: provide the subdir based on this doc: 
        ## http://128.192.9.183/eln/gwscratch/2020/01/10/succinct-rotamer-set-labeling-for-sequences/
        raise AttributeError("rotamerSubdir")
    return project_dir 


##  @brief Looks up the sequence and generates an seqID, then checks for existing builds.
#   @param Transaction thisTransaction
#   @return Boolean structureExists
def checkIfDefaultStructureExists(thisTransaction):
    log.info("checkIfDefaultStructureExists() was called.")
    structureExists = False
    try:
        sequence = getSequenceFromTransaction(thisTransaction)
    except Exception as error:
        log.error("There was a problem getting the sequence from the transaction: "  + str(error))
        raise error
    else:
        seqID = getSeqIDForSequence(sequence)
        userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"
        log.debug("userDataDir: " + userDataDir)
        options = getOptionsFromTransaction(thisTransaction)
        try:
            log.debug("Walking the userDataDir.")

            for element in os.walk(userDataDir):
                rootPath = element[0]
                dirNames = element[1]
                fileNames = element[2]

                log.debug("rootPath: " + str(rootPath))
                log.debug("dirNames: " + str(dirNames))
                log.debug("fileNames: " + str(fileNames))
                for dirName in dirNames:
                    log.debug("dirName: " + dirName)
                    log.debug("seqID: " + seqID)
                    if seqID == dirName:
                        return True
                        
        except Exception as error:
            log.error("There was a problem checking if this structure exists.")
            raise error
        else:
            return structureExists



def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

