#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import gemsModules
import gmml
import traceback
import gemsModules.common.utils
from multiprocessing import Process
from gemsModules.project.projectUtil import *
from gemsModules.project import settings as projectSettings
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonLogic
from gemsModules.delegator import io as delegatorio
from gemsModules.sequence import io as sequenceIO
#from gemsModules.common.services import *
#from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *

from gemsModules.sequence import projects as sequenceProjects

from . import settings as sequenceSettings
from .structureInfo import *
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)



##  @brief Give a transaction and pUUID, and this method builds the json response and
#   appends that to the transaction.
#   @param Transaction thisTransaction
#   @param String uUUID - Upload ID for user provided input.
def appendBuild3DStructureResponse(thisTransaction : Transaction, pUUID : str):
    log.info("appendBuild3DStructureResonse() was called.")
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    if not 'entity' in thisTransaction.response_dict:
        thisTransaction.response_dict['entity']={}
    if not 'type' in thisTransaction.response_dict['entity']:
        thisTransaction.response_dict['entity']['type']='Sequence'
    if not 'responses' in thisTransaction.response_dict:
        thisTransaction.response_dict['responses']=[]

    downloadUrl = getDownloadUrl(pUUID, "cb")
    thisTransaction.response_dict['responses'].append({
        'Build3DStructure': {
            'payload': pUUID ,
            'downloadUrl': downloadUrl
        }
    })


def buildEach3DStructureInStructureInfo(structureInfo : StructureInfo, buildStrategyID : str, thisTransaction : Transaction, this_seqID : str, this_pUUID : str, projectDir : str):
    needToInstantiateCarbohydrateBuilder = True
    from multiprocessing import Process
    for buildState in structureInfo.buildStates:
        log.debug("Checking if a structure has been built in this buildState: ")
        log.debug("buildState: " + repr(buildState))
        conformerID = buildState.structureDirectoryName # May return "default" or a conformerID
        ##  check if requested structures exitst, update structureInfo_status.json and project when exist
        if sequenceProjects.structureExists(buildState, thisTransaction, buildStrategyID):
            ## Nothing in Sequence/ needs to change. In Builds/ProjectID/
            ## add symLink in Existing to Sequences/SequenceID/defaults/All_builds/conformerID.
            log.debug("Found an existing structure for " + conformerID)
            buildDir = "Existing_Builds/"
            sequenceProjects.addBuildFolderSymLinkToExistingConformer(this_seqID, buildStrategyID, this_pUUID, conformerID)
        else: # Doesn't already exist.
            log.debug("Need to build this structure: " + conformerID )
            if needToInstantiateCarbohydrateBuilder:
                needToInstantiateCarbohydrateBuilder = False # Only ever do this once.
                log.debug("About to getCbBuilderForSequence")
                inputSequence = getSequenceFromTransaction(thisTransaction)          
                builder = getCbBuilderForSequence(inputSequence)
            buildDir = "New_Builds/"
            sequenceProjects.createConformerDirectoryInBuildsDirectory(projectDir, conformerID)
            ## TODO - one day, the path on a compute node might differ from the website path
            outputDirPath = os.path.join(projectDir, buildDir, conformerID)
            log.debug("outputDirPath: " + outputDirPath)
            #from multiprocessing import set_start_method
            #set_start_method("spawn")
            #d = Process(target=build3DStructure, args=(buildState, thisTransaction, outputDirPath, builder))
           # d.start()
            build3DStructure(buildState, thisTransaction, outputDirPath, builder)
            sequenceProjects.addSequenceFolderSymLinkToNewBuild(this_seqID, buildStrategyID, this_pUUID, conformerID)        
            if conformerID == "default": # And doesn't already exist.
                #sequenceProjects.createDefaultSymLinkSequencesDirectory(this_seqID, conformerID, buildStrategyID)
                sequenceProjects.createDefaultSymLinkBuildsDirectory(projectDir, buildDir + conformerID)
        # buildDir is either New_Builds/ or Existing_Builds/
        sequenceProjects.createSymLinkInRequestedStructures(projectDir, buildDir, conformerID)
        # Needs to be Requested_Structres/. Need to add conformerID separately.
        # sequenceProjects.addResponse(buildState, thisTransaction, conformerID, buildState.conformerLabel)
        # This probably needs work    
        sequenceProjects.registerBuild(buildState, thisTransaction)

##TODO: Replace this with more generically useful: build3DStructure(transaction, service)
##      Needs to work whether default structure or specific rotamers are requested.

##  @brief Creates a jobsubmission for Amber. Submits that. Updates the transaction to reflect this.
#   @param Transaction thisTransaction
#   @param Service service (optional)
def build3DStructure(buildState : BuildState, thisTransaction : Transaction, outputDirPath : str, builder):
    log.info("build3DStructure() was called.")
    log.debug("outputDirPath: " + outputDirPath)
    try:
        pUUID = sequenceProjects.getProjectpUUID(thisTransaction)
        ##sequence = getSequenceFromTransaction(thisTransaction)
    except Exception as error:
        log.error("Problem finding the project pUUID in the transaction: " + str(error))
        raise error
    
    ##TODO: figure out how to return this response now, and still continue this logic.
    # log.debug("About to getCbBuilderForSequence")
    # builder = getCbBuilderForSequence(sequence)
    try:
        ## If this is default, set the output path, otherwise use what was passed in.
        if buildState.isDefaultStructure:
            log.debug("Generating default in: " + outputDirPath)
            ## Using multiprocessing for this function call.
            builder.GenerateSingle3DStructureDefaultFiles(outputDirPath)
            #p = Process(target=builder.GenerateSingle3DStructureDefaultFiles, args=(outputDirPath,))
            #p.start()
        else:
            log.debug("The request is for a conformer with outputDirPath: " + outputDirPath)
                ## Need to put the info into the GMML struct: SingleRotamerInfoVector
            gmmlConformerInfo = populateGMMLConformerInfoStruct(buildState)
            builder.GenerateSpecific3DStructure(gmmlConformerInfo, outputDirPath)
            #p = Process(target=builder.GenerateSpecific3DStructure, args=(gmmlConformerInfo, outputDirPath,))
            #p.start()
    except Exception as error:
        log.error("There was a problem generating this build: " + str(error))
        raise error
    ## Generate JSOn to tell mmservice/amber that there is a job to do
    ## TODO  make filling this in use a class in amber/io.py 
    amberSubmissionJson='{ \
    "molecularSystemType":"Glycan", \
    "molecularModelingJobType":"Prep_and_Minimization", \
    "jobID":"' + pUUID + '", \
    "localWorkingDirectory":"' + outputDirPath + '", \
    "comment":"initiated by gemsModules/sequence"\
    }'
    log.debug(amberSubmissionJson)
#    # TODO:  Make this resemble real code....
#    ##  Moving this to mmservice/amber/amber.py
#    the_json_file = outputDirPath + "/amber_submission.json"
#    min_json_in = open (the_json_file , 'w')
#    min_json_in.write(amberSubmissionJson)
#    min_json_in.close()

    from gemsModules.mmservice.amber.amber import manageIncomingString
    ## Using multiprocessing for this function call.
    manageIncomingString(amberSubmissionJson)
    #p = Process(target=manageIncomingString, args=(amberSubmissionJson,))
    #p.start()
    ## everything up to here -- all the amber stuff --
    ## is what needs to move

##  @brief Pass a BuildState, get a gmml level struct with conformer information.
##  @param BuildState. Information to generate a specific, single 3D shape.
#   @return SingleRotamerInfoVector object from gmml.
# def populateGMMLConformerInfoStruct(buildState : BuildState):
#     log.info("populateGMMLConformerInfoStruct() was called.")
#     try:
#         gmmlConformerInfo = gmml.single_rotamer_info_vector()
#         for conf in buildState.sequenceConformation:
#             singleRotamerInfo = gmml.SingleRotamerInfo()
#             singleRotamerInfo.linkageIndex = conf['linkageLabel'] # This is a bad gems name. Notes in RotamerConformation class.
#             singleRotamerInfo.linkageName = conf['linkageLabel'] # This is a better match, but GMML probably doesn't need to know user labels.
#             singleRotamerInfo.dihedralName = conf['dihedralName']
#             singleRotamerInfo.selectedRotamer = conf['rotamer']
#             gmmlConformerInfo.push_back(singleRotamerInfo)
#             #singleRotamerInfo.numericValue = conf['numericValue'] # Not supported at GMML or gems level yet.
#             #log.debug("LinkageLabel: " + conf['linkageLabel'] + ", dihedralName: " + conf['dihedralName'] + ", rotamer: " + conf['rotamer'])
#             #print(conf)
#     except Exception as error:
#         log.error("Could not populateGMMLConformerInfoStruct: " + str(error) )
#         raise error
#     else:
#         return gmmlConformerInfo

# This poor code is a result of how the combinations are generated in 
# structureinfo.generateCombinationsFromRotamerData().
def populateGMMLConformerInfoStruct(buildState : BuildState):
    log.info("populateGMMLConformerInfoStruct() was called.")
# example buildState.sequenceConformation:
# ('6', 'h', '-g', '6', 'o', 'gg', '9', 'h', '-g', '9', 'o', 'gg', '10', 'o', 'gg', '13', 'h', '-g', '13', 'o', 'gg', '14', 'o', 'tg', '16', 'h', '-g', '16', 'o', 'tg')
    try:
        gmmlConformerInfo = gmml.single_rotamer_info_vector()
        for rotList in divideListIntoChunks(buildState.sequenceConformation, 3):
            singleRotamerInfo = gmml.SingleRotamerInfo()
            singleRotamerInfo.linkageIndex = rotList[0]
            singleRotamerInfo.dihedralName = rotList[1]
            singleRotamerInfo.selectedRotamer = rotList[2]
            gmmlConformerInfo.push_back(singleRotamerInfo)
            #singleRotamerInfo.numericValue = conf['numericValue'] # Not supported at GMML or gems level yet.
            log.debug("LinkageLabel: " + rotList[0] + ", dihedralName: " + rotList[1] + ", rotamer: " + rotList[2])
    except Exception as error:
        log.error("Could not populateGMMLConformerInfoStruct: " + str(error) )
        raise error
    return gmmlConformerInfo

def divideListIntoChunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

##  @brief Pass a sequence string, get a builder for that sequence.
##  @param String sequence - GLYCAM Condensed string sequence.
#   @return CarbohydrateBuilder object from gmml.
def getCbBuilderForSequence(sequence : str):
    log.info("getCbBuilderForSequence() was called.\n")
    GemsPath = getGemsHome()
    log.debug("GemsPath: " + GemsPath )

    prepfile = GemsPath + "/gemsModules/sequence/GLYCAM_06j-1.prep"
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
