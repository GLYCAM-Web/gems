#!/usr/bin/env python3
""" Utilities needed by receive.py in the sequence entity """
#import json
#import sys
import os
#import re
##import importlib.util
#import shutil
#import uuid
#import traceback
#import gemsModules.deprecated
#import gemsModules.deprecated.sequence

# for key, val in gemsModules.deprecated.delegator.settings.subEntities:
#     if val in gemsModules.deprecated.delegator.settings.deprecated:
#         pass
# prototype: need to build import statement
# from gemsModules.deprecated.deprecated_20221212. + val + import         
    


#from gemsModules.deprecated.common import io as commonio
from gemsModules.deprecated.common import logic as commonlogic
#from gemsModules.deprecated.common import services as commonservices
#from gemsModules.deprecated.sequence import settings as sequenceSettings
from gemsModules.deprecated.sequence import io as sequenceio
#

from gemsModules.deprecated.common.loggingConfig import loggers, createLogger
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


def do_marco(thisTransaction: sequenceio.Transaction) -> sequenceio.Transaction:
    log.info("do_marco() was called.\n")
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}
    thisTransaction.response_dict['entity'] = {}
    thisTransaction.response_dict['entity']['type'] = 'SequenceDefault'
    thisTransaction.response_dict['responses'] = []
    thisTransaction.response_dict['responses'].append(
        {'DefaultTest': {'payload': commonlogic.marco('Sequence')}})
    thisTransaction.build_outgoing_string()
    return thisTransaction


# @brief Default service is marco polo. Can change if needed later.
#   @param Transaction thisTransaction
#   @TODO: write this to use transaction_in and transaction_out
def doDefaultService(thisTransaction: sequenceio.Transaction) -> sequenceio.Transaction:
    log.info("doDefaultService() was called.\n")
    return do_marco(thisTransaction) 


def do_status(thisTransaction: sequenceio.Transaction) -> sequenceio.Transaction:
    log.info("do_status() was called.\n")
    if thisTransaction.transaction_out.entity.responses is None:
        thisTransaction.transaction_out.entity.responses = {}
        thisTransaction.transaction_out.entity.responses['Get Status']=sequenceio.Response()
        theResponse=thisTransaction.transaction_out.entity.responses['Get Status']
        theResponse.typename='Status'
        theResponse.outputs={'Message':'I am fine.  I hope you are well, too!'}
        thisTransaction.transaction_out.entity.responses['Get Status']=theResponse
    return thisTransaction


def get_sequence(thisSequenceEntity: sequenceio.sequenceEntity)->str:
    """ Get the sequence from the transaction. """
    log.info("get_sequence was called.")
    if thisSequenceEntity.inputs is None:
        return None
    if thisSequenceEntity.inputs.sequence is None: 
        return None
    return thisSequenceEntity.inputs.sequence.payload


def we_should_build_the_default_structure_on_validation(thisTransaction: sequenceio.Transaction)->bool:
    """ Determine whether or not to build the default sequence once valid. """
    log.info("we_should_build_the_default_structure_on_validation() was called.\n")
    build_default_structure = True
##  The following would be true if the evaluation were being requested with
##    an "Evaluate" service.  
#    # If there are services defined, and if Build3DStructure is defined, 
#    # then we should not build the default structure because the user has already
#    # defined which structures to build.
#    if thisTransaction.transaction_in.entity.services is not None:
#        for currentService in thisTransaction.transaction_in.entity.services:
#            log.debug("service, currentService: " + str(currentService))
#            thisService = thisTransaction.transaction_in.entity.services[currentService]
#            if thisService.typename == 'Build3DStructure':
#                build_default_structure = False
##  In the meantime, the following should work with what the front end is doing:
    if thisTransaction.transaction_in.mdMinimize == "false":
        build_default_structure = True
    # See if we are not in a situation where we normally need to build the default
    from gemsModules.deprecated.common.logic import getGemsExecutionContext
    the_context = getGemsExecutionContext()
    if the_context == "default": # this is a normal user, so the user decides
        build_default_structure = False
    # Check to see if the default build has been explicitly set (to true or false)
    if thisTransaction.transaction_in.entity.inputs.evaluationOptions is not None:
        if thisTransaction.transaction_in.entity.inputs.evaluationOptions.noBuild is True:
            build_default_structure = False
        if thisTransaction.transaction_in.entity.inputs.evaluationOptions.noBuild is False:
            build_default_structure = True
    log.debug("build_default_structure: " + str(build_default_structure))
    return build_default_structure

def multistructure_build_needs_new_project(thisTransaction: sequenceio.Transaction)->bool:
    log.info("multistructure_build_needs_new_project() was called.\n")
    # Get list of existing structures in the project
    if thisTransaction.transaction_out.project is None:
        return True
    from gemsModules.deprecated.sequence.projects import get_all_conformerIDs_in_project_dir
    existing_structures = get_all_conformerIDs_in_project_dir(thisTransaction.transaction_out.project.project_dir)
    # If existing_structures is empty, then we do not need a new project
    if len(existing_structures) == 0:
        return False
    # Get list of structures to be built
    from gemsModules.deprecated.sequence.structureInfo import generateCombinationsFromRotamerData
    from gemsModules.deprecated.sequence.structureInfo import getStructureDirectoryName
    from gemsModules.deprecated.sequence.structureInfo import buildConformerLabel
    structures_to_build = []
    thisTransaction.evaluateCondensedSequence()
    rotamerData = thisTransaction.getRotamerDataIn()
    if rotamerData is None:
        return True
    maxNumberOfStructuresToBuild = thisTransaction.getNumberStructuresHardLimitIn()
    if maxNumberOfStructuresToBuild is None:
        maxNumberOfStructuresToBuild = thisTransaction.getNumberStructuresHardLimitOut()
    if maxNumberOfStructuresToBuild is None:
        maxNumberOfStructuresToBuild = 64  # please let this not break before we rewrite this code
    sequenceRotamerCombos = generateCombinationsFromRotamerData(
            rotamerData,
            maxNumberCombos=maxNumberOfStructuresToBuild)
    for sequenceRotamerCombo in sequenceRotamerCombos:
        conformerLabel = buildConformerLabel(sequenceRotamerCombo)
        structures_to_build.append(getStructureDirectoryName(conformerLabel))
    # If existing_structures is not a subset of structures_to_build, then we need a new project
    if not set(existing_structures).issubset(set(structures_to_build)):
        return True
    return False

def we_need_filesystem_writes(thisSequenceEntity : sequenceio.sequenceEntity) -> bool:
    # check to see if filesystem writes are needed
    # Other parts of the code might make decisions based on other criteria
    log.info("we_need_filesystem_writes() was called.\n")
    theseNeedFilesystemWrites = ['Build3DStructure', 'DrawGlycan']
    needFilesystemWrites = False
    for service in thisSequenceEntity.services:
        thisService = thisSequenceEntity.services[service]
        if thisService.typename in theseNeedFilesystemWrites:
            log.debug("Found service - " + thisService.typename +
                      " - that needs filesystem writes.")
            needFilesystemWrites = True
    return needFilesystemWrites


def set_up_filesystem_for_writing(thisTransaction: sequenceio.Transaction) -> int:
    # ##
    # Set the project directory
    # ## TODO - this next is why it might fail.  I wasn't sure what better to do (BLF)
    log.info("set_up_filesystem_for_writing() was called.\n")
    from gemsModules.deprecated.common.logic import writeStringToFile
    thisProject = thisTransaction.transaction_out.project
    thisProject.requested_service = "Build3DStructure"
    thisProject.setServiceDir()
    thisProjectDir = os.path.join(
        thisProject.service_dir,
        'Builds',
        thisProject.pUUID)
    thisProject.setProjectDir(
        specifiedDirectory=thisProjectDir, noClobber=False)

    thisProject.setHostUrlBasePath()
    thisProject.setDownloadUrlPath()

    # Create the needed initial directories including a logs directory
    thisProject.createDirectories()

    thisProject.writeInitialLogs

    # Generate the complete incoming JSON object, including all defaults
    incomingString = thisTransaction.incoming_string
    incomingRequest = thisTransaction.transaction_in.json(indent=2)
    writeStringToFile(incomingString, os.path.join(
        thisProject.logs_dir, "request-raw.json"))
    writeStringToFile(incomingRequest, os.path.join(
        thisProject.logs_dir, "request-initialized.json"))

    return 0

