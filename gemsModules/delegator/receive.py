#!/usr/bin/env python3
import gemsModules
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...

def delegate(jsonObjectString):
    print("~~~\nDelegator receive.py delegate() was called.\n~~~")
    #print("jsonObjectString: \n" + jsonObjectString)

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
        print(" There was an error! ")
        #exit(1)
        thisTransaction.build_outgoing_string()
        return thisTransaction.outgoing_string

    """
      TODO:  This is going to need recursion down to the
      lowest-level Entities at the top level.  Not doing that yet.
      And, not that the models in transaction.py can handle it either.

      Entities referenced within Services will need this, too, so
      this should probably be a module in common.services.
    """
    # See if it is possible to load a module for the requested Entity
    entityType = thisTransaction.request_dict['entity']['type']
    print("entityType: " + entityType)
    theEntity = importEntity(entityType)
    #print(thisTransaction.request_dict['entity']['type'])
    print(theEntity)

    if theEntity is None:
        #thisTransaction.build-general-error-output()
        print("there was no entity to call.  bailing")
        appendCommonParserNotice(thisTransaction,'NoEntityDefined')
    elif not 'services' in thisTransaction.request_dict['entity'].keys():
        """If no service is requested in the json object, do the default service."""
        print("could not find services in thisTransaction.request_dict['entity'].keys()")
        print("keys: " + str(thisTransaction.request_dict['entity'].keys))
        print("There were no services listed for the intity, doing the default.")
        #print("calling default")
        theEntity.receive.doDefaultService(thisTransaction)
    else:
        """This is where specific requested services are called."""
        #print("Calling receive for this entity: " + str(receive.entity))
        #print(theEntity.entity.receive)
        theEntity.receive.receive(thisTransaction)

    """
    Check to see if an outgoing string got built.  If not, try to
    build one.  If that still doesn't work, make the string be a
    generic error output JSON object.
    """
    if thisTransaction.outgoing_string is None:
        thisTransaction.build_outgoing_string()
    if thisTransaction.outgoing_string is None:
        ## TODO:  write this function....
        thisTransaction.build_general_error_output()

    # Return whatever outgoing string got made
    #print("about to return")
    return thisTransaction.outgoing_string

def doDefaultService(thisTransaction):
    """This might not be necessary... """
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='Delegator'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'payload':marco('Delegator')})
    thisTransaction.build_outgoing_string()

def receive(thisTransaction):
    print("Delegator received it")
    print("request_dict: " + str(thisTransaction.request_dict))

    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doDefaultService(thisTransaction)
    else:
        requestedServices = thisTransaction.request_dict['entity']['services']
        print("len(requestedServices): " + str(len(requestedServices)))
        for element in requestedServices:
            print("element.keys(): " + str(element.keys()))
            if 'listEntities' in element.keys():
                entities = listEntities("Delegator")
                print("entities: " + str(entities))
                if thisTransaction.response_dict is None:
                    thisTransaction.response_dict={}
                thisTransaction.response_dict['entity']={}
                thisTransaction.response_dict['entity']['type']='Delegator'
                thisTransaction.response_dict['responses'] = []
                thisTransaction.response_dict['responses'].append({'entities' : entities})
                thisTransaction.build_outgoing_string()




def main():
  import importlib.util, os, sys
  #from importlib import util
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
  utils.investigate_gems_setup(sys.argv)

  with open(sys.argv[1], 'r') as file:
    jsonObjectString = file.read().replace('\n', '')

  try:
    responseObjectString=delegate(jsonObjectString)
  except Exception as error:
    print("The delegator module captured an error.")
    print(str(error))
    ##TODO: see about exploring this error and returning more info. Temp solution for now.
    responseObject = {
        'DelegatorNotice' : {
            'type' : 'UnknownError',
            'notice' : {
                'code' : '500',
                'brief' : 'unknownError',
                'blockID' : 'unknown',
                'message' : 'Not sure what went wrong. Error captured by the Delegator gemsModule.'
            }
        }
    }
    responseObjectString = str(responseObject)


  print(responseObjectString)


if __name__ == "__main__":
  main()

