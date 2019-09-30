#!/usr/bin/env python3
import sys, os, re, importlib.util
import gemsModules
import gmml

#from gemsModules import common
#from gemsModules import sequence
#from gemsModules.sequence.entity import *
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from . import settings


##Validate can potentially handle multiple sequences. Top level iterates and 
##  updates transaction.
def validateCondensedSequence(thisTransaction : Transaction, thisService : Service = None):
    print("~~~ validateCondensedSequence was called.")
    #Look in transaction for sequence
    inputs = thisTransaction.request_dict['entity']['inputs']
    print("Number of inputs: " + str(len(inputs)))
    print("inputs: " + str(inputs))
    inputCount = 1
    
    sequences = []
    for input in inputs:
        print("~~~ input# " + str(inputCount))
        payload = input['Sequence']['payload']
        print("payload: " + payload)
        if payload == None:
            print("Could not find Sequence in inputs.")
            ##transaction, noticeBrief, blockId
            common.settings.appendCommonParserNotice( thisTransaction, 'EmptyPayload', 'InvalidInputPayload')
            
        elif payload == "":
            print("Sequence payload is an empty string. Invalid sequence.")
            common.settings.appendCommonParserNotice( thisTransaction, 'EmptyPayload', 'InvalidInputPayload')

        elif "'" in payload:
            print("Sequence contains a single quote. Invalid sequence.")
            common.settings.appendCommonParserNotice( thisTransaction, 'Invalidinput', 'InvalidInputPayload')
        elif "(" in payload:
            print("Sequence contains a parenthesis. Invalid sequence.")
            common.settings.appendCommonParserNotice( thisTransaction,  'InvalidInput', 'InvalidInputPayload')
        elif ")" in payload:
            print("Sequence contains a parenthesis. Invalid sequence.")
            common.settings.appendCommonParserNotice( thisTransaction,  'InvalidInput', 'InvalidInputPayload')
        else:
            print("input: " + str(input))
            sequence = payload
            print("sequence: " + sequence)
            sequences.append(sequence)

            #Get prep residues
            prepResidues = gmml.condensedsequence_glycam06_residue_tree()
            print("prepResidues: \n" + str(prepResidues))

            #Create an assembly
            assembly = gmml.Assembly()
            print("assembly: " + str(assembly))

            #Call assembly.CheckCondensed sequence sanity.
            valid = assembly.CheckCondensedSequenceSanity(sequence, prepResidues)
            print("validation result: " + str(valid))

            ## Add valid to the transaction responses.
            if valid:
                if thisTransaction.response_dict is None:
                    thisTransaction.response_dict={}
                    thisTransaction.response_dict['entity']={}
                if thisTransaction.response_dict['entity'] is None:
                    thisTransaction.response_dict['entity']={}
                if not 'responses' in thisTransaction.response_dict['entity']:
                    thisTransaction.response_dict['entity']['responses']=[]

                print("Creating a response for this sequence.")
                thisTransaction.response_dict['entity']['responses'].append({ 
                    "condensedSequenceValidation" : {
                        'sequence': sequence,
                        'valid' : valid,
                    }
                })
            else:
                thisTransaction.response_dict['responses'].append({ 
                    common.settings.appendCommonParserNotice( thisTransaction,  'Invalidinput', 'InvalidInputPayload')
                })

        inputCount += 1

    print("sequences: " + str(sequences))




    

    

    

    #Update transaction with results so a response string may be built.

## TODO Write this function
def evaluate(thisTransaction : Transaction, thisService : Service = None):
    # from .evaluate import *
    #if ('jsonObjectOutputFormat', 'Pretty') in self.transaction_in.options:
    # evaluateSequenceSanity(thisTransaction : Transaction)
    print("evaluate was called! ...But it has not been written for this module yet.")

def build3DStructure(thisTransaction : Transaction, thisService : Service = None):
    print("~~~ Sequence entity's build3Dstructure was called!")
    import uuid
    theUUID=str(uuid.uuid4())

    inputs = thisTransaction.request_dict['entity']['inputs']
    theInputs=getTypesFromList(inputs)
    if 'Sequence' in theInputs: 
        print("found Sequence in theInputs")
    else:
        #sequence is required. Attach an error response and return.
        common.settings.appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity','Expected Sequence')
        return

    ### This is REALLY REALLY UGLY  PLEASE FIX THIS
    theSequence=list(list(inputs[0].values())[0].values())[0]
    #print(theSequence)

    ## The original way. TODO: delete the subprocess call to the bash file.
    import subprocess
    subprocess.run("$GEMSHOME/gemsModules/sequence/do_the_build.bash '" + theSequence +"' " + theUUID, shell=True)
    print("Attempting to do the build.")

    # projectDir = "/website/userdata/tools/cb/git-ignore-me_userdata/" + str(theUUID) + "/"
    # prepFile = "GLYCAM_06j-1.prep"
    # offFile =  projectDir + "structure.off-test"
    # pdbFile = projectDir + "structure.pdb=test"
    # from . import buildFromSequence
    # buildFromSequence.buildThis(theSequence,  prepFile, offFile, pdbFile)
    
        

    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    if not 'entity' in thisTransaction.response_dict:
        thisTransaction.response_dict['entity']={}
    if not 'type' in thisTransaction.response_dict['entity']:
        thisTransaction.response_dict['entity']['type']='Sequence'
    if not 'responses' in thisTransaction.response_dict:
        thisTransaction.response_dict['responses']=[]

    thisTransaction.response_dict['responses'].append({'Build3DStructure': {'payload': theUUID }})


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
    print("~~~\nSequence entity has received a transaction.")
    import gemsModules.sequence
    ## First figure out the names of each of the requested services
    if not 'services' in thisTransaction.request_dict['entity'].keys():
        print("'services' was not present in the request. Do the default.")
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
                print("The provided service is not recognized. Building and returning an error response.")
                common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
            else:
                pass
        ## if it is known, try to do it
        elif i == "Validate":
            print("Validate service requested from sequence entity.")
            validateCondensedSequence(thisTransaction, None)
        elif i == "Evaluate":
            evaluate(thisTransaction,  None)
        elif i == 'Build3DStructure':
            build3DStructure(thisTransaction ,  None)
        else:
            print("got to the else, so something is wrong")
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
 
