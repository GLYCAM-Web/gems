#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##    @class RotamerConformation
#    @brief    An object that represents a single requested pose for a single linkage
class RotamerConformation(BaseModel):
    ##Linkage Labels may be arbitrary, but they must be unique.
    linkageLabel : str = ""
    dihedralName : str = ""
    rotamer : str = ""

##   @class BuildState
#    @brief An object that represents one requested build state.
#    @TODO: Add more fields, ringPucker, protonationState, etc...
class BuildState(BaseModel):
    ## Labels may be either "structure" if there is only one for this project.
    #    or, they may be a terse label,
    #    or they may be uuids if the terse label is > 32 char long.
    structureLabel : str = ""
    simulationPhase : str = "gas-phase"
    ## Solvated requests might specify a shape.
    solvationShape : str = None

    ## new, building, ready, submitted, complete, failed, delayed
    status : str = "new" 
    date : datetime = None
    addIons : str = "default" ## Is there a benefit for this to be a String? Boolean?
    energy : str = None ## kcal/mol
    forceField : str = None ## TODO: This needs to be a class. Schedule design with Lachele.
    sequenceConformation : List[RotamerConformation] = None




##  @brief Object for tracking the parsing of rotamerData
#   @param rotamerData is list of nested dict objects from the frontend that 
#          represents user's rotamer selections.
#   @TODO: Move this to a better file for this stuff.
class RotamerCounter():
    linkages = []
    activeLevel = 0
    rootHits = 0

    def __init__(self, rotamerData):
        for linkage in rotamerData:
            label = linkage['linkageLabel']
            for dihedral in linkage['dihedrals']:
                name = dihedral['dihedralName']
                count = len(dihedral['selectedRotamers'])
                log.debug("count: " + str(count))
                thisLinkageCountingObj = {
                    'label' : label,
                    'dihedral' : name,
                    'count' : count,
                    'currentIndex' : count - 1
                }
                self.linkages.append(thisLinkageCountingObj)

        ## Instantiate to the index of the last element in the list.
        self.activeLevel = len(self.linkages) - 1


    def __str__(self):
        result = "\nactiveLevel: " + str(self.activeLevel)
        result = result + "\nlinkages: " 
        for linkage in self.linkages:
            result = result + "\n" + str(linkage)

        return result

##   @class StructureInfo
#    @brief An object to represent the data previously held in the Structure_Mapping_Table.
#    @detail This object holds the data that describes a series of ways that this single structure
#            has been built. Each variation of a rotamer or from gas-phase to solvated, etc...
#            represents a different build state, and each gets a record in this object.
#            This object can be used to track a request, and a copy of it could be used to track 
#            the progress of that requested series of jobs.
class StructureInfo(BaseModel):
    ## Useful to know what this all applies to.
    sequence : str = ""
    ## A build state is a descriptive object that can be used to request a pdb file 
    #    of a sequence in a specific pose, with various other settings as well.
    buildStates : List[BuildState] = None


##  @brief  Makes decisions about what rotamers the next sequence should use.
#   @detail Behaves like an odometer: iteration needs to allow for rotamer reuse after
#           a reset. Between resets, decrements are used.
#   @param  rotamerCounter
#   @TODO: Move this to a better file for this stuff.
def decrementCounters(rotamerCounter):
    log.info("decrementCounters() was called.")
    leafNode = rotamerCounter.linkages[len(rotamerCounter.linkages) - 1]

    if leafNode['currentIndex'] == 0:
        updateCount = 1
        thisIndex = len(rotamerCounter.linkages) - 1

        #All decrementing work to be done above the active level.
        while thisIndex > rotamerCounter.activeLevel:
            rotamerCounter.linkages[thisIndex]['currentIndex'] = rotamerCounter.linkages[thisIndex]['count'] - 1
            thisIndex = thisIndex - 1

        ## The active linkage.
        activeLinkage = rotamerCounter.linkages[rotamerCounter.activeLevel]
        ## reset active linkage and increment its parent once.
        activeLinkage['currentIndex'] = activeLinkage['count'] - 1

        ## decrement the parent, when appropriate.
        parentIndex = rotamerCounter.activeLevel - 1
        parentLinkage = rotamerCounter.linkages[parentIndex]
        if parentIndex > 0:
            parentLinkage['currentIndex'] = parentLinkage['currentIndex'] - 1
            rotamerCounter.activeLevel = parentIndex
        elif parentIndex == 0:
            if parentLinkage['currentIndex'] > 0:
                parentLinkage['currentIndex'] = parentLinkage['currentIndex'] - 1
                rotamerCounter.rootHits = rotamerCounter.rootHits + 1
                rotamerCounter.activeLevel = len(rotamerCounter.linkages) - 1
                resetCount = 1
                while resetCount < len(rotamerCounter.linkages):
                    rotamerCounter.linkages[resetCount]['currentIndex'] = rotamerCounter.linkages[resetCount]['count'] - 1
                    resetCount = resetCount + 1
            else:
                log.debug("I think we are done with updating parent linkages?")

        updateCount = updateCount + 1
    else:
        leafNode['currentIndex'] = leafNode['currentIndex'] - 1


##  @brief  Updates the sequence with the next config object for a linkage based on the counterObj
#   @detail Within a sequence, a conformer represents the state (rotamer) of a single label-dihedral pair.
#           Just gets whatever rotamer is indicated in counterObj['currentIndex'], which puts all
#           selection responsibility in the counter and decrementCounters(). Does not increment indices.
#   @param  rotamerData
#   @param  counterObj
#   @param  sequence  Not the string, but a list of conformers currently being built.
#   @TODO: Move this to a better file for this stuff.
def addNextConformer(rotamerData, counterObj, sequence):
    log.debug("addNextConformer() was called.")
    myLabel = counterObj['label']
    myDihedral = counterObj['dihedral']
    myCount = counterObj['count']
    myCurrentIndex = counterObj['currentIndex']

    for linkageData in rotamerData:
        linkageLabel = linkageData['linkageLabel'].strip()
        log.debug("Looking for linkageLabel: " + linkageLabel)
        if linkageLabel == myLabel:
            log.debug("Found the linkage. Looking for the dihedral.")

            for dihedral in linkageData['dihedrals']:
                dihedralName = dihedral['dihedralName']
                log.debug("Looking for dihedralName: " + dihedralName)  
                if dihedralName == myDihedral:
                    log.debug("Found the dihedral for this linkage.")
                    log.debug("myCurrentIndex: " + str(myCurrentIndex))
                    rotamer = dihedral['selectedRotamers'][myCurrentIndex]
                    log.debug("rotamer: " + rotamer)
                
                    conformer = {
                        'linkageLabel' : linkageLabel,
                        'dihedralName' : dihedralName,
                        'rotamer' : rotamer
                    }
                    sequence.append(conformer)


##  @brief Grab the next sequence indicated by the rotamerCounter object. 
#   @detail Handles things at the sequence level, grabbing conformer config dicts 
#       and updating the rotamerCounter object so the next one will be the correct one.
#   @TODO: Move this to a better file for this stuff.
def getNextSequence(rotamerData, rotamerCounter, sequences):
    log.debug("getNextSequence() was called.")
    sequence = []

    log.debug("\n\nrotamerCounter before building a sequence: \n" + str(rotamerCounter) + "\n")

    ##Iterate through the rotamerCounter grabbing the keys for
    #   grabbing the right rotamers from rotamer date
    for i in range(len(rotamerCounter.linkages)) :
        counterObj = rotamerCounter.linkages[i]
        log.debug("Looking up this linkage at i: " + str(i) + ": " +  str(counterObj))

        if len(sequences) == 0: 
            log.debug("first sequence. Getting the first thing found for each label-dihedral pair.")
            ##First sequence. Grab the first element found in each element.
            addNextConformer(rotamerData, counterObj, sequence)
            if i == len(rotamerCounter.linkages) - 1:
                log.debug("decrementing counters for the first time.")
                log.debug("\n\nrotamerCounter before: \n" + str(rotamerCounter))
                decrementCounters(rotamerCounter)
                log.debug("\n\nrotamerCounter after: \n" + str(rotamerCounter))
        else:
            log.debug("Sequences exist, need to check against those.")
            ## The lastLeafConformer  is the conformer of the leaf of the previous sequence.
            addNextConformer(rotamerData, counterObj, sequence)
            if i == len(rotamerCounter.linkages) - 1:
                log.debug("\n\nrotamerCounter before: \n" + str(rotamerCounter))
                decrementCounters(rotamerCounter)
                log.debug("\n\nrotamerCounter after: \n" + str(rotamerCounter))
        
    log.debug("\n\nreturning this sequence: \n " + str(sequence) + "\n")
    return sequence


##  @brief Uses the rotamerCounter to multiply the number of rotamer selections for each
#       linkage-dihedral pair
#   @param rotamerCounter
#   @TODO: Move this to a better file for this stuff.
def getRequestedStructureCount(rotamerCounter):
    log.info("getRequestedStructureCount() was called.")
    requestedStructureCount = 1
    for linkage in rotamerCounter.linkages:
        x = int(linkage['count'])
        requestedStructureCount = requestedStructureCount * x

    return requestedStructureCount

##  @brief  Finds rotamerData in the transaction
#   @param  Transaction
#   @return rotamerData
#   @TODO: Move this to a better file for this stuff.
def getRotamerDataFromTransaction(thisTransaction: Transaction):
    log.info("getRotamerDataFromTransaction() was called.")
    request = thisTransaction.request_dict
    if "options" in request.keys():
        if "geometryOptions" in request['options'].keys():
            if 'rotamerData' in request['options']['geometryOptions'].keys():
                rotamerData = request['options']['geometryOptions']['rotamerData']
                log.debug("rotamerData: " + str(rotamerData))
                return rotamerData
            else:
                raise AttributeError("rotamerData")
        else:
            raise AttributeError("geometryOptions")
    else:
        log.debug("No options present in the request. Likely just a request for the default.")

##  @brief Pass in a sequence (list of rotamerConformations), get a terse label.
#   @detail Translate the more verbose sequenceConf object into a terse string that is useful
#           for naming directories and describing interesting geometry in a build.
#   @param sequenceConf List[rotamerConformation]
#   @return string structureLabel
def buildStructureLabel(sequenceConf):
    log.info("buildStructureLabel() was called.\n\n")
    structureLabel = ""
    log.debug("this sequenceConf: \n" + str(sequenceConf))

    #Assess each rotamer conf obj
    for rotamerConf in sequenceConf:
        log.debug("this rotamerConf: \n" + str(rotamerConf))

        ##Decide whether or not to add the label.
        if structureLabel == "":
            structureLabel = rotamerConf['linkageLabel']
        elif rotamerConf['linkageLabel'] not in structureLabel:
            structureLabel = structureLabel + "_"+ rotamerConf['linkageLabel']
        else:
            log.debug("adding to the same linkage.")
            structureLabel = structureLabel + "_"

        ##Decide which abbreviated dihedral is needed
        dihedralAbbreviation = ""
        if rotamerConf['dihedralName'] == "phi":
            dihedralAbbreviation = "h"
        elif rotamerConf['dihedralName'] == "psi":
            dihedralAbbreviation = "s"
        elif rotamerConf['dihedralName'] == "omega":
            dihedralAbbreviation = "o"
        elif rotamerConf['dihedralName'] == "chi":
            dihedralAbbreviation = "c"
        else:
            log.debug("Unrecognized dihedralName: " + str(rotamerConf['dihedralName'])) 

        structureLabel = structureLabel + dihedralAbbreviation

        ##Add the rotamer value
        structureLabel = structureLabel + rotamerConf['rotamer']


    return structureLabel


##  @brief  Gets the shape from the user request in transactions or returns default.
#   @param Transaction
#   @return String solvent_shape
def getSolvationShape(thisTransaction):
    log.info("getSolvationShape() was called.")
    project = getFrontendProjectFromTransaction(thisTransaction)
    if project is not None:
        return project['solvation_shape']
    else:
        ##TODO: write logic for commandline users to specify solvent shapes other than the default.
        return "REC"

##  @brief Look at the transaction to see if a force field is specified
#   @param Transaction thisTransaction
#   @return String either "default" or the force field name.
def getForceFieldFromRequest(thisTransaction):
    log.info("getForceFieldFromRequest() was called.")
    feProject = getFrontendProjectFromTransaction(thisTransaction)
    if feProject is not None:
        log.debug("feProject keys: " + str(feProject.keys()))
        if feProject['force_field'] == "":
            return "default"
        else:
            return project['force_field']

    else:
        ##TODO: write logic for commandline users to specify forcefields other than the default
        ##Should it live in options?
        return "default"

##  @brief Parses user's selected rotamers (rotamerData) into a list of 
#           structures to request.
#   @detail With a limit of 64 structures to request at a time, users select
#           each rotamer they want for each linkage. This code creates the 
#           list of unique permutations possible for those selections.
#   @param Transaction 
#   @TODO: Move this to a better file for this stuff.
def buildStructureInfo(thisTransaction : Transaction):
    log.info("buildStructureInfo() was called.")

    structureInfo = StructureInfo()
    structureInfo.buildStates = []
    try:
        sequence = getSequenceFromTransaction(thisTransaction)
        log.debug("sequence: " + str(sequence))
        structureInfo.sequence = sequence
        ##TODO: Also grab the following from the request, or set defaults:
        ##    buildType, ions, forceField, date.
    except Exception as error:
        log.error("There was a problem getting the sequence from the transaction: " + str(error))
        raise error
    else:
        try:
            #RotamerData is the list of dict objects describing each linkage
            rotamerData = getRotamerDataFromTransaction(thisTransaction)
        except Exception as error:
            log.error("There was a problem getting rotamerData from the transaction: " + str(error))
            raise error
        else:
            sequences = []

            ## Need to be able to handle the default, which has no rotamerData.
            if rotamerData == None:
                log.debug("Default request!")
                buildState = BuildState()
                buildState.structureLabel = "default"
                buildState.date = datetime.now()
                structureInfo.buildStates.append(buildState)

            ## Presence of rotamerData indicates specific rotamer requests.
            else:    
                linkageCount = len(rotamerData)
                log.debug("linkageCount: " + str(linkageCount))
                log.debug("\nrotamerData:\n" + str(rotamerData))

                ##Rotamer counter objects allow the logic to track the rotamer selection.
                rotamerCounter = RotamerCounter(rotamerData)
                log.debug("rotamerCounter: " + str(rotamerCounter.__dict__))

                ##How many structures have been requested?
                requestedStructureCount = getRequestedStructureCount(rotamerCounter)
                log.debug("requestedStructureCount: " + str(requestedStructureCount))
                
                ##Define when to stop.
                while len(sequences) < requestedStructureCount and len(sequences) <= 64:
                    buildState = BuildState()
                    ##Build the sequenceConformation
                    sequenceConf = getNextSequence(rotamerData, rotamerCounter, sequences)
                    buildState.sequenceConformation = sequenceConf
                    
                    ##Build the structureLabel
                    buildState.structureLabel = buildStructureLabel(sequenceConf)
                    log.debug("structureLabel: \n" + buildState.structureLabel)

                    ##Check if the user requested a specific simulationPhase
                    buildState.simulationPhase = checkForSimulationPhase(thisTransaction)
                    log.debug("simulationPhase: " + buildState.simulationPhase)
                    if buildState.simulationPhase == "solvent":
                        buildState.solvationShape = getSolvationShape(thisTransaction)

                    ##Set the date
                    buildState.date = datetime.now()
                    log.debug("date: " + str(buildState.date))

                    ## Check if the user requested to add ions
                    buildState.addIons = checkForAddIons(thisTransaction)

                    ##sequences is needed for progress tracking.
                    sequences.append(sequenceConf)     
                    log.debug("sequence list length: " + str(len(sequences)))
                    structureInfo.buildStates.append(buildState)
                    
                ##Useful logging for maintenance
                log.debug("sequences: ")
                for element in sequences:
                    log.debug("~")
                    for item in element:
                        log.debug( str(item) )

                log.debug("sequenceCount: " + str(len(sequences)))

    return structureInfo


##  @brief creates the files needed to track a request for various builds of a sequence.
#   @detail not for updating existing files. 
def saveRequestInfo(structureInfo, projectDir):
    log.info("saveRequestInfo() was called.")
    
    ## convert the object to dict
    try:
        data = convertStructureInfoToDict(structureInfo)
        log.debug("structureInfo as dict: \n\n")
        prettyPrint(data)
    except Exception as error:
        log.error("There was a problem converting the structureInfo to dict: " + str(error))
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
                raise error


##  @brief Pass in structureInfo, get a dict in return.
#   @detail Since structureInfo objects have lists of objects with lists of objects, 
#   a bit of homework is saved by using this to convert to dict.
def convertStructureInfoToDict(structureInfo):
    log.info("convertStructureInfoToDict was called.")
    data = {}
    ## set the sequence.
    try:
        data['sequence'] = structureInfo.sequence
        data['buildStates'] = []
    except Exception as error:
        log.error("There was a problem finding the sequence in structureInfo: " + str(error))
        raise error
    else:
        try:
            if structureInfo.buildStates is not None:
                ##Process the build states.
                for buildState in structureInfo.buildStates:
                    log.debug("buildState: " + repr(buildState))
                    state = {}
                    state['structureLabel'] = buildState.structureLabel
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
                        raise error
                    else:
                        data['buildStates'].append(state)
            else: 
                log.debug("There may be no build states in a default structure request.")
        except Exception as error:
            log.error("There was a problem building the states for this structureInfo: " + str(error))
            raise error
        else:
            return data




##  @brief Checks a transaction for user requests that specify adding ions.
#   @detail Default value is "default" - which depends on other software's defauts.
#   @param Transaction
def checkForAddIons(thisTransaction: Transaction):
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
def checkForSimulationPhase(thisTransaction: Transaction):
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
def updateBuildStatus(structureInfoFilename : str, buildState : BuildState, status : str):
    log.info("updateStructureInfo() was called.")
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
                log.error("\n\n\n\n\nStill in dev \n\n\n\n")
                ##TODO: Find the appropriate record for updating.
                for recordedState in data['buildStates']:
                    log.debug("recordedState['structureLabel']: " + recordedState['structureLabel'])
                    log.debug("buildState.structureLabel: " + buildState.structureLabel)
                    if recordedState['structureLabel'] == buildState.structureLabel:
                        log.debug("Found the record to update. recordedState['status']: " + recordedState['status'])
                        recordedState['status'] = status
                        log.debug("updated recordedState['status']: " + recordedState['status'])

        except Exception as error:
            log.error("There was a problem updating the object: " + str(error))
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
                raise error


##  @brief Converts everything to string, creating and returning a new object for storage.
#   @detail Recursively handles the sequenceConformation too.
#   @param buildState BuildState
#   @return state dict
def prepareBuildRecord(buildState : BuildState):
    log.info("prepareBuildRecord() was called.")
    log.debug("buildState: " + repr(buildState))
    state = {}
    state['structureLabel'] = buildState.structureLabel
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
            raise error


##  @brief Pass in a transaction, get the structureInfo.json for that sequence.
#   @detail File for tracking the existance of various builds of a given sequence.
#   @return structureInfo filename String
def getStructureInfoFilename(thisTransaction : Transaction):
    log.info("getStructureInfoFilename() was called.")
    try:
        sequence = getSequenceFromTransaction(thisTransaction)
    except Exception as error:
        log.error("There was a problem getting the sequence from the transaction: " + str(error))
        raise error
    else:
        seqID = getSeqIDForSequence(sequence)
        userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"
        seqIDPath = userDataDir + seqID
        ##Update the json file for future reference.
        return seqIDPath + "/structureInfo.json"

## @brief pass in a transaction, ,get the structureInfo_status.json for that project.
#   @detail File for tracking the statuses of requested builds.
#   @return structureInfo_status filename String
def getStatusFilename(thisTransaction : Transaction):
    log.info("getStatusFileName() was called.")
    try:
        projectDir = getProjectDir(thisTransaction)
        log.debug("projectDir: " + projectDir)
    except Exception as error:
        log.error("There was a problem getting the projectDir: " + str(error))
        raise error
    else:
        statusFilename = projectDir + "logs/structureInfo_status.json"

        return statusFilename


def main():
    log.info("main() was called.")

if __name__ == "__main__":
    main()