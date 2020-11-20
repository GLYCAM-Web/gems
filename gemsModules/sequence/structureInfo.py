#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.schema import schema
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.delegator import io as delegatorio
from gemsModules.common.loggingConfig import *
from gemsModules.project.projectUtil import *
import gmml
import itertools
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##    @class RotamerConformation
#    @brief    An object that represents a single requested pose for a single linkage
# class RotamerConformation(BaseModel):
#     ##Linkage Labels may be arbitrary, but they must be unique.
#     ## TODO : linkageLabel is now passing down linkageIndex to gmml. 
#     ## The problem is addNextConformer() is using linkageLabel along with RotamerCounter somehow. 
#     ## We need:
#     #linkageIndex : str = "" # Once implemented, linkageLabel can be whatever.
#     linkageLabel : str = "" # Now contains what is linkageIndex at GMML level.
#     dihedralName : str = ""
#     rotamer : str = ""

##   @class BuildState
#    @brief An object that represents one requested build state.
#    @TODO: Add more fields, ringPucker, protonationState, etc...
class BuildState(BaseModel):
    ## Labels may be either "structure" if there is only one for this project.
    #    or, they may be a terse label,
    #    or they may be uuids if the terse label is > 32 char long.
    structureLabel : str = ""
    structureDirectoryName : str = ""
    simulationPhase : str = "gas-phase"
    ## Solvated requests might specify a shape.
    solvationShape : str = None

    isDefaultStructure : bool = False
    ## new, building, ready, submitted, complete, failed, delayed
    status : str = "new" 
    date : datetime = None
    addIons : str = "default" ## Is there a benefit for this to be a String? Boolean?
    energy : str = None ## kcal/mol
    forceField : str = None ## TODO: This needs to be a class. Schedule design with Lachele.
    #sequenceConformation : List[RotamerConformation] = None 
    sequenceConformation : List = None
    ## Would be nice to just directly use the gmml level class like this:
    #gmmlConformerInfo : gmml.single_rotamer_info_vector = None   
       
##  @brief Object for tracking the parsing of rotamerData
#   @param rotamerData is list of nested dict objects from the frontend that 
#          represents user's rotamer selections.
#   @TODO: Move this to a better file for this stuff.
# class RotamerCounter():
#     linkages = []
#     activeLevel = 0
#     rootHits = 0

#     def __init__(self, rotamerData):
#         for linkage in rotamerData:
#             label = linkage['linkageLabel']
#             for dihedral in linkage['dihedrals']:
#                 name = dihedral['dihedralName']
#                 count = len(dihedral['selectedRotamers'])
#                 log.debug("count: " + str(count))
#                 thisLinkageCountingObj = {
#                     'label' : label,
#                     'dihedral' : name,
#                     'count' : count,
#                     'currentIndex' : count - 1
#                 }
#                 self.linkages.append(thisLinkageCountingObj)

#         ## Instantiate to the index of the last element in the list.
#         self.activeLevel = len(self.linkages) - 1


#     def __str__(self):
#         result = "\nactiveLevel: " + str(self.activeLevel)
#         result = result + "\nlinkages: " 
#         for linkage in self.linkages:
#             result = result + "\n" + str(linkage)

#         return result

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
# def decrementCounters(rotamerCounter):
#     log.info("decrementCounters() was called.")
#     leafNode = rotamerCounter.linkages[len(rotamerCounter.linkages) - 1]

#     if leafNode['currentIndex'] == 0:
#         updateCount = 1
#         thisIndex = len(rotamerCounter.linkages) - 1

#         #All decrementing work to be done above the active level.
#         while thisIndex > rotamerCounter.activeLevel:
#             rotamerCounter.linkages[thisIndex]['currentIndex'] = rotamerCounter.linkages[thisIndex]['count'] - 1
#             thisIndex = thisIndex - 1

#         ## The active linkage.
#         activeLinkage = rotamerCounter.linkages[rotamerCounter.activeLevel]
#         ## reset active linkage and increment its parent once.
#         activeLinkage['currentIndex'] = activeLinkage['count'] - 1

#         ## decrement the parent, when appropriate.
#         parentIndex = rotamerCounter.activeLevel - 1
#         parentLinkage = rotamerCounter.linkages[parentIndex]
#         if parentIndex > 0:
#             parentLinkage['currentIndex'] = parentLinkage['currentIndex'] - 1
#             log.debug("Are we the baddies?: " + str(parentLinkage['currentIndex']))
#             rotamerCounter.activeLevel = parentIndex
#         elif parentIndex == 0:
#             if parentLinkage['currentIndex'] > 0:
#                 parentLinkage['currentIndex'] = parentLinkage['currentIndex'] - 1
#                 rotamerCounter.rootHits = rotamerCounter.rootHits + 1
#                 rotamerCounter.activeLevel = len(rotamerCounter.linkages) - 1
#                 resetCount = 1
#                 while resetCount < len(rotamerCounter.linkages):
#                     rotamerCounter.linkages[resetCount]['currentIndex'] = rotamerCounter.linkages[resetCount]['count'] - 1
#                     resetCount = resetCount + 1
#             else:
#                 log.debug("I think we are done with updating parent linkages?")

#         updateCount = updateCount + 1
#     else:
#         leafNode['currentIndex'] = leafNode['currentIndex'] - 1


##  @brief  Updates the sequence with the next config object for a linkage based on the counterObj
#   @detail Within a sequence, a conformer represents the state (rotamer) of a single label-dihedral pair.
#           Just gets whatever rotamer is indicated in counterObj['currentIndex'], which puts all
#           selection responsibility in the counter and decrementCounters(). Does not increment indices.
#   @param  rotamerData
#   @param  counterObj
#   @param  sequence  Not the string, but a list of conformers currently being built.
#   @TODO: Move this to a better file for this stuff.
# def addNextConformer(rotamerData, counterObj, sequence):
#     log.debug("addNextConformer() was called.")
#     myLabel = counterObj['label']
#     myDihedral = counterObj['dihedral']
#     myCount = counterObj['count']
#     myCurrentIndex = counterObj['currentIndex']

#     for linkageData in rotamerData:
#         linkageLabel = linkageData['linkageLabel'].strip()
#         log.debug("Looking for linkageLabel: " + linkageLabel)
#         if linkageLabel == myLabel:
#             log.debug("Found the linkage. Looking for the dihedral.")

#             for dihedral in linkageData['dihedrals']:
#                 dihedralName = dihedral['dihedralName']
#                 log.debug("Looking for dihedralName: " + dihedralName)  
#                 if dihedralName == myDihedral:
#                     log.debug("Found the dihedral for this linkage.")
#                     log.debug("myCurrentIndex: " + str(myCurrentIndex))
#                     rotamer = dihedral['selectedRotamers'][myCurrentIndex]
#                     log.debug("rotamer: " + rotamer)
                
#                     conformer = {
#                         'linkageLabel' : linkageLabel,
#                         'dihedralName' : dihedralName,
#                         'rotamer' : rotamer
#                     }
#                     sequence.append(conformer)


##  @brief Grab the next sequence indicated by the rotamerCounter object. 
#   @detail Handles things at the sequence level, grabbing conformer config dicts 
#       and updating the rotamerCounter object so the next one will be the correct one.
#   @TODO: Move this to a better file for this stuff.
# def getNextSequence(rotamerData, rotamerCounter, sequences):
#     log.debug("getNextSequence() was called.")
#     sequence = []

#     log.debug("\n\nrotamerCounter before building a sequence: \n" + str(rotamerCounter) + "\n")

#     ##Iterate through the rotamerCounter grabbing the keys for
#     #   grabbing the right rotamers from rotamer date
#     for i in range(len(rotamerCounter.linkages)) :
#         counterObj = rotamerCounter.linkages[i]
#         log.debug("Looking up this linkage at i: " + str(i) + ": " +  str(counterObj))

#         if len(sequences) == 0: 
#             log.debug("first sequence. Getting the first thing found for each label-dihedral pair.")
#             ##First sequence. Grab the first element found in each element.
#             addNextConformer(rotamerData, counterObj, sequence)
#             if i == len(rotamerCounter.linkages) - 1:
#                 log.debug("decrementing counters for the first time.")
#                 log.debug("\n\nrotamerCounter before: \n" + str(rotamerCounter))
#                 decrementCounters(rotamerCounter)
#                 log.debug("\n\nrotamerCounter after: \n" + str(rotamerCounter))
#         else:
#             log.debug("Sequences exist, need to check against those.")
#             ## The lastLeafConformer  is the conformer of the leaf of the previous sequence.
#             addNextConformer(rotamerData, counterObj, sequence)
#             if i == len(rotamerCounter.linkages) - 1:
#                 log.debug("\n\nrotamerCounter before: \n" + str(rotamerCounter))
#                 decrementCounters(rotamerCounter)
#                 log.debug("\n\nrotamerCounter after: \n" + str(rotamerCounter))
        
#     log.debug("\n\nreturning this sequence: \n " + str(sequence) + "\n")
#     return sequence


##  @brief Uses the rotamerCounter to multiply the number of rotamer selections for each
#       linkage-dihedral pair
#   @param rotamerCounter
#   @TODO: Move this to a better file for this stuff.
# def getRequestedStructureCount(rotamerCounter):
#     log.info("getRequestedStructureCount() was called.")
#     requestedStructureCount = 1
#     for linkage in rotamerCounter.linkages:
#         x = int(linkage['count'])
#         requestedStructureCount = requestedStructureCount * x

#     return requestedStructureCount

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
# def buildStructureLabel(sequenceConf):
#     log.info("buildStructureLabel() was called.\n\n")
#     structureLabel = ""
#     log.debug("this sequenceConf: \n" + str(sequenceConf))

#     #Assess each rotamer conf obj
#     for rotamerConf in sequenceConf:
#         log.debug("this rotamerConf: \n" + str(rotamerConf))

#         ##Decide whether or not to add the label.
#         if structureLabel == "":
#             structureLabel = rotamerConf['linkageLabel']
#         elif rotamerConf['linkageLabel'] not in structureLabel:
#             structureLabel = structureLabel + "_"+ rotamerConf['linkageLabel']
#         else:
#             log.debug("adding to the same linkage.")
#             structureLabel = structureLabel + "_"

#         ##Decide which abbreviated dihedral is needed
#         dihedralAbbreviation = ""
#         if rotamerConf['dihedralName'] == "phi":
#             dihedralAbbreviation = "h"
#         elif rotamerConf['dihedralName'] == "psi":
#             dihedralAbbreviation = "s"
#         elif rotamerConf['dihedralName'] == "omg":
#             dihedralAbbreviation = "o"
#         elif rotamerConf['dihedralName'] == "omega":
#             dihedralAbbreviation = "o"
#         elif rotamerConf['dihedralName'] == "chi1":
#             dihedralAbbreviation = "c1"
#         elif rotamerConf['dihedralName'] == "chi2":
#             dihedralAbbreviation = "c2"
#         else:
#             log.debug("Unrecognized dihedralName: " + str(rotamerConf['dihedralName'])) 

#         structureLabel = structureLabel + dihedralAbbreviation

#         ##Add the rotamer value
#         structureLabel = structureLabel + rotamerConf['rotamer']


#     return structureLabel

##  @brief Pass in a sequence (list of rotamerConformations), get a terse label.
#   @detail Translate the more verbose sequenceConf object into a terse string that is useful
#           for naming directories and describing interesting geometry in a build.
#   @param sequenceConf List[rotamerConformation]
#   @return string structureLabel
def buildStructureLabelOliver(rotamerCombo):
    log.info("buildStructureLabel() was called.\n\n")
    structureLabel = ""
    currentLinkage = ""
    #log.debug("this sequenceConf: \n" + str(sequenceConf))

    for item in rotamerCombo:
        ## Decide whether or not to add the label.
        if structureLabel == "": # first loop
            currentLinkage = item
            structureLabel += item
        elif item.isdigit(): ## Assumes only linkages are ints, and not negative.
            structureLabel += "_"
            if item != currentLinkage: # new linkage
                structureLabel += item 
                currentLinkage = item
        else:
            structureLabel += item
    return structureLabel


class RotamerConformation(BaseModel):
    #linkageIndex : str = "" # Once implemented, linkageLabel can be whatever.
    linkageLabel : str = "" # Now contains what is linkageIndex at GMML level.
    dihedralName : str = ""
    rotamer : str = ""

def convertDihedralNameToCode(dihedralName : str):
    dihedralName = dihedralName.replace("omega", "omg")
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
    project = getProjectFromTransaction(thisTransaction)
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
    project = getProjectFromTransaction(thisTransaction)
    if project is not None:
        log.debug("project keys: " + str(project.keys()))
        if project['force_field'] == "":
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
# def buildStructureInfo(thisTransaction : Transaction):
#     log.info("buildStructureInfo() was called.")

#     structureInfo = StructureInfo()
#     structureInfo.buildStates = []
#     try:
#         sequence = getSequenceFromTransaction(thisTransaction)
#         log.debug("sequence: " + str(sequence))
#         structureInfo.sequence = sequence
#         ##TODO: Also grab the following from the request, or set defaults:
#         ##    buildType, ions, forceField, date.
#     except Exception as error:
#         log.error("There was a problem getting the sequence from the transaction: " + str(error))
#         raise error
#     try:
#         #RotamerData is the list of dict objects describing each linkage
#         rotamerData = getRotamerDataFromTransaction(thisTransaction)
#     except Exception as error:
#         log.error("There was a problem getting rotamerData from the transaction: " + str(error))
#         raise error
#     sequences = []
#     ## Need to be able to handle the default, which has no rotamerData.
#     if rotamerData == None:
#         log.debug("Default request!")
#         buildState = BuildState()
#         buildState.structureLabel = "structure"
#         buildState.date = datetime.now()
#         structureInfo.buildStates.append(buildState)

#     ## Presence of rotamerData indicates specific rotamer requests.
#     else:    
#         linkageCount = len(rotamerData)
#         log.debug("linkageCount: " + str(linkageCount))
#         log.debug("\nrotamerData:\n" + str(rotamerData))

#         ##Rotamer counter objects allow the logic to track the rotamer selection.
#         rotamerCounter = RotamerCounter(rotamerData)
#         log.debug("rotamerCounter: " + str(rotamerCounter.__dict__))

#         ##How many structures have been requested?
#         requestedStructureCount = getRequestedStructureCount(rotamerCounter)
#         log.debug("requestedStructureCount: " + str(requestedStructureCount))
                
#         ##Define when to stop.
#         while len(sequences) < requestedStructureCount and len(sequences) <= 64:
#             buildState = BuildState()
#             ##Build the sequenceConformation
#             sequenceConf = getNextSequence(rotamerData, rotamerCounter, sequences)
#             buildState.sequenceConformation = sequenceConf
                    
#             ##Build the structureLabel
#             buildState.structureLabel = buildStructureLabel(sequenceConf)
#             log.debug("structureLabel: \n" + buildState.structureLabel)
#             if len(buildState.structureLabel) > 32 :
#                 log.debug("structureLabel is long so building a UUID for structureDirectoryName")
#                 buildState.structureDirectoryName = getUuidForString(buildState.structureLabel)
#                 log.debug("The structureDirectoryName/UUID is : " + buildState.structureDirectoryName)
#             else:
#                 log.debug("structureLabel is short so using it for structureDirectoryName")
#                 buildState.structureDirectoryName = buildState.structureLabel 
#                 log.debug("The structureDirectoryName is : " + buildState.structureDirectoryName)

#             ##Check if the user requested a specific simulationPhase
#             buildState.simulationPhase = checkForSimulationPhase(thisTransaction)
#             log.debug("simulationPhase: " + buildState.simulationPhase)
#             if buildState.simulationPhase == "solvent":
#                         buildState.solvationShape = getSolvationShape(thisTransaction)

#             ##Set the date
#             buildState.date = datetime.now()
#             log.debug("date: " + str(buildState.date))

#             ## Check if the user requested to add ions
#             buildState.addIons = checkForAddIons(thisTransaction)

#             ##sequences is needed for progress tracking.
#             sequences.append(sequenceConf)     
#             log.debug("sequence list length: " + str(len(sequences)))
#             structureInfo.buildStates.append(buildState)
                    
#         ##Useful logging for maintenance
#         log.debug("sequences: ")
#         for element in sequences:
#             log.debug("~")
#             for item in element:
#                 log.debug( str(item) )

#         log.debug("sequenceCount: " + str(len(sequences)))

#     return structureInfo

def countNumberOfShapesUpToLimit(rotamerData : []):
    hardLimit = 64
    count = 1
    for linkage in rotamerData:
        for dihedral in linkage['dihedrals']:
            count *= len(dihedral['selectedRotamers'])
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
def buildStructureInfoOliver(thisTransaction : Transaction):
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
        log.error(traceback.format_exc())
        raise error
    try:
        #RotamerData is the list of dict objects describing each linkage
        rotamerData = getRotamerDataFromTransaction(thisTransaction)
    except Exception as error:
        log.error("There was a problem getting rotamerData from the transaction: " + str(error))
        log.error(traceback.format_exc())
        raise error
        
    sequences = []
    ## Need to be able to handle the default, which has no rotamerData.
    ## Oliver has decided to always request a default for symlinking ease.
    buildState = BuildState()
    buildState.structureLabel = "default"
    buildState.structureDirectoryName = "default"
    buildState.isDefaultStructure = True
    buildState.date = datetime.now()
    structureInfo.buildStates.append(buildState)

    ## Presence of rotamerData indicates specific rotamer requests.
    if rotamerData != None:
        #Just get all this info once and append to each buildstate in the loop below
        simulationPhase = checkForSimulationPhase(thisTransaction)
        log.debug("simulationPhase: " + simulationPhase)
        solvationShape = None
        if simulationPhase == "solvent":
            solvationShape = getSolvationShape(thisTransaction)
        date = datetime.now()
        log.debug("date: " + str(date))
        addIons = checkForAddIons(thisTransaction)
        log.debug("\nrotamerData:\n" + str(rotamerData))
        # Now convert the rotamerData object into a List for itertools to work on.
        sequenceRotamerCombos = generateCombinationsFromRotamerData(rotamerData)
        # Now put add these combos to individual buildstates with other info
        for rotamerCombo in sequenceRotamerCombos:
            buildState = BuildState()
            buildState.sequenceConformation = rotamerCombo
            buildState.structureLabel = buildStructureLabelOliver(rotamerCombo)
            log.debug("label is :" + buildState.structureLabel)
            if len(buildState.structureLabel) > 32 :
                log.debug("structureLabel is long so building a UUID for structureDirectoryName")
                buildState.structureDirectoryName = getUuidForString(buildState.structureLabel)
                log.debug("The structureDirectoryName/UUID is : " + buildState.structureDirectoryName)
            else:
                log.debug("structureLabel is short so using it for structureDirectoryName")
                buildState.structureDirectoryName = buildState.structureLabel 
                log.debug("The structureDirectoryName is : " + buildState.structureDirectoryName)
            buildState.simulationPhase = simulationPhase
            if solvationShape != None:
                buildState.solventShape = solventShape
            buildState.date = date
            buildState.addIons = addIons
            structureInfo.buildStates.append(buildState)    
    return structureInfo

def generateCombinationsFromRotamerData(rotamerData):
    # First convert into a nested list for itertools to work with
    rotamerDataList = []
    for linkage in rotamerData:
        linkageIndex = ([linkage['linkageLabel']]) #converts to string
        dihedrals = []
        for dihedral in linkage['dihedrals']:
            dihedralCodeName = convertDihedralNameToCode(dihedral['dihedralName'])
            rotamers = []
            for rotamer in dihedral['selectedRotamers']:
                rotamers.extend([rotamer])
            rotamerDataList.extend([linkageIndex, [dihedralCodeName], rotamers])
    maxStructures = countNumberOfShapesUpToLimit(rotamerData)
    # The inner .product function is what creates the combinations. The islice limits the number.
    return list(itertools.islice(itertools.product(*rotamerDataList), maxStructures))

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
def convertStructureInfoToDict(structureInfo):
    log.info("convertStructureInfoToDict was called.")
    data = {}
    ## set the sequence.
    try:
        data['sequence'] = structureInfo.sequence
        data['buildStates'] = []
    except Exception as error:
        log.error("There was a problem finding the sequence in structureInfo: " + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        try:
            if structureInfo.buildStates is not None:
                ##Process the build states.
                for buildState in structureInfo.buildStates:
                    log.debug("buildState: \n" + repr(buildState))
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
                            log.debug("sequenceConformation: \n" + repr(buildState.sequenceConformation))
                            for rotamerConf in buildState.sequenceConformation:
                                log.debug("rotamerConf: \n" + repr(rotamerConf))
                                state['sequenceConformation'].append(rotamerConf)
                        else:
                            log.debug("No sequence conformation. Must be a request for the default structure.")
                    except Exception as error:
                        log.error("There was a problem converting the sequence conformation to dict: " + str(error))
                        log.error(traceback.format_exc())
                        raise error
                    else:
                        data['buildStates'].append(state)
            else: 
                log.debug("There may be no build states in a default structure request.")
        except Exception as error:
            log.error("There was a problem building the states for this structureInfo: " + str(error))
            log.error(traceback.format_exc())
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
                    log.debug("recordedState['structureLabel']: " + recordedState['structureLabel'])
                    log.debug("buildState.structureLabel: " + buildState.structureLabel)
                    if recordedState['structureLabel'] == buildState.structureLabel:
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

def updateStructureInfoWithUserOptions(thisTransaction : Transaction, structureInfo : StructureInfo, filename: str):
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
def getStructureInfoFilename(thisTransaction : Transaction):
    log.info("getStructureInfoFilename() was called.")
    try:
        sequence = getSequenceFromTransaction(thisTransaction, 'indexOrdered')
    except Exception as error:
        log.error("There was a problem getting the sequence from the transaction: " + str(error))
        log.error(traceback.format_exc())
        raise error
    else:
        seqID = getSeqIDForSequence(sequence)
        userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/Sequences/"
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
        log.error(traceback.format_exc())
        raise error
    else:
        statusFilename = projectDir + "logs/structureInfo_status.json"

        return statusFilename


def main():
    log.info("main() was called.")

if __name__ == "__main__":
    main()
