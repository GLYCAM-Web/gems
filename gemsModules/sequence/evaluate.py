#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import gemsModules
import gmml
import traceback
import gemsModules.common.utils
from gemsModules.project.projectUtil import *
from gemsModules.project import settings as projectSettings
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.delegator import io as delegatorio
#from gemsModules.common.services import *
#from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from . import settings as sequenceSettings

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

## TODO Write this function
def evaluateSequenceSanity(thisTransaction : Transaction):
    pass
def getSequenceGeometricOptions(thisTransaction : Transaction):
    pass



##   @brief Evaluate a condensed sequence 
#    @detail Evaluating a sequence requires a sequence string and a path to a prepfile.
#    1) Checks sequence for validity,
#    2) Starts a gemsProject.
#    3) builds a default structure, moving it to the output dir
#    3) appends options to transaction
#    4) returns boolan valid
#   @param Transaction thisTransaction
#   @param Service service
#   @return boolean valid
def evaluateCondensedSequence(thisTransaction : Transaction, thisService : Service = None):
    log.info("evaluateCondensedSequence() was called.\n")
    sequence = getSequenceFromTransaction(thisTransaction)
    #Test that this exists.
    if sequence is None:
        log.error("No sequence found in the transaction.")
        raise AttributeError
    else:
        log.debug("sequence: " + sequence)
    this_sequence = gmml.CondensedSequence(sequence)
    valid = this_sequence.GetIsSequenceOkay()
    if valid:
        log.debug("This is a valid sequence: " + sequence) 
        from gemsModules.sequence import build
        builder = build.getCbBuilderForSequence(sequence)
        linkages = getLinkageOptionsFromBuilder(builder)
    else: 
        the_response=this_sequence.GetResponse() 
        log.error("Seq is NOT valid.  The following is the response object:")
        log.error(the_response)
        linkages='Null'
#        raise AttributeError
#    builder = getCbBuilderForSequence(sequence)
#    valid = builder.GetSequenceIsValid()
#    linkages = getLinkageOptionsFromBuilder(builder)
    responseConfig = buildEvaluationResponseConfig(valid, linkages)
    appendResponse(thisTransaction, responseConfig)
    log.debug("Returning from evaluateCondensedSequence.")
    return valid


##  @brief Pass in validation result and linkages, get a responseConfig.
#   @param boolean valid
#   @param dict linkages
#   @return dict config
def buildEvaluationResponseConfig(valid, linkages):
    log.info("buildEvaluationResponseConfig() was called. \n")
    config = {
        "entity" : "Sequence",
        "respondingService" : "SequenceEvaluation",
        "responses" : [{
            "type": "Evaluate",
            "outputs" : [{
                "SequenceValidation" : {
                    "SequenceIsValid" : valid
                }
            },{
                "BuildOptions": {
                    "geometricElements" : [
                        { "Linkages" : linkages }
                    ]
                }
            }]
        }]
    }

    return config



##  @brief Pass a cb builder, get linkage options.
#   @param  CarbohydrateBuilder builder - GMML class.
#   @return dict linkages
def getLinkageOptionsFromBuilder(builder):
    log.info("getLinkageOptionsFromBuilder() was called.\n")
    userOptionsString = builder.GenerateUserOptionsJSON()
    userOptionsJSON = json.loads(userOptionsString)
    optionsResponses = userOptionsJSON['responses']
    for response in optionsResponses:
        log.debug("response.keys: " + str(response.keys()))
        if 'Evaluate' in response.keys():
            if "glycosidicLinkages" in response['Evaluate'].keys():
                linkages = response['Evaluate']['glycosidicLinkages']
                if linkages != None:
                    ## Creating a new dict that can hold a new, derived field.
                    updatedLinkages = []
                    for element in linkages:
                        log.debug("element: " + str(element))
                        if element == None:
                            return None
                        copy = {}
                        for key in element.keys():
                            log.debug("key: " + key)
                            log.debug("element[" + key + "]: " + str(element[key]))
                            copy[key] = {}
                            for gmmlKey in element[key]:
                                copy[key].update({
                                    gmmlKey : element[key][gmmlKey],
                                    'linkageSequence' : element[key]['linkageName']
                                })
                        updatedLinkages.append(copy)
                else:
                    return None
            else: 
                return None

    log.debug("updatedLinkages: " + str(updatedLinkages))
    return updatedLinkages



##  @brief Only validate a condensed sequence. Boolean result.
#   @deprecated.
def validateCondensedSequence(thisTransaction : Transaction, thisService : Service = None):
    log.info("~~~ validateCondensedSequence was called.\n")
    #Look in transaction for sequence
    inputs = thisTransaction.request_dict['entity']['inputs']
    log.debug("inputs: " + str(inputs))

    for input in inputs:
        log.debug("input.keys(): " + str(input.keys()))

        keys = input.keys()

        if 'Sequence' in keys:
            payload = input['Sequence']['payload']
            log.debug("payload: " + payload)
            if payload == None:
                log.error("Could not find Sequence in inputs.")
                ##transaction, noticeBrief, blockId
                common.settings.appendCommonParserNotice( thisTransaction, 'EmptyPayload', 'InvalidInputPayload')
            else:
                log.debug("validating input: " + str(input))
                sequence = payload
                log.debug("getting prepResidues.")
                #Get prep residues
                prepResidues = gmml.condensedsequence_glycam06_residue_tree()
                log.debug("Instantiating an assembly.")
                #Create an assembly
                assembly = gmml.Assembly()

                try:
                    log.debug("Checking sequence sanity.")
                    #Call assembly.CheckCondensed sequence sanity.
                    valid = assembly.CheckCondensedSequenceSanity(sequence, prepResidues)
                    log.debug("validation result: " + str(valid))

                    ## Add valid to the transaction responses.
                    if valid:
                        thisTransaction.response_dict={}
                        thisTransaction.response_dict['entity']={
                                'type' : "sequence",
                        }
                        thisTransaction.response_dict['entity']['responses']=[]
                        log.debug("Creating a response for this sequence.")
                        thisTransaction.response_dict['entity']['responses'].append({
                            "condensedSequenceValidation" : {
                                'sequence': sequence,
                                'valid' : valid,
                            }
                        })
                    else:
                        log.error("~~~\nCheckCondensedSequenceSanity returned false. Creating an error response.")
                        log.error("thisTransaction: "  + str(thisTransaction))
                        log.error(traceback.format_exc())
                        ##appendCommonParserNotice(thisTransaction: Transaction,  noticeBrief: str, blockID: str = None)
                        common.settings.appendCommonParserNotice( thisTransaction,  'InvalidInput', 'InvalidInputPayload')
                except:
                    log.error("Something went wrong while validating this sequence.")
                    log.error("sequence: " + sequence)
                    log.error(traceback.format_exc())
                    common.settings.appendCommonParserNotice( thisTransaction, 'InvalidInput', 'InvalidInputPayload')
        else:
            ##Can be ok, inputs may be provided that are not sequences.
            log.debug("no sequence found in this input, skipping.")
            pass









def main():
    import importlib.util, os, sys
    if importlib.util.find_spec("gemsModules") is None:
        this_dir, this_filename = os.path.split(__file__)
        sys.path.append(this_dir + "/../")
        if importlib.util.find_spec("common") is None:
            print("Something went horribly wrong.  No clue what to do.")
            return
        else:
            from common import utils
    else:
        from gemsModules.common import utils
    data=utils.JSON_From_Command_Line(sys.argv)




if __name__ == "__main__":
    main()

