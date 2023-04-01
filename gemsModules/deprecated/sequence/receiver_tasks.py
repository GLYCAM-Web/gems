#!/usr/bin/env python3
""" Utilities needed by receive.py in the sequence entity """
import os

from gemsModules.deprecated.common import logic as commonlogic
from gemsModules.deprecated.sequence import io as sequenceio

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


def we_should_start_new_project(thisTransaction: sequenceio.Transaction)->bool:
    log.info("we_should_start_new_project() was called.\n")
    if thisTransaction.transaction_in.project is None:
        log.debug("returning true because thisTransaction.transaction_in.project is None")
        return True
    if thisTransaction.transaction_in.project.force_use_this_project:
        return False
    return True

def we_need_filesystem_writes(thisSequenceEntity : sequenceio.sequenceEntity) -> bool:
    # check to see if filesystem writes are needed based on API inspection
    log.info("we_need_filesystem_writes() was called.\n")
    theseNeedFilesystemWrites = ['Build3DStructure', 'DrawGlycan']
    needFilesystemWrites = False
    for service in thisSequenceEntity.services:
        thisService = thisSequenceEntity.services[service]
        if thisService.typename in theseNeedFilesystemWrites:
            log.debug("Found service - " + thisService.typename +
                      " - that needs filesystem writes.")
            needFilesystemWrites = True
        if thisService.typename == 'Evaluate':
            if thisSequenceEntity.inputs.evaluationOptions is None:
                needFilesystemWrites=True
            else:
                if thisSequenceEntity.inputs.evaluationOptions.buildDefaultStructure:
                    needFilesystemWrites=True
                else:
                    needFilesystemWrites=False
    log.debug("returning that needFilesystemWrites is : "  + str(needFilesystemWrites))
    return needFilesystemWrites


def set_up_filesystem_for_writing(thisTransaction: sequenceio.Transaction) -> int:
    # ##
    # Set the project directory
    log.info("set_up_filesystem_for_writing() was called.\n")
    log.debug("and a debug statement was written.\n")
    from gemsModules.deprecated.common.logic import writeStringToFile
    thisProject = thisTransaction.transaction_out.project
    ## CHANGEME ? because could be Evaluate and an associated default build
    ##          the default build is technically a separate service and
    ##          should probably be treated as such.
    thisProject.requested_service = "Build3DStructure" # maybe move setting this and read it here.  Alternate is "EvaluationDefaultBuild"
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

    log.debug("About to write initial logs")
    thisProject.writeInitialLogs()
    log.debug("Just wrote write initial logs")

    # Generate the complete incoming JSON object, including all defaults
    incomingString = thisTransaction.incoming_string
    incomingRequest = thisTransaction.transaction_in.json(indent=2, by_alias=True)
    writeStringToFile(incomingString, os.path.join(
        thisProject.logs_dir, "request-raw.json"))
    writeStringToFile(incomingRequest, os.path.join(
        thisProject.logs_dir, "request-initialized.json"))

    log.debug("set_up_filesystem_for_writing() is returning.\n")
    return 0

def default_structure_exists(transaction_out: sequenceio.sequenceTransactionSchema) -> bool:
    pass

def set_this_build_as_default(transaction_out: sequenceio.sequenceTransactionSchema) -> int:
    pass


