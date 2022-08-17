#!/usr/bin/env python3
import os
import traceback
from gemsModules.sequence import sequence_api as sequenceio
from gemsModules.project import project_api as projectio
from gemsModules.common.loggingConfig import loggers, createLogger
from gemsModules.common.logic import writeStringToFile
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

# @brief Default service is marco polo. Can change if needed later.
#   @param Transaction thisTransaction
#   @TODO: write this to use transaction_in and transaction_out


def doDefaultService(thisTransaction: sequenceio.Transaction):
    log.info("doDefaultService() was called.\n")
    pass
#    if thisTransaction.response_dict is None:
#        thisTransaction.response_dict = {}
#    thisTransaction.response_dict['entity'] = {}
#    thisTransaction.response_dict['entity']['type'] = 'SequenceDefault'
#    thisTransaction.response_dict['responses'] = []
#    thisTransaction.response_dict['responses'].append(
#        {'DefaultTest': {'payload': marco('Sequence')}})
#    thisTransaction.build_outgoing_string()


# @brief The main way Delegator interacts with this module. Request handling.
#   @param Transaction receivedTransactrion
def receive(receivedTransaction: sequenceio.Transaction):
    log.info("sequence.receive() was called:\n")
    log.debug("The received transaction contains this incoming string: ")
    log.debug(receivedTransaction.incoming_string)
    log.debug("request dict: ")
    log.debug(receivedTransaction.request_dict)

    # ##
    # ## Initialize the transaction
    # ##
    # ## This should not need to be done anywhere else in the module.
    # ##
    # ## Ensure that our Transacation is the Sequence variety
    thisTransaction = sequenceio.Transaction(
        receivedTransaction.incoming_string)
    from pydantic import BaseModel, ValidationError
    try:
        # ## Fill out the incoming transaction based on the incoming JSON object
        thisTransaction.populate_transaction_in()
    except ValidationError as e:
        log.error(e)
        log.error(traceback.format_exc())
        thisTransaction.generateCommonParserNotice(
            noticeBrief='JsonParseEror',
            additionalInfo={'hint': str(e)})
        return
    try:
        # ## Initialize the outgoing transaction by copying the incoming transaction
        thisTransaction.initialize_transaction_out_from_transaction_in()
        # For convenience, make a short alias for the entity in the transaction_in
        thisSequence = thisTransaction.transaction_out.entity
    except Exception as error:
        log.error(
            "There was a problem initializing the outgoing transaction : " + str(error))
        log.error(traceback.format_exc())
        raise error
    # ##
    # ## Initialize the project
    # ##
    # ## There should not be many alterations required elsewhere.
    # ##
    # ## Because our transacation is the Sequence variety, the project will be CbProject
    try:
        # ##
        # ## If the outgoing project is None, a new project is needed
        # ##
        if thisTransaction.transaction_out.project is None:
            log.debug("transaction_out.project is None.  Starting a new one.")
            thisTransaction.transaction_out.project = projectio.CbProject()
        # ##
        # ## Initialize the parts of the project that need to be done even if there is no output
        # ## to the filesystem.
        # ##
        log.debug("Initializing the non-filesystem parts of the outgoing project")

        thisProject = thisTransaction.transaction_out.project

        thisProject.setFilesystemPath()

        log.debug("About to load the version info")
        thisProject.loadVersionsFileInfo()
        # ##
        # ## Initialize the parts of the project that are written to the filesystem.
        # ## Also write initialization info to the filesystem.
        # ##
        log.debug(
            "Initializing the filesystem parts of the outgoing project, if any")

        # ##
        # ## TODO - this might fail if more than one service needs filesystem access
        # ##        see next todo for more.
        # ##
        # check to see if filesystem writes are needed
        theseNeedFilesystemWrites = ['Build3DStructure', 'DrawGlycan']
        needFilesystemWrites = False
        for service in thisSequence.services:
            thisService = thisSequence.services[service]
            if thisService.typename in theseNeedFilesystemWrites:
                log.debug("Found service - " + thisService.typename +
                          " - that needs filesystem writes.")
                needFilesystemWrites = True

        if needFilesystemWrites:
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
    except Exception as error:
        log.error(
            "There was a problem initializing the outgoing project: " + str(error))
        log.error(traceback.format_exc())
        raise error
    log.debug("Just initialized the outgoing project.  The transaction_out is :   ")
    log.debug(thisTransaction.transaction_out.json(indent=2))

    ###################################################################
    #
    # these are for logging/debugging and can go if they get heavy
    #
    log.debug("The entity type is : " + thisSequence.entityType)
    log.debug("The services are: ")
    log.debug(thisSequence.services)
    vals = thisSequence.services.values()
    for j in vals:
        if 'Build3DStructure' in j.typename:
            log.debug("Found a build 3d request.")
        elif 'Evaluate' in j.typename:
            log.debug("Found an evaluation request.")
        elif 'Validate' in j.typename:
            log.debug("Found a validation request.")
        else:
            log.debug("Found an unknown service: '" + str(j.typename))
    log.debug("The Seqence Entity's inputs looks like:")
    log.debug(thisSequence.inputs)
    log.debug("The Seqence Entity's inputs.Sequence looks like:")
    log.debug(thisSequence.inputs.sequence.payload)
    ###################################################################

    # First figure out the names of each of the requested services
    if thisSequence.services == []:
        log.debug("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        # TODO: write the following properly
        thisTransaction.doDefaultService()
        return

    log.info("Sequence has been validated. Thank you.")
    # for each requested service:
    for currentService in thisSequence.services:
        log.debug("service, currentService: " + str(currentService))
        thisService = thisSequence.services[currentService]

        # OGNov21: Always validate the sequence. If not valid, always stop.
        # Can remove all other sequence validation checks from sequence code.
        # Note that "payload" is used above, no need to check here.
        # Instantiating carbBuilder in multiple places isn't great design.
        # Wrapping just the new condensedSequence class wasn't possible for Oliver's poor brain.
        # doing thisTransaction.generateCommonParserNotice before the "for currentService ..." loop causes a "doesn't exist" fault
        from gemsModules.sequence import build
        carbBuilder = build.getCbBuilderForSequence(
            thisSequence.inputs.sequence.payload)
        valid = carbBuilder.IsStatusOk()
        if not valid:
            # Is incorrect user input an error?
            log.error(carbBuilder.GetStatusMessage())
            log.debug(
                "Just about to call generateCommonParserNotice with the outgoing project.  The transaction_out is :   ")
            log.debug(thisTransaction.transaction_out.json(indent=2))
            thisTransaction.generateCommonParserNotice(
                noticeBrief='InvalidInputPayload', exitMessage=carbBuilder.GetStatusMessage())
            # prepares the transaction for return to the requestor, success or fail.
            # NOTE!!! This uses the child method in sequence.io - a better method!
            thisTransaction.build_outgoing_string()
            return thisTransaction
        # End OGNov21 edit.
        if 'Evaluate' in thisService.typename:
            log.debug("Evaluate service requested from sequence entity.")
            from gemsModules.sequence import evaluate
            try:
                thisTransaction.evaluateCondensedSequence()
                if thisTransaction.transaction_out.entity.inputs.evaluationOptions is not None:
                    if thisTransaction.transaction_out.entity.inputs.evaluationOptions.noBuild is False:
                        # Build the Default structure.
                        from gemsModules.sequence import logic
                        thisTransaction.manageSequenceBuild3DStructureRequest(
                            defaultOnly=True)
            except Exception as error:
                log.error(
                    "There was a problem evaluating the condensed sequence: " + str(error))
                log.error(traceback.format_exc())
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='InvalidInputPayload')
        elif 'Build3DStructure' in thisService.typename:
            log.debug("Build3DStructure service requested from sequence entity.")
            try:
                # first evaluate the requested structure. Only build if valid.
                from gemsModules.sequence import evaluate
                thisTransaction.evaluateCondensedSequence()
                valid = thisTransaction.transaction_out.entity.outputs.sequenceEvaluationOutput.sequenceIsValid
                thisTransaction.setIsEvaluationForBuild(True)
            except Exception as error:
                log.error(
                    "There was a problem evaluating the condensed sequence: " + str(error))
                log.error(traceback.format_exc())
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='InvalidInputPayload')
            else:
                if valid:
                    log.debug("Valid sequence.")
                    try:
                        from gemsModules.sequence import logic
                        thisTransaction.manageSequenceBuild3DStructureRequest()

                    except Exception as error:
                        log.error(
                            "There was a problem with manageSequenceBuild3DStructureRequest(): " + str(error))
                        raise error
                else:
                    log.error("Invalid Sequence. Cannot build.")
                    print("the transaction is : ")
                    print(thisTransaction)
                    thisTransaction.generateCommonParserNotice(
                        noticeBrief='InvalidInputPayload', additionalInfo={"hint": "Sequence is invalid"})
        elif "Validate" in thisService.typename:
            log.debug("Validate service requested from sequence entity.")
            from gemsModules.sequence import evaluate
            try:
                thisTransaction.evaluateCondensedSequence(validateOnly=True)
            except Exception as error:
                log.error(
                    "There was a problem validating the condensed sequence: " + str(error))
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='InvalidInputPayload')
        else:
            log.error("got to the else, so something is wrong")
            thisTransaction.generateCommonParserNotice(
                noticeBrief='ServiceNotKnownToEntity')

    # prepares the transaction for return to the requestor, success or fail.
    # NOTE!!! This uses the child method in sequence.io - a better method!
    thisTransaction.build_outgoing_string()
    if needFilesystemWrites:
        outgoingResponse = thisTransaction.transaction_out.json(indent=2)
        writeStringToFile(outgoingResponse, os.path.join(
            thisProject.logs_dir, "response.json"))
    return thisTransaction


def main():
    log.info("main() was called.\n")


if __name__ == "__main__":
    main()
