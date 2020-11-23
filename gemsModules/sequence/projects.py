#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import gemsModules
import gmml
import traceback
import gemsModules.common.utils
from gemsModules.project.projectUtil import *
from gemsModules.project import settings as projectSettings
from gemsModules.common import io as commonio
from gemsModules.sequence import io as sequence_io
from gemsModules.common import logic as commonlogic
from gemsModules.delegator import io as delegatorio

from gemsModules.common.loggingConfig import *
from . import settings as sequenceSettings

from datetime import datetime
from .structureInfo import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##  If a project has been created, there are clues in the transaction, Checking for the 
##  project dir in the filesystem is ideal.
##
def projectExists(thisTransaction : Transaction):
    log.info("projectExists() was called.")

    projectDir = getProjectDir(thisTransaction)
    log.debug("projectDir: " + projectDir)
    
    if os.path.exists(projectDir):
        log.debug("Found an existing project dir.")
        return True
    else:
        log.debug("No projectDir found.")
        return False

def addResponse(buildState : BuildState, thisTransaction : Transaction, conformerID : str):        
    log.info("addResponse() was called.")
    try:
        pUUID = getProjectpUUID(thisTransaction)
        sequence = getSequenceFromTransaction(thisTransaction)
    except Exception as error:
        log.error("Problem finding the project pUUID or sequence in the transaction: " + str(error))
        log.error(traceback.format_exc())
        raise error
# "payload": "97b8338e-bdf5-4120-bb7e-609e4097af33",
# "sequence": "DNeu5Aca2-6DGalpb1-4DGlcpNAcb1-6[DNeu5Aca2-6DGalpb1-4DGlcpNAcb1-2]DManpa1-6[DNeu5Aca2-6DGalpb1-4DGlcpNAcb1-2[DNeu5Aca2-6DGalpb1-4DGlcpNAcb1-4]DManpa1-3]DManpb1-4DGlcpNAcb1-4DGlcpNAcb1-OH",
# "seqID": "b0f05178-eeb3-536c-8937-bfb1b797c2a8",
# "conformerID" : "44a25e2c-c7b5-5683-bc63-717ca66f23b5",         
# "conformerPath": "ProjectID/Requested_Structures/conformerID/",
# "fullDirectory": "/website/userdata/tools/cb/git-ignore-me_userdata/Builds/97b8338e-bdf5-4120-bb7e-609e4097af33/Requested_Structures/44a25e2c-c7b5-5683-bc63-717ca66f23b5",
# "downloadUrl": "http://172.25.0.2/json/download/cb/97b8338e-bdf5-4120-bb7e-609e4097af33/website/userdata/tools/cb/git-ignore-me_userdata/Builds/97b8338e-bdf5-4120-bb7e-609e4097af33/Requested_Structures/44a25e2c-c7b5-5683-bc63-717ca66f23b5"

    gemsProject = thisTransaction.response_dict['project']
    indexOrdered = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
    seqID = getSeqIDForSequence(indexOrdered)
    # By the time build3DStructure() is called, evaluation response exists.
    #  all we need to do is build the output and append it.
    output = sequence_io.Build3DStructureOutput(pUUID, sequence, seqID, conformerID)
    log.debug("Build3DStructure output: " + repr(output))
    outputs = []
    outputs.append(output)
    inputs = []
    inputs.append(sequence)
    serviceResponse = sequence_io.ServiceResponse("Build3DStructure", inputs, outputs)
    responseObj = serviceResponse.dict(by_alias=True)
    commonlogic.updateResponse(thisTransaction, responseObj)

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
            log.error(traceback.format_exc())
            raise error
        #else:
            #try:
                #updateBuildStatus(structureInfoFilename, buildState, "submitted")
            #except Exception as error:
                #log.error("There was a problem updating the structureInfo.json: " + str(error))
                #raise error
            #else:
                #try:
                    #updateBuildStatus(statusFilename, buildState, "submitted")
                #except Exception as error:
                    #log.error("There was a problem updating the status file: " + str(error))
                    #raise error



##  @brief Return true if this structure has been built previously, otherwise false.
#   @oaram
#   @return
def structureExists(buildState: BuildState, thisTransaction : Transaction, buildStrategyID : str):
    log.info("structureExists() was called.")
    if not sequenceExists(buildState, thisTransaction):
        log.debug("Sequence has never been built before; a new sequence is born!")
        return False
    sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
    userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
    seqID = getSeqIDForSequence(sequence)
    sequenceDir = userDataDir + seqID + "/" + buildStrategyID + "/" 
    log.debug("sequenceDir: " + sequenceDir)

    if buildState.structureLabel == "default":
        defaultBuildDir = sequenceDir + "All_Builds/default"
        log.debug("defaultBuildDir: " + defaultBuildDir)
        if os.path.isdir(defaultBuildDir):
            log.debug("default structure found.")
            return True
        else:
            log.debug("default structure not found.")
            return False
    else:
        
        structureLinkInSequenceDir = sequenceDir + "/All_Builds/" + buildState.structureDirectoryName
        log.debug("structureLinkInSequenceDir: " + structureLinkInSequenceDir)
        if os.path.isdir(structureLinkInSequenceDir):
            log.debug("The requested structure (" + buildState.structureDirectoryName + ") already exists.")
            return True
        else:
            log.debug("The requested structure (" + buildState.structureDirectoryName + ") doesn't exist.")
            return False
            ## Need to write a buildStateExists() method that compares BuildStates that have
            ##  been logged to file to requested BuildStates.
            ## Oliver: Not sure what this comment wants exactly, or if what I have done covers it.


##  @brief Return true if this sequence has been built previously, otherwise false.
#   @oaram
#   @return
def sequenceExists(buildState: BuildState, thisTransaction : Transaction):
    log.info("sequenceExists() was called.")
    try:
        sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
        log.debug("Checking for previous builds of this sequence: \n" + sequence)
    except Exception as error:
        log.error("There was a problem getting the sequence from structureInfo: " + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        ## Check if this sequence has been built before.
        ## Can we assume that seqID has already been initialized and saved?
        userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
        seqID = getSeqIDForSequence(sequence)
        sequenceDir = userDataDir + seqID
        log.debug("sequenceDir: " + sequenceDir)
        if os.path.isdir(sequenceDir):
            log.debug("This sequence has previous builds.")
            return True
        else:
            log.debug("No directory exists for this sequence, there cannot be any previous builds.")
            return False


##  @brief Build a structure response config oobject and append it to a transaction
#   @param Transaction
def respondWithExistingDefaultStructure(thisTransaction: Transaction):
    log.info("respondWithExistingDefaultStructure() was called.")

    try:
        gemsProject = thisTransaction.response_dict['gems_project']
        sequence = gemsProject['sequence']
        pUUID = gemsProject['pUUID']

        inputs = []
        inputs.append(sequence)
        
        indexOrdered = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
        seqID = getSeqIDForSequence(indexOrdered)

        downloadUrl = getDownloadUrl(gemsProject['pUUID'], "cb")
        outputs = []

        ouput = sequence_io.Build3DStructureOutput(pUUID, sequence, seqID, downloadUrl)
        outputs.append(ouput)

        serviceResponse = sequence_io.ServiceResponse("Build3DStructure", inputs, outputs)
        responseObj = serviceResponse.dict(by_alias = True)
        commonlogic.updateResponse(thisTransaction, responseObj)
    except Exception as error:
        log.error("There was a problem getting the sequence from the request: " + str(error))
        log.error(traceback.format_exc())
        raise error


##  @brief Pass in a gemsProject and get a responseConfig.
#   @param GemsProject gemsProject
#   @return dict config
def build3dStructureResponseConfig(thisTransaction : Transaction):
    log.info("build3dStructureResponseConfig() was called.\n")
    gemsProject = thisTransaction.response_dict['gems_project']
    indexOrdered = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
    seqID = getSeqIDForSequence(indexOrdered)
    downloadUrl = getDownloadUrl(gemsProject['pUUID'], "cb")
    sequence = gemsProject['sequence']
    config = {
        "sequence" : sequence,
        "validateOnly" : False,
        "outputType" : "Build3DStructure",
        "payload" : gemsProject['pUUID'],
        "seqID" : seqID,
        "downloadUrl" : downloadUrl

    }

    

    # config = {
    #     "entity" : "Sequence",
    #     "respondingService" : "Build3DStructure",
    #     "responses" : [{
    #         'payload' : gemsProject['pUUID'],
    #         'sequence' : gemsProject['sequence'],
    #         'seqID' : seqID,
    #         'downloadUrl' : downloadUrl
    #     }]
    # }

    log.debug("returning 3dStructureResponseConfig: " + str(config))

    return config


## TODO: make all these directory/link/file making functions into one thing
## that gets called by string only


## OG this is all being done elsewhere
# def createSequenceProjectDirectoryStructure(projectDir : str ):
#     # Ensure that the project directory is present and add some dirs
#     log.info("createSequenceProjectDirectoryStructure() was called.")
#     if os.path.exists(projectDir):
#         log.debug("Found an existing project dir.")
#     else:
#         log.debug("No projectDir found.  Making one now at: " + projectDir)
#         try: 
#             os.makedirs(projectDir)
#         except Exception as error:
#             log.error("There was a problem making directory: " + projectDir)
#             raise error
#     try:
#         log.debug("Changing to the project diretctory for making more.")
#         os.chdir(projectDir)
#     except Exception as error:
#         log.error("Could not chdir to the project directory: " + projectDir)
#         raise error
#     try: 
#         ##  TODO:  write code to determine if there are multiple rotamers 
#         ##  possible and, if so, to make directories for them.
#         ##  For this moment, single-structure only
#         ##
#         ##  Also consider having it not create both New and Existing every time.
#         ##  Might be just as well to leave it.  But, do think about that.
#         ##  Note that makedirs makes everything in supplied path that doesn't exist.
#         ##  Exception should be raised when making projectID if it exists already.
#         os.makedirs('defaults/Requested_Builds',exist_ok = True)
#         os.makedirs('logs',exist_ok = True)
#         os.makedirs('New_Builds/logs',exist_ok = True)
#         os.makedirs('New_Builds/structure',exist_ok = True)
#         #Required if previous structures exist, but decision should be elsewhere?
#         os.makedirs('Existing_Builds/logs',exist_ok = True)
#         # if not os.path.exists('defaults/Requested_Builds') : 
#         #     os.makedirs('defaults/Requested_Builds')
#         # if not os.path.exists('logs') : 
#         #     os.makedirs('logs')
#         # if not os.path.exists('New_Builds/logs') : 
#         #     os.makedirs('New_Builds/logs')
#         # if not os.path.exists('New_Builds/structure') : 
#         #     os.makedirs('New_Builds/structure')
#         # if not os.path.exists('Existing_Builds/logs') : 
#         #     os.makedirs('Existing_Builds/logs')
#     except Exception as error:
#         log.error("There was a problem making directory: " + projectDir)
#         raise error

def createConformerDirectoryInBuildsDirectory(projectDir : str, conformerDirName : str):
    log.info("createConformerDirectoryInBuildsDirectory() was called.")
    log.debug("projectDir: " + projectDir)
    log.debug("conformerDirName: " + conformerDirName)
    conformerDirPath = (projectDir + "/New_Builds/" + conformerDirName + '/')
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

# def createDefaultSymLinkSequencesDirectory(this_seqID : str, conformerID : str, buildStrategyID : str):
#     log.info("createDefaultSymLinkSequencesDirectory() was called")
#     try:
#         sequence_dir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
#         parent_dir = sequence_dir + this_seqID + "/" + buildStrategyID + "/" 
#         path_down_to_source = "All_Builds/" + conformerID
#         path_down_to_dest_dir = None
#         commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, "defaultFolder", parent_dir)
#         path_down_to_source = "defaultFolder/mol_min.pdb"
#         commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, "default.pdb", parent_dir)
#         path_down_to_source = "defaultFolder/structure.pdb"
#         commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir, "default_unminimized.pdb", parent_dir)
#     except Exception as error:
#         log.error("Cound not create default symlinks in Sequences/" + str(error))
#         raise error

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


## Oliver: Change this to be for default structures, or delete
# def createSequenceProjectSymlinks(projectDir : str):
#     # Generate symbolic links within project directories
#     log.info("createSequenceProjectSymlinks() was called.")
#     try:
#         log.debug("Changing to the project diretctory for making more.")
#         os.chdir(projectDir)
#     except Exception as error:
#         log.error("Could not chdir to the project directory: " + projectDir)
#         raise error
#     # TODO:  write in logic for:
#     #     evaluate.determineDefaultStructures()
#     if os.path.exists("New_Builds/structure/structure.pdb"):
#         default_unminimized="New_Builds/structure/structure.pdb"
#         default="New_Builds/structure/mol_min.pdb"
#         structure="New_Builds/structure"
#     elif os.path.exists("Existing_Builds/structure/structure.pdb"):
#         default_unminimized="Existing_Builds/structure/structure.pdb"
#         default="Existing_Builds/structure/mol_min.pdb"
#         structure="Existing_Builds/structure"
#     else:
#         log.error("Cannot find the default unminimized structure.")
#     try:
# #        make_relative_symbolic_link(
# #                path_down_to_source : str, 
# #                path_down_to_dest_dir : str , 
# #                dest_link_label : str, 
# #                parent_directory : str
# #                )
#         commonlogic.make_relative_symbolic_link( default_unminimized, 'defaults' , 'default_unminimized.pdb', None)
#         commonlogic.make_relative_symbolic_link( default, 'defaults' , 'default.pdb', None)
#         commonlogic.make_relative_symbolic_link( structure,'defaults/Requested_Builds' , 'structure', None)
#     except Exception as error:
#         log.error("Could not make one or mor symlinks in Create Project symlinks")
#         raise error
 





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
        os.makedirs(projIDPath + '/Requested_Builds')
        os.makedirs(projIDPath + '/Existing_Builds')
        os.makedirs(projIDPath + '/New_Builds')
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
    


    # logs folder handled by the generic startProject function

#     # For now, just setting for a single structure
#     if not os.path.isdir(projIDPath + '/defaults/Requested_Builds'):
#         # TODO:  one day this might be annoying.  Feel free to change it
#         raise AttributeError("Cannot make sequence links for uninitialized project directory")
#     if not os.path.exists(projIDPath + '/defaults/Sequence_Repository'): 
#         path_down_to_source = 'Sequences/'+ sequenceID
#         path_down_to_dest_dir = 'Builds/' + projectID + '/defaults/'
# #        make_relative_symbolic_link(
#                path_down_to_source : str, 
#                path_down_to_dest_dir : str , 
#                dest_link_label : str, 
#                parent_directory : str
#                )
        # commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir , 'Sequence_Repository', parent_dir)        
 # ## OG removing this bit, it was specific for a default structure, will replace with something that handles both.
#     ## If this appears to be a new build for this sequence, have seqIDPath point into projIDPath    
#     if os.path.isfile(projIDPath + '/New_Builds/structure/structure.off'):
#         # TODO : Make it possible for there to be other Build_Conditions....
#         log.debug("This appears to be a bew build.")
#         path_down_to_source = 'Builds/' + projectID + '/New_Builds/structure'
#         path_down_to_dest_dir = 'Sequences/'+sequenceID + '/' + buildStrategyID + '/All_Builds/'
#         if not os.path.exists(path_down_to_dest_dir + '/structure') : 
#             commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir , None, parent_dir)
#         temp_parent_dir = seqIDPath + '/' + buildStrategyID + '/'
#         path_down_to_source = 'All_Builds/structure/mol_min.pdb'
#         log.debug("The relevant paths are:  ")
#         log.debug("        temp_parent_dir : " + temp_parent_dir)
#         log.debug("        path_down_to_source  :  " + path_down_to_source)
#         commonlogic.make_relative_symbolic_link(path_down_to_source, None, 'default.pdb' ,  temp_parent_dir)
#         path_down_to_source = 'All_Builds/structure/structure.pdb'
#         commonlogic.make_relative_symbolic_link(path_down_to_source, None, 'default_unminimized.pdb' , temp_parent_dir)
#     ## If this appears to be an old build for this sequence, ink have projIDPath point into seqIDPath
#     else:
#         log.debug("New build failed, so we will assume it is an existing build.")
#         path_down_to_source = 'Sequences/'+ sequenceID + '/' + buildStrategyID + '/All_Builds/structure'
#         path_down_to_dest_dir = 'Builds/' + projectID + '/Existing_Builds/'
#         commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir , None, parent_dir)
## OG removing END

# def createSymLinksOldAndCrufty(buildState : BuildState, thisTransaction : Transaction):
#     log.info("createSymLinks() was called.")

#     sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
#     seqID = getSeqIDForSequence(sequence)

    
#     log.debug("Checking to see if the seqIDPath already exists for this sequence: " + seqIDPath)
#     if not os.path.exists(seqIDPath):
#         log.debug("seqIDPath does not exist. Creating it now.")
#         try:
#             os.makedirs(seqIDPath)
#         except Exception as error:
#             log.error("There was a problem creating the seqIDPath: " + str(error))
#             raise error
#         else:
#             try:
#                 createSeqLog(sequence, seqIDPath)
#             except Exception as error:
#                 log.error("There was a problem creating the SeqLog: " + str(error))
#                 raise error
#             else:
#                 projectDir = getProjectDir(thisTransaction)
#                 try:
#                     isDefault = checkIfDefaultStructureRequest(thisTransaction)
#                     log.debug("isDefault: " + str(isDefault))
#                     if isDefault:
#                         link = seqIDPath + "/default"
#                         projectDir = projectDir + "default"
#                     else:
#                         link = seqIDPath + "/" + buildState.structureLabel
                    
#                     if os.path.exists(projectDir):
#                         target = projectDir
#                         ##What is being linked to is the projecDir or the 
#                         log.debug("target: " + target)
#                         ##This will be the symbolic link
#                         log.debug("link: " + link)
#                         os.symlink(target, link)
#                     else:
#                         log.error("Failed to find the target dir for the symbolic link.")
#                         raise FileNotFoundError(projectDir)
                    
#                 except Exception as error:
#                     log.error("There was a problem creating the symbolic link.")
#                     raise error
            
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

