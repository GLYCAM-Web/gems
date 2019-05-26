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
 
