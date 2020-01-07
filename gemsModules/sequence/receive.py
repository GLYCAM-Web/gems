#!/usr/bin/env python3
import sys, os, re, importlib.util
import gemsModules
import gmml

#from gemsModules import common
#from gemsModules import sequence
#from gemsModules.sequence.receive import *
import gemsModules.common.utils
from gemsModules.project.projectUtil import *
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from . import settings

##Validate can potentially handle multiple sequences. Top level iterates and
##  updates transaction.
def validateCondensedSequence(thisTransaction : Transaction, thisService : Service = None):
#    print("~~~ validateCondensedSequence was called.")
    #Look in transaction for sequence
    inputs = thisTransaction.request_dict['entity']['inputs']
#    print("inputs: " + str(inputs))

    for input in inputs:
#        print("input.keys(): " + str(input.keys()))

        keys = input.keys()

        if 'Sequence' in keys:
            payload = input['Sequence']['payload']
#            print("payload: " + payload)
            if payload == None:
#                print("Could not find Sequence in inputs.")
                ##transaction, noticeBrief, blockId
                common.settings.appendCommonParserNotice( thisTransaction, 'EmptyPayload', 'InvalidInputPayload')
            else:
#                print("validating input: " + str(input))
                sequence = payload
#                print("getting prepResidues.")
                #Get prep residues
                prepResidues = gmml.condensedsequence_glycam06_residue_tree()
#                print("Instantiating an assembly.")
                #Create an assembly
                assembly = gmml.Assembly()

                try:
#                    print("Checking sequence sanity.")
                    #Call assembly.CheckCondensed sequence sanity.
                    valid = assembly.CheckCondensedSequenceSanity(sequence, prepResidues)
#                    print("validation result: " + str(valid))

                    ## Add valid to the transaction responses.
                    if valid:
                        thisTransaction.response_dict={}
                        thisTransaction.response_dict['entity']={
                                'type' : "sequence",
                        }
                        thisTransaction.response_dict['entity']['responses']=[]
#                       print("Creating a response for this sequence.")
                        thisTransaction.response_dict['entity']['responses'].append({
                            "condensedSequenceValidation" : {
                                'sequence': sequence,
                                'valid' : valid,
                            }
                        })
                    else:
#                        print("~~~\nCheckCondensedSequenceSanity returned false. Creating an error response.")
                        #print("thisTransaction: "  + str(thisTransaction))
                        ##appendCommonParserNotice(thisTransaction: Transaction,  noticeBrief: str, blockID: str = None)
                        common.settings.appendCommonParserNotice( thisTransaction,  'InvalidInput', 'InvalidInputPayload')
                except:
#                    print("Something went wrong while validating this sequence.")
#                    print("sequence: " + sequence)
                    common.settings.appendCommonParserNotice( thisTransaction, 'InvalidInput', 'InvalidInputPayload')
        else:
            pass
#            print("no sequence found in this input, skipping.")


## TODO Write this function
def evaluate(thisTransaction : Transaction, thisService : Service = None):
    pass
    # from .evaluate import *
    #if ('jsonObjectOutputFormat', 'Pretty') in self.transaction_in.options:
    # evaluateSequenceSanity(thisTransaction : Transaction)
#    print("evaluate was called! ...But it has not been written for this module yet.")

def build3DStructure(thisTransaction : Transaction, thisService : Service = None):
#    print("~~~ Sequence receive.py build3Dstructure() was called!")
    startProject(thisTransaction)
    pUUID=thisTransaction.response_dict['gems_project']['pUUID']

    inputs = thisTransaction.request_dict['entity']['inputs']

    for thisInput in inputs:
#        print("thisInput: " + str(thisInput))
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




def doDefaultService(thisTransaction : Transaction):
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
#    print("~~~\nSequence entity has received a transaction.")
#    print(" the verbosity is : " + verbosity)
    import gemsModules.sequence
    ## First figure out the names of each of the requested services
    if not 'services' in thisTransaction.request_dict['entity'].keys():
#        print("'services' was not present in the request. Do the default.")
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
#                print("The requested service is not recognized.")
                common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
            else:
                pass
        ## if it is known, try to do it
        elif i == "Validate":
#            print("Validate service requested from sequence entity.")
            validateCondensedSequence(thisTransaction, None)
        elif i == "Evaluate":
            evaluate(thisTransaction,  None)
        elif i == 'Build3DStructure':
            build3DStructure(thisTransaction ,  None)
        else:
#            print("got to the else, so something is wrong")
            common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
    thisTransaction.build_outgoing_string()



# Some alternate ways to interrogate lists:
#    if any("Evaluate" in s for s in input_services ):
#        print("It is here!")
#    types=[s for s in input_services if "type" in s.values()]
#    evaluations=[s for s in input_services if "Evaluate" in s]
#    print(evaluations)


def main():
    pass

if __name__ == "__main__":
  main()

