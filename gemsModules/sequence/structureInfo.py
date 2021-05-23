#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.schema import schema
from gemsModules.sequence import io as sequenceio
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.common.loggingConfig import *
from gemsModules.project import projectUtilPydantic as projectUtils
from gemsModules.project import settings as projectSettings
import gmml, os, sys
import itertools
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  @brief Pass in a sequence (list of rotamerConformations), get a terse label.
#   @detail Translate the more verbose sequenceConf object into a terse string that is useful
#           for naming directories and describing interesting geometry in a build.
#   @param sequenceConf List[rotamerConformation]
#   @return string conformerLabel
def buildConformerLabel(rotamerCombo): ## Added by Oliver 
    log.info("buildConformerLabel() was called.\n\n")
    conformerLabel = ""
    currentLinkage = ""
    #log.debug("this sequenceConf: \n" + str(sequenceConf))

    for item in rotamerCombo:
        ## Decide whether or not to add the label.
        if conformerLabel == "": # first loop
            currentLinkage = item
            conformerLabel += item
        elif item.isdigit(): ## Assumes only linkages are ints, and not negative.
            conformerLabel += "_"
            if item != currentLinkage: # new linkage
                conformerLabel += item
                currentLinkage = item
        else:
            conformerLabel += item
    return conformerLabel


def convertDihedralNameToCode(dihedralName : str):
    dihedralName = dihedralName.replace("omega", "omg")
    dihedralName = dihedralName.replace("Omg", "omg")
    dihedralName = dihedralName.replace("Phi", "phi")
    dihedralName = dihedralName.replace("Psi", "psi")
    if dihedralName == "phi":
        return "h"
    elif dihedralName == "psi":
        return "s"
    elif dihedralName == "omg":
        return "o"
    elif dihedralName == "omg7":
        return "o7"
    elif dihedralName == "omg8":
        return "o8"
    elif dihedralName == "omg9":
        return "o9"
    elif dihedralName == "chi1":
        return "c1" # Cannot use numbers.
    elif dihedralName == "chi2":
        return "c2" # Cannot use numbers.

    else:
        log.debug("Unrecognized dihedralName: " + str(dihedralName)) 

##  @brief  Gets the shape from the user request in transactions or returns default.
#   @param Transaction
#   @return String solvent_shape
def getSolvationShape(thisTransaction):
    log.info("getSolvationShape() was called.")
    return "REC"
    # This info currently lives in sequence.io.Single3DStructureBuildDetails

##  @brief Look at the transaction to see if a force field is specified
#   @param Transaction thisTransaction
#   @return String either "default" or the force field name.
def countNumberOfShapes(rotamerData : []):
    log.info("countNumberOfShapes was called.")
    count = 1
    for linkage in rotamerData.singleLinkageRotamerDataList:
        log.debug("The linkage is: ")
        log.debug(linkage)
        for dihedral in linkage.selectedRotamers:
            log.debug("The dihedral is: ")
            log.debug(dihedral)
            count *= len(dihedral.dihedralValues)
    log.debug("the total count is: " + str(count))
    return count
def countNumberOfShapesUpToLimit(rotamerData : [], hardLimit = 1):
    log.info("countNumberOfShapesUpToLimit was called.")
    count = countNumberOfShapes(rotamerData)
    if hardLimit != -1 : 
        if count >= hardLimit: 
            return hardLimit
    return count

##  @brief Parses user's selected rotamers (rotamerData) into a list of 
#           structures to request.
#   @detail With a limit of 64 structures to request at a time, users select
#           each rotamer they want for each linkage. This code creates the 
#           list of unique permutations possible for those selections.
#   @param Transaction 
#   @TODO: Move this to a better file for this stuff.
def buildStructureInfoOliver(thisTransaction : sequenceio.Transaction):
    log.info("buildStructureInfoOliver() was called.")

    structureInfo = sequenceio.StructureBuildInfo()
    try:
        structureInfo.incomingSequence = thisTransaction.getInputSequencePayload()
        structureInfo.indexOrderedSequence = thisTransaction.getSequenceVariantOut('indexOrdered')
        if structureInfo.indexOrderedSequence is None :
            error="Unable to find indexOrderedSequence.  Was the sequence evaluated?"
            log.error(errof)
            thisTransaction.generateCommonParserNotice(
                    noticeBrief='GemsError',
                    additionalInfo={"hint":error})
            return
        log.debug("indexOrderedSequence: " + str(structureInfo.indexOrderedSequence))
        structureInfo.setSeqID()
#        structureInfo.sequence = sequence
        ##TODO: Also grab the following from the request, or set defaults:
        ##    buildType, ions, forceField, date.
    except Exception as error:
        log.error("There was a problem getting the sequence from the transaction: " + str(error))
        log.error(traceback.format_exc())
        raise error
    try:
        #RotamerData is the list of dict objects describing each linkage
        #rotamerData = getRotamerDataFromTransaction(thisTransaction)
        rotamerDataIn = thisTransaction.getRotamerDataIn()
        log.debug("Found rotamerData in the input, and it is : ")
        log.debug(rotamerDataIn)
    except Exception as error:
        log.error("There was a problem checking for input rotamerData from the transaction: " + str(error))
        log.error(traceback.format_exc())
        raise error
        
    ## Need to be able to handle the default, 
    ##     ... so it needs rotamerData.
    ## Oliver has decided to always request a default for symlinking ease.
    ## Lachele sees this decision and raises an explicit conformer
    ##
    # If there was an explicit request for multiple builds in the 
    # incoming request, then do whatever was requested - UNLESS
    # this is being run from the website.  In that case, enforce a
    # hard limit of 64 onto the number of structures.
    doSingleDefaultOnly = False  # this is probably not needed
    maxNumberOfStructuresToBuild=thisTransaction.getNumberStructuresHardLimitIn()
    if maxNumberOfStructuresToBuild is None :
        maxNumberOfStructuresToBuild = -1
    if thisTransaction.getIsEvaluationForBuild() is False :
        log.debug("transaction says this is not an evaluation for a build")
        maxNumberOfStructuresToBuild = 1
        doSingleDefaultOnly = True

    maxHardLimit = -1
    transactionContext = os.environ.get('GW_GRPC_ROLE')
    log.debug("transactionContext is : " + str(transactionContext))
    # TODO - make these limits configurable via environment variable
    # TODO - This impacts the frontend. Make an appropriate plan. FE devs need to know this too.
    if transactionContext == 'Developer' : 
        maxHardLimit = 8
    if transactionContext == 'Swarm' :
        maxHardLimit = 64

    log.debug("The max number structs to build (1) is :  " + str(maxNumberOfStructuresToBuild) )
    log.debug("The max hard limit (1) is :  " + str(maxHardLimit) )
    thisTransaction.setNumberStructuresHardLimitOut(maxHardLimit)

    if maxHardLimit != -1 :
        if maxHardLimit < maxNumberOfStructuresToBuild :
            maxNumberOfStructuresToBuild = maxHardLimit
        if maxNumberOfStructuresToBuild == -1 :
            maxNumberOfStructuresToBuild = maxHardLimit

    log.debug("The max number structs to build (2) is :  " + str(maxNumberOfStructuresToBuild) )
    if rotamerDataIn is None :
        rotamerData = thisTransaction.getRotamerDataOut()
        for rotamer in rotamerData.singleLinkageRotamerDataList :
            rotamer.selectedRotamers = rotamer.likelyRotamers
    else :
        rotamerData = rotamerDataIn

    log.debug("The max number structs to build (3) is :  " + str(maxNumberOfStructuresToBuild) )
    if rotamerData is None :
        rotamerData = AllLinkageRotamerData()
        rotamerData.totalPossibleRotamers = 1
        rotamerData.totalLikelyRotamers = 1
        rotamerData.totalSelectedRotamers = 1

    log.debug("The max number structs to build (4) is :  " + str(maxNumberOfStructuresToBuild) )
    if rotamerData.totalPossibleRotamers == 1 : 
        log.debug("totalPossibleRotamers: 1")
        buildState = sequenceio.Single3DStructureBuildDetails()
        buildState.conformerLabel = "structure"
        buildState.structureDirectoryName = "structure"
        buildState.conformerID = buildState.structureDirectoryName
        buildState.isDefaultStructure = True
        buildState.date = datetime.now()
        structureInfo.individualBuildDetails.append(buildState)
        log.debug("returning structureInfo: " + repr(structureInfo))
        return structureInfo 

    log.debug("The max number structs to build is :  " + str(maxNumberOfStructuresToBuild) )

    if doSingleDefaultOnly is True :
        if maxNumberOfStructuresToBuild != 1 :
            log.error("Mismatch between doSingleDefaultOnly and maxNumberOfStructuresToBuild")

    downloadUrlPath = thisTransaction.transaction_out.project.getDownloadUrlPath()
    ## Presence of incoming rotamerData indicates specific rotamer requests.
    firstStructure=True
    if rotamerData != None:
        from urllib.parse import urljoin
        #Just get all this info once and append to each buildstate in the loop below
        simulationPhase = checkForSimulationPhase(thisTransaction)
        log.debug("simulationPhase: " + simulationPhase)
        solvationShape = None
        if simulationPhase == "solvent":
            # ## TODO - move this to a method of Transaction
            solvationShape = getSolvationShape(thisTransaction)
        date = datetime.now()
        log.debug("date: " + str(date))
        addIons = checkForAddIons(thisTransaction)
        log.debug("\nrotamerData:\n" + str(rotamerData))
        # Now convert the rotamerData object into a List for itertools to work on.
        sequenceRotamerCombos = generateCombinationsFromRotamerData(
                rotamerData,
                maxNumberCombos = maxNumberOfStructuresToBuild)
        log.debug("Here are the sequence rotamer combos: ")
        log.debug(sequenceRotamerCombos)
        # Now put add these combos to individual build states with other info
        for rotamerCombo in sequenceRotamerCombos:
            buildState = sequenceio.Single3DStructureBuildDetails()
            buildState.sequenceConformation = rotamerCombo
            buildState.conformerLabel = buildConformerLabel(rotamerCombo)
            log.debug("The build state after setting conformerLabel is : ")
            log.debug(buildState.json(indent=2))
            if firstStructure is True :
                buildState.isDefaultStructure = True
                firstStructure = False
            log.debug("label is :" + buildState.conformerLabel)
            if len(buildState.conformerLabel) > 32 :
                log.debug("conformerLabel is long so building a UUID for structureDirectoryName")
                buildState.structureDirectoryName = getUuidForString(buildState.conformerLabel)
                log.debug("The structureDirectoryName/UUID is : " + buildState.structureDirectoryName)
            else:
                log.debug("conformerLabel is short so using it for structureDirectoryName")
                buildState.structureDirectoryName = buildState.conformerLabel 
                log.debug("The structureDirectoryName is : " + buildState.structureDirectoryName)
            buildState.simulationPhase = simulationPhase
            if solvationShape != None:
                buildState.solventShape = solventShape
            buildState.date = date
            buildState.addIons = addIons
            buildState.conformerID = buildState.structureDirectoryName
            buildState.downloadUrl = urljoin(downloadUrlPath, buildState.conformerLabel)

            structureInfo.individualBuildDetails.append(buildState)
    else:
        log.debug("rotamerData is None.") 

    log.debug("returning structureInfo: " + repr(structureInfo))  
    return structureInfo

def generateCombinationsFromRotamerData(rotamerData, maxNumberCombos=1):
    # First convert into a nested list for itertools to work with
    log.info("generateCombinationsFromRotamerData was called.")
    rotamerDataList = []
    for linkage in rotamerData.singleLinkageRotamerDataList:
        log.debug("the linkage is: ")
        log.debug(linkage)
        #linkageIndex = str(linkage.linkageLabel)
        linkageIndex = str(linkage.indexOrderedLabel)
        log.debug("the linkage label is: " + str(linkageIndex))
        dihedrals = []
        for dihedral in linkage.selectedRotamers:
            log.debug("the dihedral is: ")
            log.debug(dihedral)
            dihedralCodeName = convertDihedralNameToCode(dihedral.dihedralName)
            log.debug("the dihedralCodeName is: " + dihedralCodeName)
            rotamers = []
            for rotamer in dihedral.dihedralValues:
                rotamers.extend([rotamer])
            rotamerDataList.extend([[linkageIndex], [dihedralCodeName], rotamers])
    maxStructures = countNumberOfShapesUpToLimit(rotamerData , hardLimit = maxNumberCombos)
    # The inner .product function is what creates the combinations. The islice limits the number.
    log.debug("The rotamerDataList is : ")
    log.debug(rotamerDataList)
    theResult = list(itertools.islice(itertools.product(*rotamerDataList), maxStructures))
    log.debug("theResult is : " + str(theResult))
    return theResult

##  @brief creates the files needed to track a request for various builds of a sequence.
#   @detail Updates existing files if they already exist.
#   @param structureInfo
#   @param projectDir
def saveRequestInfo(structureInfo, projectDir):
    log.info("saveRequestInfo() was called.")
    log.debug("projectDir: " + projectDir)
    
    ## convert the object to dict
    try:
        if "dict" == str(type(structureInfo)):
            data = structureInfo
        else:
            data = convertStructureInfoToDict(structureInfo)
            log.debug("structureInfo as dict: \n\n")
        
        prettyPrint(data)

    except Exception as error:
        log.error("There was a problem converting the structureInfo to dict: " + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        ## dump to request file
        try:
            fileName = projectDir + "logs/structureInfo_request.json"
            log.debug("Attempting to write: " + fileName)
            with open(fileName, 'w') as outFile:
                jsonString = json.dumps(data, indent=4, sort_keys=False, default=str)
                log.debug("jsonString: \n" + jsonString )
                outFile.write(jsonString)
        except Exception as error:
            log.error("There was a problem writing structureInfo_request.json to file: " + str(error))
            log.error(traceback.format_exc())
            raise error
        else:
             ## also dump to status file.
            try:
                statusFileName = projectDir + "logs/structureInfo_status.json"
                log.debug("Attempting to write: " + statusFileName)
                with open(statusFileName, 'w') as statusFile:
                    jsonString = json.dumps(data, indent=4, sort_keys=False, default=str)
                    log.debug("jsonString: \n" + jsonString )
                    statusFile.write(jsonString)
            except Exception as error:
                log.error("There was a problem writing structureInfo_status.json: " + str(error))
                log.error(traceback.format_exc())
                raise error


##  @brief Pass in structureInfo, get a dict in return.
#   @detail Since structureInfo objects have lists of objects with lists of objects, 
#   a bit of homework is saved by using this to convert to dict.
#def convertStructureInfoToDict(structureInfo):
def convertStructureInfoToDict(structureInfo : sequenceio.StructureBuildInfo()):
    log.info("convertStructureInfoToDict was called.")
    inputIsGood = True
    if structureInfo is None :
        inputIsGood = False
    if structureInfo is "" :
        inputIsGood = False
    if inputIsGood is False :
        error = "Bad data passed to convertStructureInfoToDict : " + str(structureInfo)
        log.error(error)
        raise error
    else : 
        return structureInfo.json(indent=2)

#    data = {}
#    ## set the sequence.
#    try:
#        data['sequence'] = structureInfo.sequence
#        data['buildStates'] = []
#    except Exception as error:
#        log.error("There was a problem finding the sequence in structureInfo: " + str(error))
#        log.error(traceback.format_exc())
#        raise error
#    else:
#        try:
#            if structureInfo.buildStates is not None:
#                ##Process the build states.
#                for buildState in structureInfo.buildStates:
#                    log.debug("buildState: \n" + repr(buildState))
#                    state = {}
##                    state['conformerLabel'] = buildState.conformerLabel
#                    state['simulationPhase'] = buildState.simulationPhase
#                    if buildState.simulationPhase == "solvent":
#                        state['solvationShape'] = buildState.solvationShape
#                    state['status'] = buildState.status
#                    state['date'] = str(buildState.date)
#                    state['addIons']  = buildState.addIons
#                    state['energy'] = buildState.energy
#                    state['forceField']  = buildState.forceField
#                    state['sequenceConformation'] = []
#                    try:
#                        if buildState.sequenceConformation is not None:
#                            log.debug("sequenceConformation: \n" + repr(buildState.sequenceConformation))
#                            for rotamerConf in buildState.sequenceConformation:
#                                log.debug("rotamerConf: \n" + repr(rotamerConf))
#                                state['sequenceConformation'].append(rotamerConf)
#                        else:
#                            log.debug("No sequence conformation. Must be a request for the default structure.")
#                    except Exception as error:
#                        log.error("There was a problem converting the sequence conformation to dict: " + str(error))
#                        log.error(traceback.format_exc())
#                        raise error
#                    else:
#                        data['buildStates'].append(state)
#            else: 
#                log.debug("There may be no build states in a default structure request.")
#        except Exception as error:
#            log.error("There was a problem building the states for this structureInfo: " + str(error))
#            log.error(traceback.format_exc())
#            raise error
#        else:
#            return data



##  @brief Checks a transaction for user requests that specify adding ions.
#   @detail Default value is "default" - which depends on other software's defauts.
#   @param Transaction
def checkForAddIons(thisTransaction: sequenceio.Transaction):
    log.info("checkForAddIons() was called.")

    result = "default"
    request = thisTransaction.request_dict
    if "project" in request.keys():
        if "ion" in request['project'].keys():
            result = request['project']['ion']
    
    ##If both a project and options exist, let the options override the
    #   project.
    if "options" in request.keys():
        if "add_ions" in request['options'].keys():
            result = request['options']['add_ions']

    return result


##  @brief Checks a transaction for user requests that specify simulation phase
#   @detail Default value is gas_phase
#   @param Transaction
def checkForSimulationPhase(thisTransaction: sequenceio.Transaction):
    log.info("checkForSimulationPhase() was called.")

    simulationPhase = "gas_phase"
    request = thisTransaction.request_dict
    if "project" in request.keys():
        if "solvation" in request['project'].keys():
            if request['project']['solvation'] == "yes":
                simulationPhase = "solvent"

    ##If both a project and options exist, let the options override the
    #   project.
    if "options" in request.keys():
        if "solvation" in request['options'].keys():
            if request['options']['solvation'] == "yes":
                simulationPhase = "solvent"

    return "gas_phase"


##  @brief Creates a record of a newly built structure in its seqID dir.
#   @detail structureInfo.json holds the master record of all builds for a given sequence. 
#           structureInfo_status.json holds the master record of all builds for a given project.
#           This method expects a file at a time to be passed in for updating.
#   @param structureInfoFilename String
def updateBuildStatus(structureInfoFilename : str, buildState : sequenceio.Single3DStructureBuildDetails, status : str):
    log.info("updateBuildStatus() was called.")
    log.debug("structureInfoFilename: " + structureInfoFilename)

    if "status" in structureInfoFilename:
        log.debug("Updating a project's  status file")
    else:
        log.debug("Updating an seqDir's structureInfo.json")
        ## Throw errors if the seqDir don't already exist.
        seqDir = structureInfoFilename.replace("structureInfo.json", "")
        log.debug("seqDir: " + seqDir)
        if os.path.exists(seqDir):
            log.debug("seqDir exists.")
        else:
            raise(FileNotFoundError(seqDir))

    if os.path.exists(structureInfoFilename):
        log.debug("Found the file.")
    else:
        raise(FileNotFoundError(structureInfoFilename))

    try:
        ##Load the object from the file.
        with open(structureInfoFilename, 'r') as inFile:
            data = json.load(inFile)
    except Exception as error:
        log.error("There was a problem reading the file " + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        try:
            log.debug("data before update:\n\n")
            prettyPrint(data)

            buildState.status = status
            log.debug("buildState: " + str(buildState))

            if len(data['buildStates']) == 0:
                log.debug("Adding the first build state.")
                record = prepareBuildRecord(buildState)
                data['buildStates'].append(record)
            else:
                log.debug("Builds exist. Checking if we are updating the status of an existing build.")
                log.debug("buildState: " + str(data['buildStates']))
                for recordedState in data['buildStates']:
                    log.debug("recordedState['conformerLabel']: " + recordedState['conformerLabel'])
                    log.debug("buildState.conformerLabel: " + buildState.conformerLabel)
                    if recordedState['conformerLabel'] == buildState.conformerLabel:
                        log.debug("Found the record to update. recordedState['status']: " + recordedState['status'])
                        recordedState['status'] = status
                        log.debug("updated recordedState['status']: " + recordedState['status'])

        except Exception as error:
            log.error("There was a problem updating the object: " + str(error))
            log.error(traceback.format_exc())
            raise error
        else:
            try:
                log.debug("Attempting to write the updated structureInfo data to file.")
                with open(structureInfoFilename, 'w') as outFile:
                    jsonString = json.dumps(data, indent=4, sort_keys=False, default=str)
                    log.debug("jsonString: \n" + jsonString )
                    outFile.write(jsonString)
            except Exception as error:
                log.error("There was a problem writing the structureInfo data to file: "  + str(error))
                log.error(traceback.format_exc())
                raise error

def updateStructureInfoWithUserOptions(thisTransaction : sequenceio.Transaction, structureInfo : sequenceio.StructureBuildInfo, filename: str):
    log.info("updateStructureInfotWithUserOptions() was called.")
    try:
        with open(filename, 'r') as inFile:
            data =json.load(inFile)

    except Exception as error:
        log.error("There was a problem updating the structureInfo file: " + str(error))
        log.error(traceback.format_exc())
        raise error

    else:
        log.debug("old data: \n\n")
        prettyPrint(data)
        for newState in structureInfo.buildStates:
            log.debug("New build state: " + str(newState))
            data['buildStates'].append(newState.__dict__)

        log.debug("updated data: \n\n")
        prettyPrint(data)
        try:
            with open(filename, 'w') as outFile:
                jsonString = json.dumps(data, indent=4, sort_keys=False, default=str)
                log.debug("jsonString: \n" + jsonString)
                outFile.write(jsonString)

        except Exception as error:
            log.error("There was a problem writing the updated data to the structureInfo file: " + str(error))
            log.error(traceback.format_exc())
            raise error


##  @brief Converts everything to string, creating and returning a new object for storage.
#   @detail Recursively handles the sequenceConformation too.
#   @param buildState Single3DStructureBuildDetails
#   @return state dict
def prepareBuildRecord(buildState : sequenceio.Single3DStructureBuildDetails):
    log.info("prepareBuildRecord() was called.")
    log.debug("buildState: " + repr(buildState))
    state = {}
    state['conformerLabel'] = buildState.conformerLabel
    state['simulationPhase'] = buildState.simulationPhase
    if buildState.simulationPhase == "solvent":
        state['solvationShape'] = buildState.solvationShape
    state['status'] = buildState.status
    state['date'] = str(buildState.date)
    state['addIons']  = buildState.addIons
    state['energy'] = buildState.energy
    state['forceField']  = buildState.forceField
    state['sequenceConformation'] = []
    try:
        if buildState.sequenceConformation is not None:
            log.debug("sequenceConformation: " + repr(buildState.sequenceConformation))
            for rotamerConf in buildState.sequenceConformation:
                log.debug("rotamerConf: " + repr(rotamerConf))
                state['sequenceConformation'].append(rotamerConf.__dict__)
        else:
            log.debug("No sequence conformation. Must be a request for the default structure.")
    except Exception as error:
        log.error("There was a problem converting the sequence conformation to dict: " + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        return state


def createSeqLog(sequence : str, seqIDPath : str):
    log.info("createSeqLog() was called.")
    logObj = StructureInfo()
    logObj.sequence = sequence
    try:
        logObj = convertStructureInfoToDict(logObj)
    except Exception as error:
        log.error("There was a problem converting the object to dict: " + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        ## dump to file
        try:
            fileName = seqIDPath + "/structureInfo.json"
            log.debug("Attempting to write: " + fileName)
            with open(fileName, 'w') as outFile:
                jsonString = json.dumps(logObj, indent=4, sort_keys=False, default=str)
                log.debug("jsonString: \n" + jsonString )
                outFile.write(jsonString)
        except Exception as error:
            log.error("There was a problem writing structureInfo_request.json to file: " + str(error))
            log.error(traceback.format_exc())
            raise error


##  @brief Pass in a transaction, get the structureInfo.json for that sequence.
#   @detail File for tracking the existance of various builds of a given sequence.
#   @return structureInfo filename String
def getStructureInfoFilename(thisTransaction : sequenceio.Transaction):
    log.info("getStructureInfoFilename() was called.")
    try:
        sequence = thisTransaction.getSequenceVariantOut('indexOrdered')
        thisProject = thisTransaction.getProjectOut()
    except Exception as error:
        log.error("There was a problem getting the sequence from the transaction: " + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        #seqID = projectUtils.getSeqIDForSequence(sequence)
        #seqIDPath = sequencePath + seqID
        sequencePath = thisProject.sequence_path
        ##Update the json file for future reference.
        return sequencePath + "/structureInfo.json"

## @brief pass in a transaction, ,get the structureInfo_status.json for that project.
#   @detail File for tracking the statuses of requested builds.
#   @return structureInfo_status filename String
def getStatusFilename(thisTransaction : sequenceio.Transaction):
    log.info("getStatusFileName() was called.")
    try:
        projectDir = thisTransaction.getProjectDirOut()
        log.debug("projectDir: " + projectDir)
    except Exception as error:
        log.error("There was a problem getting the projectDir: " + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        statusFilename = projectDir + "logs/structureInfo_status.json"

        return statusFilename

## @brief Generates a download URL for this build, assuming there is a website
#   @detail This build status info is saved in: Single3DStructureBuildDetails
#   @return Download URL for a conformer build
def generateDownloadUrl(thisTransaction : sequenceio.Transaction):
    log.info("generateDownloadUrl was called.")


def main():
    log.info("main() was called.")

if __name__ == "__main__":
    main()
