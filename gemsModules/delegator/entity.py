#!/usr/bin/env python3
import gemsModules.common as gMC
from gMC.services import parseInput, doServices
from gMC.transactions import Transaction # might need whole file...

def delegate(jsonObjectString):
    """
    Call other modules based on the contents of jsonObjectString.

    Returns a JSON object in string form.  Can be pretty-printed.

    First, a new Transaction obect is made.  This object holds all the
    information about the delegated work.  To initialize it, we give it
    the incoming JSON object, which is then interrogated by parseInput 
    in the common.services module.  If that goes well, this function 
    reads the identity of the top-level Entity and, if it can load a
    module for that entity, it passes the Transaction object over.
    """

    # Make a new Transaction object for holding I/O information.
    thisTransaction=Transaction(jsonObjectString)

    # If the incoming string was improperly formed, bail, but give a reason.
    if parseInput(thisTransaction) != 0:
        thisTransaction.build_outgoing_string()
        return thisTransaction.outgoing_string

    ###
    ###  TODO:  This is going to need recursion down to the 
    ###  lowest-level Entities at the top level.  Not doing that yet.
    ###
    ###  Entities referenced within Services will need this, too, so
    ###  this should probably be a module in common.services.
    ###
    # See if it is possible to load a module for the requested Entity
    theEntity = importEntity(thisTransaction.request_dict['entity']['type'])
    if theEntity is None:
        thisTransaction.build-general-error-output()
    elif not 'services' in thisTransaction.request_dict['entity']:
        theEntity.entity.doDefaultService(thisTransaction)
    else:
        theEntity.entity.receiving(thisTransaction)

    # Check to see if an outgoing string got built.  If not, try to
    # build one.  If that still doesn't work, make the string be a
    # generic error output JSON object. 
    if thisTransaction.outgoing_string = None:
        thisTransaction.build_outgoing_string()
    if thisTransaction.outgoing_string = None:
        thisTransaction.build-general-error-output()

    # Return whatever outgoing string got made
    return thisTransaction.outgoing_string

def doDefaultService(Transaction thisTransaction):
    """This might not be necessary... """
    from services import marco
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='Delegator'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'payload':marco('Delegator')})
    thisTransaction.build_outgoing_string()

def defaultService(theObject):
    ## TODO give me something to do...
    import json
    responseObject={
            "entity" : "Delegator",
            "responses" : [
                {
                    'payload' : 'there is no default yet'
                    }
                ]
            }
    #print(json.dumps(responseObject))
    return json.dumps(responseObject)

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
    jsonObject = file.read().replace('\n', '')
  responseObject=delegate(jsonObject)
  print(responseObject)


if __name__ == "__main__":
  main()
 
