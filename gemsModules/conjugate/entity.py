#!/usr/bin/env python3
import gemsModules
from gemsModules import common 
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...

def doDefaultService(thisTransaction):
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='Conjugate'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'payload':marco('Conjugate')})
    thisTransaction.build_outgoing_string()

def receive(thisTransaction):
    #print("Conjugate received it")
    doDefaultService(thisTransaction)

def main():
  import importlib.util, os, sys
  #from importlib import util
  if importlib.util.find_spec("gemsModules") is None:
    this_dir, this_filename = os.path.split(__file__)
    sys.path.append(this_dir + "/../")
    if importlib.util.find_spec("common") is None:
      print("Something went horribly wrong.  No clue what to do.")
      sys.exit(1)
    else:
      from common import utils
  else:
    from gemsModules.common import utils
  utils.investigate_gems_setup(sys.argv)
 
  with open(sys.argv[1], 'r') as file:
    jsonObjectString = file.read().replace('\n', '')
  responseObjectString=delegate(jsonObjectString)
  print(responseObjectString)


if __name__ == "__main__":
  main()
 
