#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil
import gemsModules
import gmml
import traceback

#from gemsModules import common
#from gemsModules import sequence
#from gemsModules.sequence.receive import *
import gemsModules.common.utils
from gemsModules.project.projectUtil import *
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from . import settings

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.ERROR

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

##Validate can potentially handle multiple sequences. Top level iterates and
##  updates transaction.
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

"""
Evaluating a sequence requires a sequence string and a path to a prepfile.
    1) Checks sequence for validity,
    2) Starts a gemsProject.
    3) builds a default structure, moving it to the output dir
    3) returns options that a user might want to set.
"""
def evaluateCondensedSequence(thisTransaction : Transaction, thisService : Service = None):
    log.info("evaluateCondensedSequence() was called.\n")
    request_dict = thisTransaction.request_dict

    inputs = request_dict['entity']['inputs']
    for element in inputs:
        log.debug("element: " + str(element))
        if "Sequence" in element.keys():
            sequence = element['Sequence']['payload']
        else:
            log.debug("Skipping")

    #TODO: test that this exists.
    if sequence is None:
        log.error("No sequence found in the transaction.")
        ##TODO: return an error
    else:
        log.debug("sequence: " + sequence)

    GemsPath = os.environ.get('GEMSHOME')
    if GemsPath == None:
        this_dir, this_filename = os.path.split(__file__)
        log.error("""

        GEMSHOME environment variable is not set.

        Set it using somthing like:

          BASH:  export GEMSHOME=/path/to/gems
          SH:    setenv GEMSHOME /path/to/gems
        """)
    log.debug("GemsPath: " + GemsPath )

    ##TODO: test that this exists.
    prepfile = GemsPath + "/gemsModules/sequence/GLYCAM_06j-1.prep"
    if os.path.exists(prepfile):
        builder = gmml.carbohydrateBuilder(sequence, prepfile)
        valid = builder.GetSequenceIsValid()
        log.debug("valid: " + str(valid))
        if valid:
            userOptionsString = builder.GenerateUserOptionsJSON()
            log.debug("userOptions: " + userOptionsString)
            userOptionsJSON = json.loads(userOptionsString)
            responses = userOptionsJSON['responses']
            for response in responses:
                log.debug("response.keys: " + str(response.keys()))
                if 'Evaluate' in response.keys():
                    linkages = response['Evaluate']['glycosidicLinkages']

                    if thisTransaction.response_dict is None:
                        thisTransaction.response_dict={}
                    if not 'entity' in thisTransaction.response_dict:
                        thisTransaction.response_dict['entity']={}
                    if not 'type' in thisTransaction.response_dict['entity']:
                        thisTransaction.response_dict['entity']['type']='Sequence'
                    if not 'responses' in thisTransaction.response_dict:
                        thisTransaction.response_dict['responses']=[]

                    log.debug("Creating a response for this sequence.")
                    thisTransaction.response_dict['responses'].append({
                        "SequenceEvaluation" : {
                            "type": "Evaluate",
                            "outputs" : [{
                                "SequenceValidation" : {
                                    "SequenceIsValid" : valid
                                    }
                                },{
                                "BuildOptions": {
                                    "options" : [
                                            { "Linkages" : linkages }
                                        ]
                                    }

                                }
                            ]
                        }
                    })
        else:
            log.error("Prepfile did not exist at: " + prepfile)
            common.settings.appendCommonParserNotice(thisTransaction, 'InvalidInput', 'InvalidInputPayload')
    else:
        log.error("This sequence is invalid: " + sequence)
        common.settings.appendCommonParserNotice( thisTransaction, 'InvalidInput', 'InvalidInputPayload')



def build3DStructure(thisTransaction : Transaction, thisService : Service = None):
    log.info("Sequence receive.py build3Dstructure() was called.\n")
    ##TODO: See if a project has already been started first.
    startProject(thisTransaction)
    pUUID=thisTransaction.response_dict['gems_project']['pUUID']

    inputs = thisTransaction.request_dict['entity']['inputs']

    for thisInput in inputs:
        log.debug("thisInput: " + str(thisInput))
        inputKeys = thisInput.keys()
        if "Sequence" in inputKeys:
            theSequence = thisInput['Sequence']['payload']
            if thisTransaction.response_dict is None:
                thisTransaction.response_dict={}
            if not 'entity' in thisTransaction.response_dict:
                thisTransaction.response_dict['entity']={}
            if not 'type' in thisTransaction.response_dict['entity']:
                thisTransaction.response_dict['entity']['type']='Sequence'
            if not 'responses' in thisTransaction.response_dict:
                thisTransaction.response_dict['responses']=[]

            thisTransaction.response_dict['responses'].append({'Build3DStructure': {'payload': pUUID }})

        if theSequence is None:
            #sequence is required. Attach an error response and return.
            common.settings.appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity','Expected Sequence')
            return

        ## The original way. TODO: delete the subprocess call to the bash file.
        import subprocess
        subprocess.run("$GEMSHOME/gemsModules/sequence/do_the_build.bash '" + theSequence +"' " + pUUID, shell=True)

"""
Default service is marco polo. Should this be something else?
"""
def doDefaultService(thisTransaction : Transaction):
    log.info("doDefaultService() was called.\n")
    # evaluate(thisTransaction : Transaction)
    # build3DStructure(thisTransaction : Transaction)
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='SequenceDefault'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'DefaultTest': {'payload':marco('Sequence')}})
    thisTransaction.build_outgoing_string()

def receive(thisTransaction : Transaction):
    log.info("receive() was called:\n")
    import gemsModules.sequence
    ## First figure out the names of each of the requested services
    if not 'services' in thisTransaction.request_dict['entity'].keys():
        log.debug("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        return

    input_services = thisTransaction.request_dict['entity']['services']
    theServices=getTypesFromList(input_services)

    ## for each requested service
    for i in theServices:
        #####  the automated module loading doesn't work, and I can't figure out how to make it work,
              # that is:
              #  requestedModule='.'+settings.serviceModules[i]
              #  the_spec = importlib.util.find_spec('.sequence.entity.evaluate',gemsModules)
              # .... and many variants thereof
        #####  so, writing something ugly for now
        if i not in settings.serviceModules.keys():
            if i not in common.settings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
            else:
                pass
        ## if it is known, try to do it
        elif i == "Validate":
            log.debug("Validate service requested from sequence entity.")
            validateCondensedSequence(thisTransaction, None)
        elif i == "Evaluate":
            log.debug("Evaluate service requested from sequence entity.")
            evaluateCondensedSequence(thisTransaction,  None)
        elif i == 'Build3DStructure':
            log.debug("Build3DStructure service requested from sequence entity.")
            build3DStructure(thisTransaction ,  None)
        else:
            log.error("got to the else, so something is wrong")
            common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
    thisTransaction.build_outgoing_string()


# Some alternate ways to interrogate lists:
#    if any("Evaluate" in s for s in input_services ):
#        print("It is here!")
#    types=[s for s in input_services if "type" in s.values()]
#    evaluations=[s for s in input_services if "Evaluate" in s]
#    print(evaluations)


def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

