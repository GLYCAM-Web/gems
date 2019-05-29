#!/usr/bin/env python3
import sys, os, re
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
    ## First figure out the names of each of the requested services
    if thisTransaction.request_dict['entity']['services'] is None:
        doDefaultService(thisTransaction)
        return
    input_services = thisTransaction.request_dict['entity']['services']
    theServices=getTypesFromList(input_services)
    ## for each requested service
    for i in theServices:
        print("the service is: " + i)
        ## if it is on the local list, do it locally
        ## if not, see if it can be done by common
        ## if none of those, have common build a complaint
    #return theServices


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
 
