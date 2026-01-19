#!/usr/bin/env python3
import os
import pathlib
import traceback
from typing import List
from gemsModules.deprecated.project import projectUtilPydantic as projectUtils
from gemsModules.deprecated.project.io import CbProject 
from gemsModules.deprecated.common import logic as commonlogic
from gemsModules.deprecated.common.loggingConfig import loggers, createLogger
from gemsModules.deprecated.sequence import io as sequenceio
from gemsModules.deprecated.sequence import structureInfo

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


def addResponse(buildState: sequenceio.Single3DStructureBuildDetails, thisTransaction: sequenceio.Transaction, conformerID: str, conformerLabel: str):
    log.info("addResponse() was called.")
    # By the time build3DStructure() is called, evaluation response exists.
    #  all we need to do is build the output and append it.
    thisSequence = thisTransaction.transaction_out.entity
    thisProject = thisTransaction.transaction_out.project
    thisBuildOutput = sequenceio.Single3DStructureBuildDetails()
    thisBuildOutput.conformerID = conformerID
    thisBuildOutput.conformerLabel = conformerLabel
    try:
        thisBuildOutput.payload = projectUtils.getProjectpUUID(thisProject)
        thisBuildOutput.incomingSequence = thisTransaction.getInputSequencePayload()
    except Exception as error:
        log.error(
            "Problem finding the project pUUID or sequence in the transaction: " + str(error))
        log.error(traceback.format_exc())
        raise error

    thisBuildOutput.indexOrderedSequence = thisTransaction.getSequenceVariantOut(
        'indexOrdered')
    thisBuildOutput.seqID = projectUtils.getSeqIdForSequence(
        thisBuildOutput.indexOrderedSequence)
    return thisBuildOutput


def registerBuild(buildState: sequenceio.Single3DStructureBuildDetails, thisTransaction: sequenceio.Transaction):
    log.debug("registerBuild() was called.")
    try:
        # TODO: get the path for structureInfo.json
        structureInfoFilename = structureInfo.getStructureInfoFilename(
            thisTransaction)
        log.debug("structureInfoFilename:" + str(structureInfoFilename))
    except Exception as error:
        log.error(
            "There was a problem getting the path for structureInfo.json: " + str(error))
        log.error(traceback.format_exc())
        raise error

    try:
        # TODO: get the path for structureInfo_status.json
        statusFilename = structureInfo.getStatusFilename(thisTransaction)
        log.debug("statusFilename:" + str(statusFilename))
    except Exception as error:
        log.error("There was a problem getting the status filename: " + str(error))
        log.error(traceback.format_exc())
        raise error


def get_all_conformerIDs_in_project_dir(project_path : str) -> List[str]:
    # Assume that conformers in "Requested" are all of them
    from os import listdir, path
    return listdir(path.join(project_path, "Requested_Builds"))


# @brief Return true if this structure has been built previously, otherwise false.
#   @oaram
#   @return
##### FIX ME
def currentBuildStructureExists(buildState: sequenceio.Single3DStructureBuildDetails, thisTransaction: sequenceio.Transaction):
    log.info("currentBuildStructureExists() was called.")
    if not currentBuildSequenceExists(thisTransaction):
        log.debug("Sequence has never been built before; a new sequence is born!")
        return False
    else:
        log.debug(
            "Sequence has previous builds. Checking for the requested buildState.")
        indexOrderedSequence = thisTransaction.getSequenceVariantOut(
            'indexOrdered')
        thisProject = thisTransaction.getProjectOut()
        if thisProject is None:
            message = "The outgoing project is None so cannot determine the filesystem path."
            log.error(message)
            thisTransaction.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo={'hint': message}
            )
            return
        thisSequence = thisTransaction.transaction_out.entity
        if thisSequence is None:
            message = "The Entity (sequence) is None so cannot determine if structure exists."
            log.error(message)
            thisTransaction.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo={'hint': message}
            )
            return


#        servicePath = os.path.join(thisProject.getFilesystemPath(
#        ), thisProject.getEntityId(), thisProject.getServiceId())
#        sequencePath = os.path.join(servicePath, "Sequences")
#        seqID = projectUtils.getSeqIdForSequence(indexOrderedSequence)
#        sequenceDir = os.path.join(
#            sequencePath, seqID, thisSequence.outputs.getBuildStrategyID())
#        log.debug("sequenceDir: " + sequenceDir)

        # get the directory for this sequence with the specified build strategy
        sequenceDir = os.path.join(
            get_sequence_base_directory(indexOrderedSequence, thisProject),
            thisSequence.outputs.getBuildStrategyID())
        log.debug("sequenceDir: " + sequenceDir)

        log.debug("buildState.conformerLabel: " + buildState.conformerLabel)
        structureLinkInSequenceDir = os.path.join(
            sequenceDir, "All_Builds", buildState.structureDirectoryName)
        log.debug("structureLinkInSequenceDir: " + structureLinkInSequenceDir)
        if os.path.isdir(structureLinkInSequenceDir):
            log.debug("The requested structure directory exists (" +
                      buildState.structureDirectoryName + ") already exists.")
            log.debug("checking for output file: " +
                      structureLinkInSequenceDir + "/structure.pdb).")
            if os.path.isfile(structureLinkInSequenceDir + "/structure.pdb"):
                return True
            else:
                return False
        else:
            log.debug("The requested structure (" +
                      buildState.structureDirectoryName + ") doesn't exist.")
            return False
            # Need to write a buildStateExists() method that compares Single3DStructureBuildDetails that have
            # been logged to file to requested Single3DStructureBuildDetails.
            # Oliver: Not sure what this comment wants exactly, or if what I have done covers it.


def get_sequence_base_directory(sequence: str, thisProject: CbProject) -> str:
    servicePath = os.path.join(
            thisProject.getFilesystemPath(), 
            thisProject.getEntityId(), 
            thisProject.getServiceId())
    sequence_base_dir = os.path.join(servicePath, "Sequences", get_seqID(sequence))
    log.debug("sequence base dir: " + sequence_base_dir)
    return sequence_base_dir


def get_seqID(sequence: str) -> str:
    return projectUtils.getSeqIdForSequence(sequence)


def sequence_default_structure_exists(the_path : str) -> bool:
    if Path(os.path.join(the_path, 'min-gas.pdb')).exists():
        return True
    if Path(os.path.join(the_path, 'structure.pdb')).exists():
        return True


def get_existing_default_evaluation_path(thisTransaction: sequenceio.Transaction) -> str:
    sequence = thisTransaction.getSequenceVariantOut('indexOrdered')
    if sequence is None:
        return None
    thisProject = thisTransaction.transaction_out.project
    sequence_base_dir = get_sequence_base_directory(sequence, thisProject)
    sequence_default_link = os.path.join(sequence_base_dir, "evaluation.json")
    from pathlib import Path
    the_path = Path(sequence_default_link)
    try:
        the_real_path = the_path.resolve(strict=True)
    except FileNotFoundError:
        return None
    return the_real_path




# @brief Return true if this sequence has been built previously using the current build strategy, otherwise false.
#   @oaram
#   @return
def currentBuildSequenceExists(thisTransaction: sequenceio.Transaction):
    log.info("currentBuildSequenceExists() was called.")
    try:
        sequence = thisTransaction.getSequenceVariantOut('indexOrdered')
    except Exception as error:
        log.error(
            "There was a problem getting the sequence from structureInfo: " + str(error))
        log.error(traceback.format_exc())
        raise error
    # Check if this sequence has been built before.
    # Can we assume that seqID has already been initialized and saved?
    log.debug("Checking for previous builds of this sequence: " + sequence)
    thisProject = thisTransaction.getProjectOut()
    if thisProject is None:
        message = "The outgoing project is None so cannot determine the filesystem path."
        log.error(message)
        thisTransaction.generateCommonParserNotice(
            noticeBrief='GemsError',
            additionalInfo={'hint': message}
        )
        return
    thisSequence = thisTransaction.transaction_out.entity
    if thisSequence is None:
        message = "The Entity (sequence) is None so cannot determine if sequence exists."
        log.error(message)
        thisTransaction.generateCommonParserNotice(
            noticeBrief='GemsError',
            additionalInfo={'hint': message}
        )
        return

    servicePath = os.path.join(thisProject.getFilesystemPath(
    ), thisProject.getEntityId(), thisProject.getServiceId())
    log.debug("servicePath is : " + servicePath)
    log.debug("servicePath is made from these things: ")
    log.debug("filesystem path:  " + thisProject.getFilesystemPath())
    log.debug("entity id:  " + thisProject.getEntityId())
    log.debug("service id : " + thisProject.getServiceId())
    sequencePath = os.path.join(servicePath, "Sequences")
    log.debug("sequencePath is : " + sequencePath)
    seqID = projectUtils.getSeqIdForSequence(sequence)
    log.debug("seqID is : " + seqID)
    # I think this is correct (Lachele)
    sequenceDir = os.path.join(
        sequencePath, seqID, thisSequence.outputs.getBuildStrategyID())
    # it used to say this
    # sequenceDir = sequencePath + seqID
    log.debug("sequenceDir is :   " + sequenceDir)
    if os.path.isdir(sequenceDir):
        log.debug("This sequence has previous builds.")
        return True
    else:
        log.debug(
            "No directory exists for this sequence, there cannot be any previous builds.")
        return False


# TODO: make all these directory/link/file making functions into one thing
# that gets called by string only
def createConformerDirectoryInBuildsDirectory(
        projectDir: str,
        conformerDirName: str,
        separator: str = 'New_Builds'):
    log.info("createConformerDirectoryInBuildsDirectory() was called.")
    log.debug("projectDir: " + projectDir)
    log.debug("conformerDirName: " + conformerDirName)
    conformerDirPath = os.path.join(projectDir, separator, conformerDirName)
    if os.path.isdir(conformerDirPath):
        return
    try:
        log.debug("Trying to create conformerDirPath: " + conformerDirPath)
        os.makedirs(conformerDirPath,mode=0o755)

    except Exception as error:
        log.error("Could not create conformerDirPath: " + conformerDirPath)
        log.error(traceback.format_exc())
        raise error

# Creates a symlink in Requested_Builds into either Existing_Builds or New_Builds


def createSymLinkInRequestedStructures(projectDir: str, buildDir: str, conformerID: str):
    log.info("createSymLinkInRequestedStructures() was called.")
    try:
        os.makedirs(projectDir + "/Requested_Builds/", exist_ok=True)
        # Can be New_Builds/conformerID or Existing_Builds/conformerID
        path_down_to_source = buildDir + "/" + conformerID
        path_down_to_dest_dir = "Requested_Builds/"
        commonlogic.make_relative_symbolic_link(
            path_down_to_source, path_down_to_dest_dir, conformerID, projectDir)
    except Exception as error:
        log.error(
            "Could not create link in Builds/projectID/Requested_Builds/: " + str(error))
        log.error(traceback.format_exc())
        raise error


def get_default_evaluation_path_from_sequence(thisTransaction: sequenceio.Transaction) -> str:
    thisProject = thisTransaction.transaction_out.project
    service_dir = thisProject.service_dir
    sequence_ID = thisTransaction.getSequenceVariantOut('suuid')
    sequence_default_link = os.path.join(service_dir, "Sequences", sequence_ID, "evaluation.json")
    from pathlib import Path
    the_path = Path(sequence_default_link)
    log.debug("The expected path for the sequence default evaluation json follows.")
    log.debug(sequence_default_link)
    try:
        the_real_path = the_path.resolve(strict=True)
    except FileNotFoundError as error:
        log.debug("could not get the real path to the evaluation json.  Error follows;")
        log.debug(error)
        return None
    return the_real_path


def set_default_evaluation_symlink_in_sequence(thisTransaction: sequenceio.Transaction) -> str:
    if get_default_evaluation_path_from_sequence(thisTransaction) is not None:
        return
    try: 
        thisProject = thisTransaction.transaction_out.project
        path_to_new_link = thisProject.sequence_path
        path_to_existing_path = os.path.join(thisProject.logs_dir, 'response.json')
        commonlogic.make_relative_symbolic_link(
                path_down_to_source = path_to_existing_path,
                path_down_to_dest_dir = path_to_new_link, 
                dest_link_label = 'evaluation.json', 
                parent_directory = thisProject.service_dir)
        return None
    except Exception as error:
        message =  "Something went wrong setting the evaluation sym link in the sequence directory."
        log.error(message)
        log.debug(error)
        return message


def addSequenceFolderSymLinkToDefaultBuild(servicePath: str, sequenceID: str, buildStrategyID: str, conformerID: str):
    log.info("addSequenceFolderSymLinkToDefaultBuild() was called.")
    # Add a symlink pointing from Sequences/sequenceID/default
    #                          to Sequences/sequenceID/buildStrategyID/All_Builds/conformerID
    path_to_new_link = os.path.join('Sequences' , sequenceID)
    path_to_existing_path = os.path.join('Sequences' , sequenceID ,  buildStrategyID , 'All_Builds' , conformerID)
    log.debug("Creating symlink with toolPath " + servicePath + " called " + conformerID +
              " from " + path_to_new_link + " pointing to " + path_to_existing_path)
    commonlogic.make_relative_symbolic_link(
            path_down_to_source = path_to_existing_path,
            path_down_to_dest_dir = path_to_new_link, 
            dest_link_label = 'default', 
            parent_directory = servicePath)

def addSequenceBuildStrategyFolderSymLinkToDefaultBuild(servicePath: str, sequenceID: str, buildStrategyID: str,  conformerID: str):
    log.info("addSequenceBuildStrategyFolderSymLinkToDefaultBuild() was called.")
    # Add a symlink from Sequences/sequenceID/buildStrategyID/default
    #                 to Sequences/sequenceID/buildStrategyID/All_Builds/conformerID
    path_to_new_link = os.path.join('Sequences' , sequenceID , buildStrategyID)
    path_to_existing_path = os.path.join('Sequences' , sequenceID ,  buildStrategyID , 'All_Builds' , conformerID)
    log.debug("Creating symlink with toolPath " + servicePath + " called " + conformerID +
              " from " + path_to_new_link + " pointing to " + path_to_existing_path)
    commonlogic.make_relative_symbolic_link(
            path_down_to_source = path_to_existing_path,
            path_down_to_dest_dir = path_to_new_link, 
            dest_link_label = 'default', 
            parent_directory = servicePath)


def addSequenceFolderSymLinkToNewBuild(servicePath: str, sequenceID: str, buildStrategyID: str, projectID: str, conformerID: str):
    log.info("addSequenceFolderSymLinkToNewBuild() was called.")
    # Add a symlink from Sequences/sequenceID/buildStrategyID/All_Builds/conformerID
    #                 to Builds/projectID/New_Builds/conformerID
    # Don't want to call this function for Existing_Builds, as they should already be linked from All_Builds.
    path_down_to_source = 'Builds/' + projectID + "/New_Builds/" + conformerID
    path_down_to_dest_dir = 'Sequences/' + sequenceID + \
        '/' + buildStrategyID + '/All_Builds/'
    log.debug("Creating symlink with toolPath " + servicePath + " called " + conformerID +
              " from " + path_down_to_dest_dir + " pointing to " + path_down_to_source)
    commonlogic.make_relative_symbolic_link(
        path_down_to_source, path_down_to_dest_dir, conformerID, servicePath)


def addBuildFolderSymLinkToExistingConformer(servicePath: str, sequenceID: str, buildStrategyID: str, projectID: str, conformerID: str):
    log.info("addBuildFolderSymLinkForExistingConformer() was called.")
    sequencePath = os.path.join(servicePath, "/Sequences/")
    path_down_to_dest_dir = os.path.join(
        'Builds', projectID, 'Existing_Builds')
    path_down_to_source = os.path.join(
        'Sequences', sequenceID, buildStrategyID, 'All_Builds', conformerID)
    log.debug("Creating symlink in " + servicePath + " between " +
              path_down_to_dest_dir + " called " + conformerID + " to " + path_down_to_source)
    commonlogic.make_relative_symbolic_link(
        path_down_to_source, path_down_to_dest_dir, conformerID, servicePath)

def addBuildFolderSymLinkForDefaultConformer(projectDir: str, buildDir: str, conformerID: str):
    log.info("addBuildFolderSymLinkForDefaultConformer() was called.")
    try:
        path_to_existing_path = os.path.join(buildDir, conformerID)
        path_to_new_link = projectDir
        commonlogic.make_relative_symbolic_link(
                path_down_to_source = path_to_existing_path,
                path_down_to_dest_dir = path_to_new_link, 
                dest_link_label = 'default', 
                parent_directory = projectDir)
    except Exception as error:
        log.error(
            "Could not create default link in Builds/projectID/: " + str(error))
        log.error(traceback.format_exc())
        raise error



# @brief  Creates the directories and files needed to store a file that can be
#           reused via symlink.
#   @detail Still being worked on, but works for default structures.
#   @param  Transaction
###########  FIX ME
def setupInitialSequenceFolders(servicePath: str, sequenceID: str, projectID: str, buildStrategyID: str):
    log.info("setupInitialSequenceFolders() was called.")
    # Some of the folders in Sequence may already exist via a previous project, those in Builds should not.
    log.debug("Here are the inputs: ")
    log.debug("servicePath:str : " + servicePath)
    log.debug("sequenceID:str : " + sequenceID)
    log.debug("projectID:str : " + projectID)
    log.debug("buildStrategyID:str : " + buildStrategyID)
    sequencePath = os.path.join(servicePath, "Sequences")
    seqIDPath = os.path.join(sequencePath, sequenceID)
    buildPath = os.path.join(servicePath, "Builds")
    projIDPath = os.path.join(buildPath, projectID)
    buildStrategyPath = os.path.join(seqIDPath, buildStrategyID)
    log.debug("sequencePath : " + sequencePath)
    log.debug("seqIDPath : " + seqIDPath)
    log.debug("buildPath : " + buildPath)
    log.debug("projIDPath : " + projIDPath)
    log.debug("buildStrategyPath : " + buildStrategyPath)
    if not os.path.isdir(buildStrategyPath):
        try:
            log.debug("buildStrategyPath was not found, so trying to create it.")
            log.debug("buildStrategyPatth is : " + str(buildStrategyPath))
            pathlib.Path(buildStrategyPath).mkdir(parents=True)
            log.debug("The path now exists? ")
            log.debug(os.path.isdir(buildStrategyPath))
            # Same level as parent directory (seqIDPath)
            path_down_to_dest_dir = None
            log.debug("seqIDPath is : " + seqIDPath +
                      " ... and does it exist? ")
            log.debug(os.path.isdir(seqIDPath))
            commonlogic.make_relative_symbolic_link(
                buildStrategyPath, None, 'current', seqIDPath)
        except Exception as error:
            log.error(
                "There was a problem creating buildStrategyPath: " + str(error))
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
        requestedBuildsPath = os.path.join(projIDPath, 'Requested_Builds')
        existingBuildsPath = os.path.join(projIDPath, 'Existing_Builds')
        newBuildsPath = os.path.join(projIDPath, 'New_Builds')
        newBuildsLogsPath = os.path.join(projIDPath, 'New_Builds', 'logs')
        existingBuildsLogsPath = os.path.join(
            projIDPath, 'Existing_Builds', 'logs')
        log.debug("Making these paths : ")
        log.debug("requestedBuildsPath : " + requestedBuildsPath)
        log.debug("existingBuildsPath : " + existingBuildsPath)
        log.debug("newBuildsPath : " + newBuildsPath)
        log.debug("newBuildsLogsPath : " + newBuildsLogsPath)
        log.debug("existingBuildsLogsPath :" + existingBuildsLogsPath)
        pathlib.Path(requestedBuildsPath).mkdir(parents=True, exist_ok=True)
        pathlib.Path(existingBuildsPath).mkdir(parents=True,  exist_ok=True)
        pathlib.Path(newBuildsPath).mkdir(parents=True, exist_ok=True)
        pathlib.Path(newBuildsLogsPath).mkdir(parents=True, exist_ok=True)
        pathlib.Path(existingBuildsLogsPath).mkdir(parents=True, exist_ok=True)
    except Exception as error:
        log.error(
            "There was a problem making folders or logs in Builds " + str(error))
        log.error(traceback.format_exc())
        raise error

    # Assumes start_project was called before now, so project folder exists in Builds/
    # OG not sure what the Sequence_Repository link be used for, but the plan requires it.
    try:
        path_to_source = 'Sequences/' + sequenceID
        path_to_dest_dir = 'Builds/' + projectID
        log.debug(
            "About to make a relative symbolib link.  Here are the arguments : ")
        log.debug("path_to_source : " + path_to_source)
        log.debug("path_to_dest_dir : " + path_to_dest_dir)
        log.debug("servicePath : " + str(servicePath))
        commonlogic.make_relative_symbolic_link(
            path_down_to_source=path_to_source,
            path_down_to_dest_dir=path_to_dest_dir,
            dest_link_label="Sequence_Repository",
            parent_directory=servicePath)
    except Exception as error:
        #log.error("There was a problem making Sequence_Repository link " + str(error))
        log.error("There was a problem making Sequence_Repository link ")
        log.error(traceback.format_exc())
        raise error


def main():
    log.info("main() was called.\n")


if __name__ == "__main__":
    main()
