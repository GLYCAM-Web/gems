#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
from datetime import datetime
#import gemsModules
import gmml
import traceback
import gemsModules.common.utils
from gemsModules.project import projectUtilPydantic as projectUtils
from gemsModules.project import settings as projectSettings
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.common.loggingConfig import *
from gemsModules.sequence import io as sequenceio
from gemsModules.sequence import settings as sequenceSettings
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
    thisBuildOutput.seqID = projectUtils.getSeqIDForSequence(thisBuildOutput.indexOrderedSequence)
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
        userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
        seqID = projectUtils.getSeqIDForSequence(indexOrderedSequence)
        sequenceDir = userDataDir + seqID + "/" + buildStrategyID + "/" 
        log.debug("sequenceDir: " + sequenceDir)
        log.debug("buildState.conformerLabel: " + buildState.conformerLabel)
           
        structureLinkInSequenceDir = sequenceDir + "All_Builds/" + buildState.structureDirectoryName
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
    userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
    seqID = projectUtils.getSeqIDForSequence(sequence)
    sequenceDir = userDataDir + seqID
    log.debug("sequenceExists sequenceDir: " + sequenceDir)
    if os.path.isdir(sequenceDir):
        log.debug("This sequence has previous builds.")
        return True
    else:
        log.debug("No directory exists for this sequence, there cannot be any previous builds.")
        return False



# ##  I believe the following is no longer used - Lachele
# ##  @ brief Pass in a gemsProject and get a responseConfig.
# #   @ param GemsProject gemsProject
# #   @ return dict config
# def build3dStructureResponseConfig(thisTransaction : sequenceio.Transaction):
    #log.info("build3dStructureResponseConfig() was called.\n")
    #gemsProject = thisTransaction.response_dict['gems_project']
    #indexOrdered = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
    #seqID = getSeqIDForSequence(indexOrdered)
    #downloadUrl = getDownloadUrl(gemsProject['pUUID'], "cb")
    #sequence = gemsProject['sequence']
    #config = {
        #"sequence" : sequence,
        #"validateOnly" : False,
        #"outputType" : "Build3DStructure",
        #"payload" : gemsProject['pUUID'],
        #"seqID" : seqID,
        #"downloadUrl" : downloadUrl
#
    #}
#
    

    log.debug("returning 3dStructureResponseConfig: " + str(config))

    return config


## TODO: make all these directory/link/file making functions into one thing
## that gets called by string only


def createConformerDirectoryInBuildsDirectory(projectDir : str, conformerDirName : str):
    log.info("createConformerDirectoryInBuildsDirectory() was called.")
    log.debug("projectDir: " + projectDir)
    log.debug("conformerDirName: " + conformerDirName)
    conformerDirPath = (projectDir + "/New_Builds/" + conformerDirName + '/')
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

# Create default symlinks. Works for either existing/new conformer/default.
# outputDir can be Existing_Builds/ or New_Builds/ followed by a conformerID or "default"
def createDefaultSymLinkBuildsDirectory(projectDir : str, outputDir : str):
    log.info("createDefaultSymLinkBuildsDirectory() was called")
    try:
        log.debug("projectDir: " + projectDir)
        log.debug("outputDir: " + outputDir)
        parent_dir = projectDir
        path_down_to_source = outputDir
        path_down_to_dest_dir = None

        commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, "defaultFolder", parent_dir)
        path_down_to_source = "defaultFolder/mol_min.pdb"
        commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, "default.pdb", parent_dir)
        path_down_to_source = "defaultFolder/structure.pdb"
        commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, "default_unminimized.pdb", parent_dir)
    except Exception as error:
        log.error("Cound not create default symlinks in Builds/" + str(error))
        log.error(traceback.format_exc())
        raise error


def addSequenceFolderSymLinkToNewBuild(sequenceID:str, buildStrategyID:str, projectID:str, conformerID:str):
    log.info("addSequenceFolderSymLinkForConformer() was called.")
    # Add a symlink from Sequences/sequenceID/buildStrategyID/All_Builds/conformerID
    #                 to Builds/projectID/New_Builds/conformerID
    # Don't want to call this function for Existing_Builds, as they should already be linked from All_Builds.
    parent_dir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"
    # sequencePath = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
    # seqIDPath = sequencePath + sequenceID
    path_down_to_source = 'Builds/' + projectID + "/New_Builds/" + conformerID
    path_down_to_dest_dir = 'Sequences/' + sequenceID + '/' + buildStrategyID + '/All_Builds/'
    log.debug("Creating symlink with parentDir " + parent_dir + " called " + conformerID + " from " + path_down_to_dest_dir + " pointing to " + path_down_to_source)
# make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, dest_link_label, parent_directory)
    commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, conformerID, parent_dir)


def addBuildFolderSymLinkToExistingConformer(sequenceID:str, buildStrategyID:str, projectID:str, conformerID:str):
    log.info("addBuildFolderSymLinkForExistingConformer() was called.")
    parent_dir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"
    path_down_to_dest_dir = 'Builds/' + projectID + '/Existing_Builds/'
    path_down_to_source = 'Sequences/' + sequenceID + '/' + buildStrategyID + '/All_Builds/' + conformerID
    log.debug("Creating symlink in " + parent_dir + " between " + path_down_to_dest_dir + " called " + conformerID + " to " + path_down_to_source)
    commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, conformerID, parent_dir)



##  @brief  Creates the directories and files needed to store a file that can be
#           reused via symlink.
#   @detail Still being worked on, but works for default structures.
#   @param  Transaction
def setupInitialSequenceFolders(sequenceID:str, projectID:str, buildStrategyID:str):
    log.info("setupInitialSequenceFolders() was called.")
    ## Some of the folders in Sequence may already exist via a previous project, those in Builds should not.
    ## userDataDir is the top level dir that holds the repository of all sequences
    log.debug(projectSettings.output_data_dir)
    sequencePath = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
    seqIDPath = sequencePath + sequenceID
    projectPath = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Builds/"
    projIDPath = projectPath + projectID
    parent_dir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"    
    buildStrategyPath = seqIDPath + '/' + buildStrategyID + '/'
    if not os.path.isdir(buildStrategyPath):
        try:
            os.makedirs(buildStrategyPath)
            path_down_to_dest_dir = None # Same level as parent directory (seqIDPath)
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

        os.makedirs(projIDPath + '/Requested_Builds', exist_ok = True)
        os.makedirs(projIDPath + '/Existing_Builds',  exist_ok = True)
        os.makedirs(projIDPath + '/New_Builds', exist_ok = True)
        os.makedirs(projIDPath + '/New_Builds/' + 'logs/', exist_ok = True)
        os.makedirs(projIDPath + '/Existing_Builds/' + 'logs/', exist_ok = True)
    except Exception as error:
        log.error("There was a problem making folders or logs in Builds " + str(error))
        log.error(traceback.format_exc())
        raise error

    # Assumes start_project was called before now, so project folder exists in Builds/
    # OG not sure what the Sequence_Repository link be used for, but the plan requires it.
    try:
        path_down_to_source = 'Sequences/'+ sequenceID
        path_down_to_dest_dir = 'Builds/' + projectID 
        commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir , 'Sequence_Repository', parent_dir)
    except Exception as error:
        log.error("There was a problem making Sequence_Repository link " + str(error))
        log.error(traceback.format_exc())
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
def getProjectSubdir(thisTransaction: sequenceio.Transaction):
    log.info("getProjectSubdir() was called.")
    project_dir = thisTransaction.response_dict['gems_project']['project_dir']
    log.debug("project_subdir: " + project_dir)

    ## If default structure, subdir name is 'structure'
    if checkIfDefaultStructureRequest(thisTransaction):
        return project_dir 
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
        sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
    except Exception as error:
        log.error("There was a problem getting the sequence from the transaction: "  + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        seqID = getSeqIDForSequence(sequence)
        userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
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
            log.error(traceback.format_exc())
            raise error
        else:
            return structureExists



def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

