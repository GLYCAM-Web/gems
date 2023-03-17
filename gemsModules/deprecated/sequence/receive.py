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
        raise Exception  # not sure if this will work as desired - BLFoley 2023-03-15
                         # it might be necessary to generate a transaction to return and
                         # populate it with an error message.
   


    ## If there is a sequence, ensure that it is valid
    build_the_default = False
    the_sequence = receiver_tasks.get_sequence(thisSequenceEntity)
    number_of_structures = -1
    if the_sequence is not None:
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
        log.info("Sequence has been validated. Thank you.")
        number_of_structures = carbBuilder.GetNumberOfShapes()
        if number_of_structures == -1:
            log.error("Number of shapes returned -1")
            log.debug("The sequence is:  ")
            log.debug(str(the_sequence))
            thisTransaction.generateCommonParserNotice(
                noticeBrief='InvalidInputPayload', 
                exitMessage=carbBuilder.GetStatusMessage()
                additionalInfo={'Message': 'Something went wrong determining the number of conformers.'})
                )
            thisTransaction.build_outgoing_string()
            return thisTransaction
        if int(number_of_shapes)


########

## Work on logic here....  

    ## Sequence is valid... yay... so....
    ## Is there already a default structure?  If so, register it and be done.
    ## Else....
    ## Is it a single conforer or multiple conformers?
        ## Single?  only one project is needed - write to the filesystem
        ## Multiple?  Make a project for the default structure and start the build



##  ok... do this.
##  
##  If there is a single structure, just do what has been done all along
##  
##  If there are multiple structures, after Evaluation: 
##      -  The default build will use a separate project made just for that. 
##      -  The evaluation that is returned will include, for the default:
##          - pUUID 
##          - SeqID 
##          - ConformerID 
##          - Download paths for minimized and unminimized.  
##  
##  When the Build request comes:
##      -  The Build request might contain the pUUID for the default
##          - Or any other pUUID.  Doesn't matter.
##      -  If all conformers in the incoming pUUID are part of the 
##          build request, then the pUUID will be retained.
##      -  If not, then a new project will be started.
##  



        ## If a default build is indicated, set up to do a default build below
        if receiver_tasks.we_should_build_the_default_structure(thisTransaction): 
            build_the_default = True

    # If we still need to build the default structure, do it now
    if build_the_default:
        thisTransaction.evaluateCondensedSequence()
        thisTransaction.manageSequenceBuild3DStructureRequest(defaultOnly=True)

########

    # ## Initialize the project
    try:
        if thisTransaction.transaction_out.project is None:
            log.debug("transaction_out.project is None.  Starting a new one.")
            thisTransaction.transaction_out.project = gemsModules.deprecated.project.io.CbProject()

        log.debug("Initializing the non-filesystem-writing parts of the outgoing project")
        thisProject = thisTransaction.transaction_out.project
        thisProject.setFilesystemPath()
        log.debug("About to load the version info")
        thisProject.loadVersionsFileInfo()
        thisTransaction.transaction_out.project=thisProject

        log.debug("Initializing the filesystem parts of the outgoing project, if any")
        if build_the_default or receiver_tasks.we_need_filesystem_writes(thisSequenceEntity):
            # ## TODO - this might fail if more than one service needs filesystem access
            return_value = receiver_tasks.set_up_filesystem_for_writing(thisTransaction)
            if return_value != 0:
                thisTransaction.generateCommonParserNotice(
                    noticeBrief='GemsEror',
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



    # If we still need to build the default structure, do it now
    if build_the_default:
        thisTransaction.evaluateCondensedSequence()
        thisTransaction.manageSequenceBuild3DStructureRequest(defaultOnly=True)



    # Figure out if there are any explicit services
    if thisSequenceEntity.services == []:
        log.debug("'services' was not present in the request. Do the default.")
        thisTransaction = receiver_tasks.doDefaultService(thisTransaction)
        return thisTransaction

    # for each explicit service:
    for currentService in thisSequenceEntity.services:
        log.debug("service, currentService: " + str(currentService))
        thisService = thisSequenceEntity.services[currentService]

        if 'Evaluate' in thisService.typename:
            log.debug("Evaluate service requested from sequence entity.")
            from gemsModules.deprecated.sequence import evaluate
            try:
                thisTransaction.evaluateCondensedSequence()
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
                from gemsModules.deprecated.sequence import evaluate
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
                        from gemsModules.deprecated.sequence import logic
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
            # this should be able to become part of previous validation, but leaving in for now
            log.debug("Validate service requested from sequence entity.")
            from gemsModules.deprecated.sequence import evaluate
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
    if needFilesystemWrites:
        outgoingResponse = thisTransaction.transaction_out.json(indent=2)
        writeStringToFile(outgoingResponse, os.path.join(
            thisProject.logs_dir, "response.json"))
    return thisTransaction


def main():
    log.info("main() was called.\n")


if __name__ == "__main__":
    main()
