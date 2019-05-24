#!/usr/bin/env python3
import sys, os
import gemsModules
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...

## TODO Write this function
def evaluate(thisTransaction : Transaction):
    # from .evaluate import *
    #if ('jsonObjectOutputFormat', 'Pretty') in self.transaction_in.options:
    # evaluateSequenceSanity(thisTransaction : Transaction)
    pass

## TODO Make this not be a call to a compiled binary
def build3DStructure(thisTransaction : Transaction):
    # Check for environment variables that tell where things go
    # check out the environment
    OutputPath = os.environ.get('GEMS_MODULES_SEQUENCE_STRUCTURE_PATH')
    if OutputPath == None:
        OutputPath = os.environ.get('GEMS_MODULES_SEQUENCE_PATH')
    if OutputPath == None:
        OutputPath = os.environ.get('GEMS_MODULES_PATH')
    if OutputPath == None:
        OutputPath = '.' 
    # Set up the location where output files will be stored
    # This next function should check for directory name prefix or
    # if the complete spec is known or if a UUID should be generated
    #    OutputDirectorySpecification = getOutputDirectorySpecification(thisTransaction: Transaction)
    # Set up the location of the MD5Sum directory
    # Set up the location of the prep file to be used
    # Generate directories as needed
    # Save output files to the directories as needed
    # Run the program to generate the files
    # Return the name of the directory where the files reside
    pass
    

def doDefaultService(thisTransaction : Transaction):
    # evaluate(thisTransaction : Transaction)
    # build3DStructure(thisTransaction : Transaction)
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='Sequence'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'payload':marco('Sequence')})
    thisTransaction.build_outgoing_string()

def receive(thisTransaction : Transaction):
    doDefaultService(thisTransaction)


def main():
    pass

if __name__ == "__main__":
  main()
 
