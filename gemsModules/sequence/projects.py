#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid, pathlib
from datetime import datetime
from typing import *
import gmml
import traceback
import gemsModules.common.utils
from gemsModules.project import projectUtilPydantic as projectUtils
from gemsModules.common import logic as commonlogic
from gemsModules.common.loggingConfig import *
from gemsModules.sequence import jsoninterface as sequenceio
from gemsModules.sequence import structureInfo

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

def addResponse(buildState : sequenceio.Single3DStructureBuildDetails, thisTransaction : sequenceio.Transaction, conformerID : str, conformerLabel : str):        
    log.info("addResponse() was called.")
    # By the time build3DStructure() is called, evaluation response exists.
    #  all we need to do is build the output and append it.
    thisSequence = thisTransaction.transaction_out.entity
    thisProject = thisTransaction.transaction_out.project
    thisBuildOutput = sequenceio.Single3DStructureBuildDetails()
    thisBuildOutput.conformerID=conformerID
    thisBuildOutput.conformerLabel=conformerLabel
    try:
        thisBuildOutput.payload = projectUtils.getProjectpUUID(thisProject)
        thisBuildOutput.incomingSequence = thisTransaction.getInputSequencePayload()
    except Exception as error:
        log.error("Problem finding the project pUUID or sequence in the transaction: " + str(error))
        log.error(traceback.format_exc())
        raise error

    thisBuildOutput.indexOrderedSequence = thisTransaction.getSequenceVariantOut('indexOrdered')
    thisBuildOutput.seqID = projectUtils.getSeqIdForSequence(thisBuildOutput.indexOrderedSequence)
    return thisBuildOutput
    

def registerBuild(buildState : sequenceio.Single3DStructureBuildDetails, thisTransaction : sequenceio.Transaction):
    log.debug("registerBuild() was called.")
    try:
        ##TODO: get the path for structureInfo.json
        structureInfoFilename = structureInfo.getStructureInfoFilename(thisTransaction)
        log.debug("structureInfoFilename:" + str(structureInfoFilename))
    except Exception as error:
        log.error("There was a problem getting the path for structureInfo.json: " + str(error))
        log.error(traceback.format_exc())
        raise error

    try:
        ##TODO: get the path for structureInfo_status.json 
        statusFilename = structureInfo.getStatusFilename(thisTransaction)
        log.debug("statusFilename:" + str(statusFilename))
    except Exception as error:
        log.error("There was a problem getting the status filename: " + str(error))
        log.error(traceback.format_exc())
        raise error



##  @brief Return true if this structure has been built previously, otherwise false.
#   @oaram
#   @return
def structureExists(buildState: sequenceio.Single3DStructureBuildDetails, thisTransaction : sequenceio.Transaction, buildStrategyID : str):
    log.info("structureExists() was called.")
    if not sequenceExists(buildState, thisTransaction):
        log.debug("Sequence has never been built before; a new sequence is born!")
        return False
    else:
        log.debug("Sequence has previous builds. Checking for the requested buildState.")
        indexOrderedSequence = thisTransaction.getSequenceVariantOut('indexOrdered')
        thisProject = thisTransaction.getProjectOut()
        if thisProject is None :
            message="The outgoing project is None so cannot determine the filesystem path."
            log.error(message)
            thisTransaction.generateCommonParserNotice(
                    noticeBrief='GemsError',
                    additionalInfo = { 'hint' : message }
                    )
            return
        thisSequence = thisTransaction.transaction_out.entity
        if thisSequence is None :
            message="The Entity (sequence) is None so cannot determine if structure exists."
            log.error(message)
            thisTransaction.generateCommonParserNotice(
                    noticeBrief='GemsError',
                    additionalInfo = { 'hint' : message }
                    )
            return
      
        servicePath = os.path.join(thisProject.getFilesystemPath(), thisProject.getEntityId(), thisProject.getServiceId())
        sequencePath = os.path.join(servicePath, "Sequences")
        seqID = projectUtils.getSeqIdForSequence(indexOrderedSequence)
        sequenceDir = os.path.join(sequencePath , seqID , thisSequence.outputs.getBuildStrategyID())
        log.debug("sequenceDir: " + sequenceDir)
        log.debug("buildState.conformerLabel: " + buildState.conformerLabel)
        structureLinkInSequenceDir = os.path.join(sequenceDir , "All_Builds" , buildState.structureDirectoryName)
        log.debug("structureLinkInSequenceDir: " + structureLinkInSequenceDir)
        if os.path.isdir(structureLinkInSequenceDir):
            log.debug("The requested structure directory exists (" + buildState.structureDirectoryName + ") already exists.")
            log.debug("checking for output file: " + structureLinkInSequenceDir + "/build-status.log).")
            if os.path.isfile(structureLinkInSequenceDir + "/build-status.log"): 
                return True
            else :
                return False
        else:
            log.debug("The requested structure (" + buildState.structureDirectoryName + ") doesn't exist.")
            return False
            ## Need to write a buildStateExists() method that compares Single3DStructureBuildDetails that have
            ##  been logged to file to requested Single3DStructureBuildDetails.
            ## Oliver: Not sure what this comment wants exactly, or if what I have done covers it.


##  @brief Return true if this sequence has been built previously, otherwise false.
#   @oaram
#   @return
def sequenceExists(buildState: sequenceio.Single3DStructureBuildDetails, thisTransaction : sequenceio.Transaction):
    log.info("sequenceExists() was called.")
    try:
        sequence = thisTransaction.getSequenceVariantOut('indexOrdered')
    except Exception as error:
        log.error("There was a problem getting the sequence from structureInfo: " + str(error))
        log.error(traceback.format_exc())
        raise error
    ## Check if this sequence has been built before.
    ## Can we assume that seqID has already been initialized and saved?
    log.debug("Checking for previous builds of this sequence: " + sequence)
    thisProject = thisTransaction.getProjectOut()
    if thisProject is None :
        message="The outgoing project is None so cannot determine the filesystem path."
        log.error(message)
        thisTransaction.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo = { 'hint' : message }
                )
        return
    thisSequence = thisTransaction.transaction_out.entity
    if thisSequence is None :
        message="The Entity (sequence) is None so cannot determine if sequence exists."
        log.error(message)
        thisTransaction.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo = { 'hint' : message }
                )
        return

    servicePath = os.path.join(thisProject.getFilesystemPath(), thisProject.getEntityId(), thisProject.getServiceId())
    log.debug("servicePath is : " + servicePath)
    log.debug("servicePath is made from these things: " )
    log.debug("filesystem path:  " + thisProject.getFilesystemPath())
    log.debug("entity id:  " + thisProject.getEntityId())
    log.debug("service id : " + thisProject.getServiceId())
    sequencePath = os.path.join(servicePath, "Sequences")
    log.debug("sequencePath is : " + sequencePath)
    seqID = projectUtils.getSeqIdForSequence(sequence)
    log.debug("seqID is : " + seqID)
    # I think this is correct (Lachele)
    sequenceDir = os.path.join(sequencePath , seqID , thisSequence.outputs.getBuildStrategyID())
    # it used to say this
    # sequenceDir = sequencePath + seqID
    log.debug("sequenceDir is :   " + sequenceDir)
    if os.path.isdir(sequenceDir):
        log.debug("This sequence has previous builds.")
        return True
    else:
        log.debug("No directory exists for this sequence, there cannot be any previous builds.")
        return False


## TODO: make all these directory/link/file making functions into one thing
## that gets called by string only
def createConformerDirectoryInBuildsDirectory(
        projectDir : str, 
        conformerDirName : str ,
        separator : str = 'New_Builds' ) :
    log.info("createConformerDirectoryInBuildsDirectory() was called.")
    log.debug("projectDir: " + projectDir)
    log.debug("conformerDirName: " + conformerDirName)
    conformerDirPath = os.path.join( projectDir , separator , conformerDirName )
    if os.path.isdir(conformerDirPath) :
        return
    try:
        log.debug("Trying to create conformerDirPath: " + conformerDirPath)
        os.makedirs(conformerDirPath)
    except Exception as error:
        log.error("Could not create conformerDirPath: " + conformerDirPath)
        log.error(traceback.format_exc())
        raise error

# Creates a symlink in Requested_Builds into either Existing_Builds or New_Builds
def createSymLinkInRequestedStructures(projectDir : str, buildDir : str, conformerID : str):
    log.info("createSymLinkInRequestedStructures() was called.")
    try:
        os.makedirs(projectDir + "/Requested_Builds/", exist_ok = True)
        path_down_to_source = buildDir + "/" + conformerID # Can be New_Builds/conformerID or Existing_Builds/conformerID
        path_down_to_dest_dir = "Requested_Builds/" 
        commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, conformerID, projectDir)
    except Exception as error:
        log.error("Could not create link in Builds/projectID/Requested_Builds/: " + str(error))
        log.error(traceback.format_exc())
        raise error


def addSequenceFolderSymLinkToNewBuild(servicePath:str, sequenceID:str, buildStrategyID:str, projectID:str, conformerID:str):
    log.info("addSequenceFolderSymLinkForConformer() was called.")
    # Add a symlink from Sequences/sequenceID/buildStrategyID/All_Builds/conformerID
    #                 to Builds/projectID/New_Builds/conformerID
    # Don't want to call this function for Existing_Builds, as they should already be linked from All_Builds.
    path_down_to_source = 'Builds/' + projectID + "/New_Builds/" + conformerID
    path_down_to_dest_dir = 'Sequences/' + sequenceID + '/' + buildStrategyID + '/All_Builds/'
    log.debug("Creating symlink with toolPath " + servicePath + " called " + conformerID + " from " + path_down_to_dest_dir + " pointing to " + path_down_to_source)
    commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, conformerID, servicePath)


def addBuildFolderSymLinkToExistingConformer(servicePath:str, sequenceID:str, buildStrategyID:str, projectID:str, conformerID:str):
    log.info("addBuildFolderSymLinkForExistingConformer() was called.")
    sequencePath = os.path.join(servicePath, "/Sequences/")
    path_down_to_dest_dir = os.path.join( 'Builds' , projectID , 'Existing_Builds')
    path_down_to_source = os.path.join( 'Sequences' , sequenceID , buildStrategyID , 'All_Builds' , conformerID )
    log.debug("Creating symlink in " + servicePath + " between " + path_down_to_dest_dir + " called " + conformerID + " to " + path_down_to_source)
    commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, conformerID, servicePath)



##  @brief  Creates the directories and files needed to store a file that can be
#           reused via symlink.
#   @detail Still being worked on, but works for default structures.
#   @param  Transaction
def setupInitialSequenceFolders(servicePath:str, sequenceID:str, projectID:str, buildStrategyID:str):
    log.info("setupInitialSequenceFolders() was called.")
    ## Some of the folders in Sequence may already exist via a previous project, those in Builds should not.
    log.debug("Here are the inputs: ")
    log.debug("servicePath:str : " + servicePath)
    log.debug("sequenceID:str : " + sequenceID)
    log.debug("projectID:str : " + projectID)
    log.debug("buildStrategyID:str : "  + buildStrategyID)
    sequencePath = os.path.join(servicePath , "Sequences")
    seqIDPath = os.path.join(sequencePath , sequenceID)
    buildPath = os.path.join(servicePath , "Builds")
    projIDPath = os.path.join(buildPath , projectID)
    buildStrategyPath = os.path.join(seqIDPath , buildStrategyID)
    log.debug("sequencePath : " + sequencePath )
    log.debug("seqIDPath : " + seqIDPath  )
    log.debug("buildPath : " + buildPath  )
    log.debug("projIDPath : " + projIDPath  )
    log.debug("buildStrategyPath : " + buildStrategyPath  )
    if not os.path.isdir(buildStrategyPath): 
        try:
            log.debug("buildStrategyPath was not found, so trying to create it.")
            log.debug("buildStrategyPatth is : " + str(buildStrategyPath))
            pathlib.Path(buildStrategyPath).mkdir(parents=True)
            log.debug("The path now exists? ")
            log.debug(os.path.isdir(buildStrategyPath))
            path_down_to_dest_dir = None # Same level as parent directory (seqIDPath)
            log.debug("seqIDPath is : " + seqIDPath + " ... and does it exist? ")
            log.debug(os.path.isdir(seqIDPath))
            commonlogic.make_relative_symbolic_link(buildStrategyPath, None, 'current', seqIDPath)
        except Exception as error:
            log.error("There was a problem creating buildStrategyPath: " + str(error))
            log.error(traceback.format_exc())
            raise error

    all_builds = seqIDPath + '/' + buildStrategyID + '/All_Builds/'
    if not os.path.isdir(all_builds):
        try:
            os.makedirs(all_builds)
        except Exception as error:
            log.error("There was a problem creating all_builds: " + str(error))
            log.error(traceback.format_exc())
            raise error
    # Just make everything you might need here.
    try:
        requestedBuildsPath = os.path.join(projIDPath , 'Requested_Builds')
        existingBuildsPath = os.path.join(projIDPath , 'Existing_Builds')
        newBuildsPath = os.path.join(projIDPath , 'New_Builds')
        newBuildsLogsPath = os.path.join(projIDPath , 'New_Builds' , 'logs')
        existingBuildsLogsPath = os.path.join(projIDPath , 'Existing_Builds' , 'logs')
        log.debug("Making these paths : " )
        log.debug("requestedBuildsPath : " + requestedBuildsPath )
        log.debug("existingBuildsPath : " + existingBuildsPath )
        log.debug("newBuildsPath : " + newBuildsPath )
        log.debug("newBuildsLogsPath : " + newBuildsLogsPath )
        log.debug("existingBuildsLogsPath :"  + existingBuildsLogsPath )
        pathlib.Path(requestedBuildsPath).mkdir(parents=True, exist_ok = True)
        pathlib.Path(existingBuildsPath).mkdir(parents=True,  exist_ok = True)
        pathlib.Path(newBuildsPath).mkdir(parents=True, exist_ok = True)
        pathlib.Path(newBuildsLogsPath).mkdir(parents=True, exist_ok = True)
        pathlib.Path(existingBuildsLogsPath).mkdir(parents=True, exist_ok = True)
    except Exception as error:
        log.error("There was a problem making folders or logs in Builds " + str(error))
        log.error(traceback.format_exc())
        raise error

    # Assumes start_project was called before now, so project folder exists in Builds/
    # OG not sure what the Sequence_Repository link be used for, but the plan requires it.
    try:
        path_to_source = 'Sequences/'+ sequenceID
        path_to_dest_dir = 'Builds/' + projectID 
        log.debug("About to make a relative symbolib link.  Here are the arguments : " )
        log.debug("path_to_source : " + path_to_source)
        log.debug("path_to_dest_dir : " + path_to_dest_dir)
        log.debug("servicePath : " + str(servicePath))
        commonlogic.make_relative_symbolic_link(
                path_down_to_source = path_to_source, 
                path_down_to_dest_dir = path_to_dest_dir , 
                dest_link_label = "Sequence_Repository", 
                parent_directory  = servicePath)
    except Exception as error:
        #log.error("There was a problem making Sequence_Repository link " + str(error))
        log.error("There was a problem making Sequence_Repository link " )
        log.error(traceback.format_exc())
        raise error    
    

def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

