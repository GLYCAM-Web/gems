#!/usr/bin/env python3
import os
import traceback

## Not sure what this was originally intended for.  Leaving for now.  BLF
# for key, val in gemsModules.deprecated.delegator.settings.subEntities:
#     if val in gemsModules.deprecated.delegator.settings.deprecated:
#         pass
# prototype: need to build import statement
# from gemsModules.deprecated.deprecated_20221212. + val + import         

from gemsModules.deprecated.sequence import io as sequenceio
from gemsModules.deprecated.sequence import receiver_tasks 

from gemsModules.deprecated.common.loggingConfig import loggers, createLogger
from gemsModules.deprecated.common.logic import writeStringToFile
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

# @brief The main way Delegator interacts with this module. Request handling.
#   @param Transaction receivedTransactrion
def receive(receivedTransaction: sequenceio.Transaction) -> sequenceio.Transaction:
    log.info("sequence.receive() was called:\n")
    log.debug("The received transaction contains this incoming string: ")
    log.debug(receivedTransaction.incoming_string)
    log.debug("request dict: ")
    log.debug(receivedTransaction.request_dict)

    # ## Initialize the transaction
    from pydantic import ValidationError
    thisTransaction = sequenceio.Transaction(receivedTransaction.incoming_string)
    try:
        thisTransaction.populate_transaction_in()
    except ValidationError as e:
        log.error(e)
        log.error(traceback.format_exc())
        thisTransaction.generateCommonParserNotice(
            noticeBrief='JsonParseEror',
            additionalInfo={'hint': str(e)})
        return thisTransaction
    try:
        thisTransaction.initialize_transaction_out_from_transaction_in()
        # For convenience, make a short alias for the entity in the transaction_in
        thisSequenceEntity = thisTransaction.transaction_out.entity
    except Exception as error:
        log.error(
            "There was a problem initializing the outgoing transaction : " + str(error))
        log.error(traceback.format_exc())
        raise  # not sure if this will work as desired - BLFoley 2023-03-15
               # it might be necessary to generate a transaction to return and
               # populate it with an error message.
   

    has_a_sequence = False

    ## If there is a sequence, ensure that it is valid
    the_sequence = receiver_tasks.get_sequence(thisSequenceEntity)
    if the_sequence is not None:
        has_a_sequence = True
        from gemsModules.deprecated.sequence import build
        carbBuilder = build.getCbBuilderForSequence(the_sequence)
        valid = carbBuilder.IsStatusOk()
        if not valid:
            log.error(carbBuilder.GetStatusMessage())
            log.debug(
                "About to call generateCommonParserNotice with the outgoing project.  The transaction_out is :   ")
            log.debug(thisTransaction.transaction_out.json(indent=2))
            thisTransaction.generateCommonParserNotice(
                noticeBrief='InvalidInputPayload', 
                exitMessage=carbBuilder.GetStatusMessage())
            thisTransaction.build_outgoing_string()
            return thisTransaction
        log.debug("Sequence is valid.")


    # If there are no explicit services
    if thisSequenceEntity.services == []:
        log.debug("'services' was not present in the request. Do the default.")
        thisTransaction = receiver_tasks.doDefaultService(thisTransaction)
        return thisTransaction


    # ## Initialize the project
    try:
        need_new_project = receiver_tasks.we_should_start_new_project(thisTransaction)
        if need_new_project:
            log.debug("We need a new project.  Starting a new one.")
            from gemsModules.deprecated.project import io as projectio
            thisTransaction.transaction_out.project = projectio.CbProject()

        log.debug("Initializing the non-filesystem-writing parts of the outgoing project")
        thisProject = thisTransaction.transaction_out.project
        thisProject.setFilesystemPath()
        log.debug("About to load the version info")
        thisProject.loadVersionsFileInfo()
        thisTransaction.transaction_out.project=thisProject

        need_filesystem_writes = receiver_tasks.we_need_filesystem_writes(thisSequenceEntity)
        log.debug("Initializing the filesystem parts of the outgoing project, if any")
        if need_filesystem_writes:
            # ## TODO - this might fail if more than one service needs filesystem access
            return_value = receiver_tasks.set_up_filesystem_for_writing(thisTransaction)
            if return_value != 0:
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='GemsError',
                    additionalInfo={'Message': 'Something went wrong while setting up the filesystem.'})

    except Exception as error:
        log.error(
            "There was a problem initializing the outgoing project: " + str(error))
        log.error(traceback.format_exc())
        raise Exception
    log.debug("Just initialized the outgoing project.  The transaction_out is :   ")
    log.debug(thisTransaction.transaction_out.json(indent=2))

    ###################################################################
    #
    # these are for logging/debugging and can go if they get heavy
    #
    log.debug("The entity type is : " + thisSequenceEntity.entityType)
    log.debug("The services are: ")
    log.debug(thisSequenceEntity.services)
    vals = thisSequenceEntity.services.values()
    for j in vals:
        if 'Build3DStructure' in j.typename:
            log.debug("Found a build 3d request.")
        elif 'Evaluate' in j.typename:
            log.debug("Found an evaluation request.")
        elif 'Validate' in j.typename:
            log.debug("Found a validation request.")
        elif 'Status' in j.typename:
            log.debug("Found a status request.")
        elif 'Marco' in j.typename:
            log.debug("Found a marco request.")
        else:
            log.debug("Found an unknown service: '" + str(j.typename))
    log.debug("The Seqence Entity's inputs looks like:")
    log.debug(thisSequenceEntity.inputs)
    log.debug("The Seqence Entity's inputs.Sequence looks like:")
    log.debug(thisSequenceEntity.inputs.sequence.payload)
    ###################################################################



    # for each explicit service:
    for currentService in thisSequenceEntity.services:
        log.debug("service, currentService: " + str(currentService))
        thisService = thisSequenceEntity.services[currentService]

        if 'Evaluate' in thisService.typename:
            log.debug("Evaluate service requested from sequence entity.")
            try:
                thisTransaction.evaluateCondensedSequence()
                if thisTransaction.transaction_in.entity.inputs.evaluationOptions is not None:
                    if not thisTransaction.transaction_in.entity.inputs.evaluationOptions.buildDefaultStructure:
                        continue
                # If still here, then we need to build the default structure
                thisTransaction.setNumberStructuresHardLimitOut(1) # because see next comment
                # The 'defaultOnly=True' part might not be working
                thisTransaction.manageSequenceBuild3DStructureRequest(defaultOnly=True)
            except Exception as error:
                log.error(
                    "There was a problem evaluating the condensed sequence: " + str(error))
                log.error(traceback.format_exc())
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='InvalidInputPayload')
        elif 'Build3DStructure' in thisService.typename:
            log.debug("Build3DStructure service requested from sequence entity.")
            # Sequence was validated above.  Should not be needed again.
            try:
                else:
                    thisTransaction.manageSequenceBuild3DStructureRequest()
            except Exception as error:
                log.error(
                    "There was a problem with manageSequenceBuild3DStructureRequest(): " + str(error))
                raise error
        elif "Validate" in thisService.typename:
            # this should be able to become part of previous validation, but leaving in for now
            log.debug("Validate service requested from sequence entity.")
            try:
                thisTransaction.evaluateCondensedSequence(validateOnly=True)
            except Exception as error:
                log.error(
                    "There was a problem validating the condensed sequence: " + str(error))
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='InvalidInputPayload')
        elif "Status" in thisService.typename:
            # this should be able to become part of previous validation, but leaving in for now
            log.debug("Status service requested from sequence entity.")
            try:
                thisTransaction = receiver_tasks.do_status(thisTransaction)
            except Exception as error:
                log.error(
                    "There was a problem getting status for sequence: " + str(error))
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='InvalidInputPayload')
        elif "Marco" in thisService.typename:
            # this should be able to become part of previous validation, but leaving in for now
            log.debug("Marco service requested from sequence entity.")
            try:
                thisTransaction = receiver_tasks.do_marco(thisTransaction)
            except Exception as error:
                log.error(
                    "There was a problem running marco for sequence: " + str(error))
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='InvalidInputPayload')
        else:
            log.error("got to the else, so something is wrong")
            thisTransaction.generateCommonParserNotice(
                noticeBrief='ServiceNotKnownToEntity')

    # prepares the transaction for return to the requestor, success or fail.
    # NOTE!!! This uses the child method in sequence.io - a better method!
    thisTransaction.build_outgoing_string()
    if need_filesystem_writes:
        outgoingResponse = thisTransaction.transaction_out.json(indent=2)
        writeStringToFile(outgoingResponse, os.path.join(
            thisProject.logs_dir, "response.json"))
    return thisTransaction


def main():
    log.info("main() was called.\n")


if __name__ == "__main__":
    main()
