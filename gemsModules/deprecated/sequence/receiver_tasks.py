#!/usr/bin/env python3
""" Utilities needed by receive.py in the sequence entity """
#import json
#import sys
#import os
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
#from gemsModules.deprecated.common import logic as commonlogic
#from gemsModules.deprecated.common import services as commonservices
#from gemsModules.deprecated.sequence import settings as sequenceSettings
from gemsModules.deprecated.sequence import io as sequenceio
#from gemsModules.deprecated.common.logic import writeStringToFile
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
        {'DefaultTest': {'payload': marco('Sequence')}})
    thisTransaction.build_outgoing_string()
    return thisTransaction

# @brief Default service is marco polo. Can change if needed later.
#   @param Transaction thisTransaction
#   @TODO: write this to use transaction_in and transaction_out
def doDefaultService(thisTransaction: sequenceio.Transaction) -> sequenceio.Transaction:
    log.info("doDefaultService() was called.\n")
    return do_marco(thisTransaction) 

def do_status(thisTransaction: sequenceio.Transaction) -> sequenceio.Transaction:
    if thisTransaction.transaction_out.entity.responses is None:
        thisTransaction.transaction_out.entity.responses = {}
        thisTransaction.transaction_out.entity.responses['Get Status']=Response()
        theResponse=thisTransaction.transaction_out.entity.responses['Get Status']
        theResponse.typename='Status'
        theResponse.outputs={'Message':'I am fine.  I hope you are well, too!'}
        thisTransaction.transaction_out.entity.responses['Get Status']=theResponse
    return thisTransaction

def get_sequence(thisSequenceEntity: sequenceio.SequenceEntity)->str:
    """ Get the sequence from the transaction. """
    log.info("get_sequence was called.")
    if thisSequenceEntity.inputs is None:
        return None
    if thisSequenceEntity.inputs.sequence is None: 
        return None
    return thisSequenceEntity.inputs.sequence.payload

def default_structure_exists(thisTransaction: sequenceio.Transaction)-> bool:
    pass

def default_structure_details(thisTransaction: sequenceio.Transaction)-> sequenceio.Single3DStructureBuildDetails:
    pass

def we_should_build_the_default_structure(thisTransaction: sequenceio.Transaction)->bool:
    """ Determine whether or not to build the default sequence. """
    build_default_structure = True
    # See if we are in a situation where we normally need to build the default
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
    return build_default_structure

def we_need_filesystem_writes(thisSequenceEntity : sequenceio.SequenceEntity) -> bool:
    # check to see if filesystem writes are needed
    # Other parts of the code might make decisions based on other criteria
    theseNeedFilesystemWrites = ['Build3DStructure', 'DrawGlycan']
    needFilesystemWrites = False
    for service in thisSequenceEntity.services:
        thisService = thisSequenceEntity.services[service]
        if thisService.typename in theseNeedFilesystemWrites:
            log.debug("Found service - " + thisService.typename +
                      " - that needs filesystem writes.")
            needFilesystemWrites = True
    return needFilesystemWrites



#### START HERE
def set_up_filesystem_for_writing(thisTransaction: sequenceio.SequenceTransaction) -> int:
    # ##
    # Set the project directory
    # ## TODO - this next is why it might fail.  I wasn't sure what better to do (BLF)
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


