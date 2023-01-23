#!/usr/bin/env python3
import json
import sys
import os
import re
#import importlib.util
import shutil
import uuid
import gemsModules.deprecated
import gmml
import traceback
import gemsModules.deprecated.common.utils
from multiprocessing import Process
from gemsModules.deprecated.project import projectUtilPydantic as projectUtils
from gemsModules.deprecated.project import settings as projectSettings
from gemsModules.deprecated.sequence import io as sequenceio
from gemsModules.deprecated.common import io as commonio
from gemsModules.deprecated.common import logic as commonLogic
from gemsModules.deprecated.common import services as commonservices

from gemsModules.deprecated.common.logic import writeStringToFile
from gemsModules.deprecated.common.loggingConfig import loggers, createLogger

from gemsModules.deprecated.sequence import projects as sequenceProjects
from gemsModules.deprecated.sequence import settings as sequenceSettings

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


def buildEach3DStructureInStructureInfo(thisTransaction: sequenceio.Transaction):
    log.info("buildEach3DStructureInStructureInfo() was called.")
    needToInstantiateCarbohydrateBuilder = True
    from multiprocessing import Process
    # get info from the transaction and check sanity
    log.debug("About to get build informaion from the transaction")
    log.debug("Working on the Build States now.")
    buildStatesOK = True
    theseBuildStates = thisTransaction.getIndividualBuildDetailsOut()
    if theseBuildStates is None:
        buildStatesOK = False
    if theseBuildStates is []:
        buildStatesOK = False
    if buildStatesOK is False:
        log.error(
            "Got all the way to buildEach3DStructureInStructureInfo without any buildStates")
        thisTransaction.generateCommonParserNotice(
            noticeBrief='GemsError',
            additionalInfo={"hint": "No buildStates accessible from structureBuildDetails"})
        return

    log.debug("Working on getting other data now.")
    try:
        theStructureBuildInfo = thisTransaction.getStructureBuildInfoOut()
        if theStructureBuildInfo.indexOrderedSequence == "":
            theStructureBuildInfo.setSequence(
                thisTransaction.getSequenceVariantOut('indexOrdered'))
            theStructureBuildInfo.setSeqId(
                theStructureBuildInfo.indexOrderedSequence)
        thisBuildStrategyID = theStructureBuildInfo.getBuildStrategyID()
        thisSeqID = thisTransaction.getSeqIdOut()
        if thisSeqID != theStructureBuildInfo.getSeqId():
            error = "Seq IDs do not match in project and build details."
            log.error("error")
            log.error("     project  : " + str(thisSeqID))
            log.error("     build details  : " +
                      str(theStructureBuildInfo.getSeqId()))
            return
        thisPuuID = thisTransaction.getPuuIDOut()
        thisProjectDir = thisTransaction.getProjectDirOut()
    except Exception as error:
        log.error(
            "Something went wrong getting the other data.  The following is from Python.")
        log.error(error)
        raise error

    thisProject = thisTransaction.transaction_out.project
    thisServiceDir = thisProject.service_dir

    for buildState in theseBuildStates:
        log.debug("Checking if a structure has been built in this buildState: ")
        log.debug("buildState: ")
        log.debug(buildState.json(indent=2))
        # May return "default" or a conformerID
        subDirectory = buildState.structureDirectoryName

        if sequenceProjects.structureExists(buildState, thisTransaction, thisBuildStrategyID):
            # Nothing in Sequence/ needs to change. In Builds/ProjectID/
            # add symLink in Existing to Sequences/SequenceID/defaults/All_builds/conformerID.
            log.debug("Found an existing structure for " + subDirectory)
            buildDir = "Existing_Builds/"
            sequenceProjects.addBuildFolderSymLinkToExistingConformer(
                thisServiceDir, thisSeqID, thisBuildStrategyID, thisPuuID, subDirectory)
        else:  # Doesn't already exist.
            log.debug("Need to build this structure: " + subDirectory)
            if needToInstantiateCarbohydrateBuilder:
                # Only ever do this once.
                needToInstantiateCarbohydrateBuilder = False
                # ## the following should probably use the indexOrdered sequence, but that doesn't work...
                inputSequence = thisTransaction.getSequenceVariantOut(
                    'indexOrdered')
                log.debug("About to getCbBuilderForSequence: " + inputSequence)
                builder = getCbBuilderForSequence(inputSequence)
            buildDir = "New_Builds/"
            buildState.setIsNewBuild(True)
            outputDirPath = buildState.getAbsoluteConformerPath()
            sequenceProjects.createConformerDirectoryInBuildsDirectory(
                thisProjectDir, subDirectory)
            # TODO - one day, the path on a compute node might differ from the website path
            log.debug("Absolute Conformer Path for this New Build: " +
                      buildState.getAbsoluteConformerPath())
            theJsonObject = buildState.json(indent=2)
            log.debug(
                "The build state for this New Build, after initializing, is  ")
            log.debug(theJsonObject)
            try:
                writeStringToFile(
                    theJsonObject,
                    os.path.join(
                        outputDirPath,
                        'info.json')
                )
            except Exception as error:
                log.error(
                    "There was an error writing the build state to a file: ")
                raise error
            build3DStructure(buildState, thisTransaction,
                             outputDirPath, builder)
            if thisTransaction.transaction_in.mdMinimize is True:
                sequenceProjects.addSequenceFolderSymLinkToNewBuild(
                    thisServiceDir, thisSeqID, thisBuildStrategyID, thisPuuID, subDirectory)

        # buildDir is either New_Builds/ or Existing_Builds/
        sequenceProjects.createSymLinkInRequestedStructures(
            thisProjectDir, buildDir, subDirectory)
        # Needs to be Requested_Structres/. Need to add conformerID separately.
        # sequenceProjects.addResponse(buildState, thisTransaction, conformerID, buildState.conformerLabel)
        # This probably needs work
        sequenceProjects.registerBuild(buildState, thisTransaction)

# TODO: Replace this with more generically useful: build3DStructure(transaction, service)
# Needs to work whether default structure or specific rotamers are requested.

# @brief Creates a jobsubmission for Amber. Submits that. Updates the transaction to reflect this.
#   @param Transaction thisTransaction
#   @param Service service (optional)


def build3DStructure(buildState: sequenceio.Single3DStructureBuildDetails, thisTransaction: sequenceio.Transaction, outputDirPath: str, builder):
    log.info("build3DStructure() was called.")
    log.debug("outputDirPath: " + outputDirPath)
    log.debug("the build state is: ")
    log.debug(buildState)
    try:
        pUUID = projectUtils.getProjectpUUID(
            thisTransaction.transaction_out.project)
        ##sequence = getSequenceFromTransaction(thisTransaction)
    except Exception as error:
        log.error(
            "Problem finding the project pUUID in the transaction: " + str(error))
        raise error

    # TODO: figure out how to return this response now, and still continue this logic.
    #  ...use 'yield'...
    # log.debug("About to getCbBuilderForSequence")
    # builder = getCbBuilderForSequence(sequence)
    thisEvaluation = thisTransaction.transaction_out.entity.outputs.sequenceEvaluationOutput
    thisBuildOptions = thisEvaluation.buildOptions
    if thisBuildOptions is None:
        thisBuildOptions = sequenceio.TheBuildOptions()
    gmmlConformerInfo = populateGMMLConformerInfoStruct(buildState)
    try:
        # If this is default, set the output path, otherwise use what was passed in.
        if buildState.isDefaultStructure:
            log.debug("Generating default structure in: " + outputDirPath)
            # Using multiprocessing for this function call.
            builder.GenerateSingle3DStructureDefaultFiles(outputDirPath)
            if not builder.IsStatusOk():
                log.error(carbBuilder.GetStatusMessage())
                log.debug(
                    "Just about to call generateCommonParserNotice with the outgoing project.  The transaction_out is :   ")
                log.debug(thisTransaction.transaction_out.json(indent=2))
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='InvalidInputPayload', exitMessage=carbBuilder.GetStatusMessage())
                thisTransaction.build_outgoing_string()
                return thisTransaction # do this or no?
            #p = Process(target=builder.GenerateSingle3DStructureDefaultFiles, args=(outputDirPath,))
            # p.start()
        else:
            log.debug(
                "The request is for a conformer with outputDirPath: " + outputDirPath)
            # Need to put the info into the GMML struct: SingleRotamerInfoVector
#            gmmlConformerInfo = populateGMMLConformerInfoStruct(buildState)
            builder.GenerateSpecific3DStructure(
                gmmlConformerInfo, outputDirPath)
            if not builder.IsStatusOk():
                log.error(carbBuilder.GetStatusMessage())
                log.debug(
                    "Just about to call generateCommonParserNotice with the outgoing project.  The transaction_out is :   ")
                log.debug(thisTransaction.transaction_out.json(indent=2))
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='InvalidInputPayload', exitMessage=carbBuilder.GetStatusMessage())
                thisTransaction.build_outgoing_string()
                return thisTransaction # do this or no?
            #p = Process(target=builder.GenerateSpecific3DStructure, args=(gmmlConformerInfo, outputDirPath,))
            # p.start()
    except Exception as error:
        log.error("There was a problem generating this build: " + str(error))
        raise error
    if thisBuildOptions.mdMinimize is False:
        log.debug("mdMinimize is false and this is the gmmlConformerInfo : ")
        log.debug(gmmlConformerInfo)
        return gmmlConformerInfo

    # Generate JSOn to tell mmservice/amber that there is a job to do
    # TODO  make filling this in use a class in amber/io.py
    amberSubmissionJson = '{ \
    "molecularSystemType":"Glycan", \
    "molecularModelingJobType":"Prep_and_Minimization", \
    "jobID":"' + pUUID + '", \
    "localWorkingDirectory":"' + outputDirPath + '", \
    "comment":"initiated by gemsModules/sequence"\
    }'
    log.debug(amberSubmissionJson)
    from gemsModules.deprecated.mmservice.amber.amber import manageIncomingString
    # Using multiprocessing for this function call.
    manageIncomingString(amberSubmissionJson)
    return gmmlConformerInfo

# This poor code is a result of how the combinations are generated in
# structureinfo.generateCombinationsFromRotamerData().


def populateGMMLConformerInfoStruct(buildState: sequenceio.Single3DStructureBuildDetails):
    log.info("populateGMMLConformerInfoStruct() was called.")
# example buildState.sequenceConformation:
# ('6', 'h', '-g', '6', 'o', 'gg', '9', 'h', '-g', '9', 'o', 'gg', '10', 'o', 'gg', '13', 'h', '-g', '13', 'o', 'gg', '14', 'o', 'tg', '16', 'h', '-g', '16', 'o', 'tg')
    try:
        gmmlConformerInfo = gmml.single_rotamer_info_vector()
        log.debug("buildState.sequenceConformation, is : ")
        log.debug(buildState.sequenceConformation)
        for rotList in divideListIntoChunks(buildState.sequenceConformation, 3):
            singleRotamerInfo = gmml.SingleRotamerInfo()
            singleRotamerInfo.linkageIndex = rotList[0]
            singleRotamerInfo.dihedralName = rotList[1]
            singleRotamerInfo.selectedRotamer = rotList[2]
            gmmlConformerInfo.push_back(singleRotamerInfo)
            # singleRotamerInfo.numericValue = conf['numericValue'] # Not supported at GMML or gems level yet.
            log.debug(
                "LinkageLabel: " + rotList[0] + ", dihedralName: " + rotList[1] + ", rotamer: " + rotList[2])
    except Exception as error:
        log.error("Could not populateGMMLConformerInfoStruct: " + str(error))
        raise error
    log.debug("About to return a gmmlConformerInfo and it is :  >>>" +
              str(gmmlConformerInfo) + "<<<")
    return gmmlConformerInfo


def divideListIntoChunks(l, n):
    log.debug("l is this thing:  " + repr(l))
    log.debug("l is this content : " + str(l))
    log.debug("n is this thing:  " + repr(n))
    log.debug("n is this content : " + str(n))
    for i in range(0, len(l), n):
        yield l[i:i + n]

# @brief Pass a sequence string, get a builder for that sequence.
# @param String sequence - GLYCAM Condensed string sequence.
#   @return CarbohydrateBuilder object from gmml.


def getCbBuilderForSequence(sequence: str):
    log.info("getCbBuilderForSequence() was called.\n")
    GemsPath = commonservices.getGemsHome()
    log.debug("GemsPath: " + GemsPath)

    prepfile = GemsPath + "/gmml/dat/prep/GLYCAM_06j-1_GAGS.prep"
    if os.path.exists(prepfile):
        log.debug("Instantiating the carbohydrateBuilder.")
        builder = gmml.carbohydrateBuilder(sequence, prepfile)
        return builder
    else:
        log.error("Prepfile did not exist at: " + prepfile)
        raise FileNotFoundError


def main():
    log.info("buildFromSequence.py was called.")
    log.info("The main function in buildFromSequence.py doesn't do anything.")


if __name__ == "__main__":
    main()
