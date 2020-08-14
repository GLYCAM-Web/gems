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
def structureExists(buildState: BuildState, thisTransaction : Transaction):
    log.info("structureExists() was called.")

    structureExists = False
    try:
        sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
        log.debug("Checking for previous builds of this sequence: \n" + sequence)
    except Exception as error:
        log.error("There was a problem getting the sequence from structureInfo: " + str(error))
        raise error
    else:
        ## Check if this sequence has been built before.
        userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
        seqID = getSeqIDForSequence(sequence)
        sequenceDir = userDataDir + seqID

        log.debug("sequenceDir: " + sequenceDir)
        if os.path.isdir(sequenceDir):
            log.debug("This sequence has previous builds.")
            return True
#            structureLabel = buildState.structureLabel
#            if structureLabel == "default":
#                ## Easy. Just check the path. If it exists, return true.
#                defaultBuildDir = sequenceDir + "/defaults/All_Builds/structure"
#                if os.path.isdir(defaultBuildDir):
#                    log.debug("default structure found.")
#                    return True
#                else:
#                    log.debug("default structure not found.")
#                    return False
#            else:
###
### START HERE -- add this logic
###
#                log.error("Need to write the logic that checks for existing builds that are not the defaults.")
#                ## Need to write a buildStateExists() method that compares BuildStates that have
#                ##  been logged to file to requested BuildStates.
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
        sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
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

## TODO: make all these directory/link/file making functions into one thing
## that gets called by string only

def createProjectDirectoryStructure(projectDir : str ):
    # Ensure that the project directory is present and add some dirs
    log.info("creatProjectDirectoryStructure() was called.")
    if os.path.exists(projectDir):
        log.debug("Found an existing project dir.")
    else:
        log.debug("No projectDir found.  Making one now at: " + projectDir)
        try: 
            os.makedirs(projectDir)
        except Exception as error:
            log.error("There was a problem making directory: " + projectDir)
            raise error
    try:
        log.debug("Changing to the project diretctory for making more.")
        os.chdir(projectDir)
    except Exception as error:
        log.error("Could not chdir to the project directory: " + projectDir)
        raise error
    try: 
        ##  TODO:  write code to determine if there are multiple rotamers 
        ##  possible and, if so, to make directories for them.
        ##  For this moment, single-structure only
        ##
        ##  Also consider having it not create both New and Existing every time.
        ##  Might be just as well to leave it.  But, do think about that.
        if not os.path.exists('defaults/All_Builds') : 
            os.makedirs('defaults/All_Builds')
        if not os.path.exists('logs') : 
            os.makedirs('logs')
        if not os.path.exists('New_Builds/logs') : 
            os.makedirs('New_Builds/logs')
        if not os.path.exists('New_Builds/structure') : 
            os.makedirs('New_Builds/structure')
        if not os.path.exists('Existing_Builds/logs') : 
            os.makedirs('Existing_Builds/logs')
    except Exception as error:
        log.error("There was a problem making directory: " + projectDir)
        raise error


def createProjectSymlinks(projectDir : str):
    # Generate symbolic links within project directories
    log.info("creatProjectSymlinks() was called.")
    try:
        log.debug("Changing to the project diretctory for making more.")
        os.chdir(projectDir)
    except Exception as error:
        log.error("Could not chdir to the project directory: " + projectDir)
        raise error
    # TODO:  write in logic for:
    #     evaluate.determineDefaultStructures()
    if os.path.exists("New_Builds/structure/structure.pdb"):
        default_unminimized="New_Builds/structure/structure.pdb"
        default="New_Builds/structure/mol_min.pdb"
        structure="New_Builds/structure"
    elif os.path.exists("Existing_Builds/structure/structure.pdb"):
        default_unminimized="Existing_Builds/structure/structure.pdb"
        default="Existing_Builds/structure/mol_min.pdb"
        structure="Existing_Builds/structure"
    else:
        log.error("Cannot find the default unminimized structure.")
    try:
#        make_relative_symbolic_link(
#                path_down_to_source : str, 
#                path_down_to_dest_dir : str , 
#                dest_link_label : str, 
#                parent_directory : str
#                )
        commonlogic.make_relative_symbolic_link( default_unminimized, 'defaults' , 'default_unminimized.pdb', None)
        commonlogic.make_relative_symbolic_link( default, 'defaults' , 'default.pdb', None)
        commonlogic.make_relative_symbolic_link( structure,'defaults/All_Builds' , 'structure', None)
    except Exception as error:
        log.error("Could not make one or mor symlinks in Create Project symlinks")
        raise error
 


## TODO: Rewrite this to a smaller scope: symlinks, and folder creation 

##  @brief  Creates the directories and files needed to store a file that can be
#           reused via symlink.
#   @detail Still being worked on, but works for default structures.
#   @param  Transaction
def createSequenceSymLinks(sequenceID:str, projectID:str):
    log.info("createSequenceSymLinks() was called.")
    ## userDataDir is the top level dir that holds the repository of all sequences
    sequencePath = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
    seqIDPath = sequencePath + sequenceID
    projectPath = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Builds/"
    projIDPath = projectPath + projectID
    parent_dir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"
    all_builds = seqIDPath + '/Build_Conditions_1/All_Builds/'
    if not os.path.isdir(all_builds):
        try:
            os.makedirs(all_builds)
        except Exception as error:
            log.error("There was a problem creating the seqIDPath: " + str(error))
            raise error
    # TODO : Make it possible for there to be other Build_Conditions....
    if not os.path.isdir(seqIDPath + '/defaults'):
        path_down_to_source = 'Build_Conditions_1/'
        commonlogic.make_relative_symbolic_link(path_down_to_source, None , 'defaults', seqIDPath)
    # TODO:  write evaluate.determineDefaultSequenecStructures which should be a lot like
    #        evaluate.determineDefaultStructures()
    # For now, just setting for a single structure
    if not os.path.isdir(projIDPath + '/defaults/All_Builds'):
        # TODO:  one day this might be annoying.  Feel free to change it
        raise AttributeError("Cannot make sequence links for uninitialized project directory")
    if not os.path.exists(projIDPath + '/defaults/Sequence_Repository'): 
        path_down_to_source = 'Sequences/'+sequenceID
        path_down_to_dest_dir = 'Builds/' + projectID + '/defaults/'
#        make_relative_symbolic_link(
#                path_down_to_source : str, 
#                path_down_to_dest_dir : str , 
#                dest_link_label : str, 
#                parent_directory : str
#                )
        commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir , 'Sequence_Repository', parent_dir)
    ## If this appears to be a new build for this sequence, have seqIDPath point into projIDPath
    if os.path.isfile(projIDPath + '/New_Builds/structure/structure.off'):
        # TODO : Make it possible for there to be other Build_Conditions....
        log.debug("This appears to be a bew build.")
        path_down_to_source = 'Builds/' + projectID + '/New_Builds/structure'
        path_down_to_dest_dir = 'Sequences/'+sequenceID + '/Build_Conditions_1/All_Builds/'
        if not os.path.exists(path_down_to_dest_dir + '/structure') : 
            commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir , None, parent_dir)
        temp_parent_dir = seqIDPath + '/Build_Conditions_1/'
        path_down_to_source = 'All_Builds/structure/mol_min.pdb'
        log.debug("The relevant paths are:  ")
        log.debug("        temp_parent_dir : " + temp_parent_dir)
        log.debug("        path_down_to_source  :  " + path_down_to_source)
        commonlogic.make_relative_symbolic_link(path_down_to_source, None, 'default.pdb' ,  temp_parent_dir)
        path_down_to_source = 'All_Builds/structure/structure.pdb'
        commonlogic.make_relative_symbolic_link(path_down_to_source, None, 'default_unminimized.pdb' , temp_parent_dir)
    ## If this appears to be an old build for this sequence, ink have projIDPath point into seqIDPath
    else:
        log.debug("New build failed, so we will assume it is an existing build.")
        path_down_to_source = 'Sequences/'+sequenceID + '/Build_Conditions_1/All_Builds/structure'
        path_down_to_dest_dir = 'Builds/' + projectID + '/Existing_Builds/'
        commonlogic.make_relative_symbolic_link(path_down_to_source, path_down_to_dest_dir , None, parent_dir)


def createSymLinksOldAndCrufty(buildState : BuildState, thisTransaction : Transaction):
    log.info("createSymLinks() was called.")

    sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
    seqID = getSeqIDForSequence(sequence)

    
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

    ## If default structure, subdir name is 'structure'
    if checkIfDefaultStructureRequest(thisTransaction):
        pass
#        project_dir = project_dir + "structure/"
#        if not os.path.exists(project_dir):
#            os.makedirs(project_dir)

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
            raise error
        else:
            return structureExists



def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

