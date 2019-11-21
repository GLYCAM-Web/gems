#!/usr/bin/env python3
import gemsModules
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
import traceback

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
    
    if verbosity > 0 :
        print("~~~\nDelegator receive.py delegate() was called.\n~~~")
    if verbosity > 1 :
        print("incoming jsonObjectString: \n" + jsonObjectString)

    # Make a new Transaction object for holding I/O information.
    thisTransaction=Transaction(jsonObjectString)

    # If the incoming string was improperly formed, bail, but give a reason.
    if parseInput(thisTransaction) != 0:
        if verbosity > -1 :
            print(" There was an error parsing the input!")
        thisTransaction.build_outgoing_string()
        return thisTransaction.outgoing_string
    
    # Grab the entity type
    entityType = thisTransaction.request_dict['entity']['type']
    if verbosity > 0 :
        print("Requested entityType: " + entityType)
    # If the entity type is CommonServies, then something was very wrong,
    # and the JSON object is coming from internal errors.  So, just return it.
    if entityType == 'CommonServices':
        if verbosity > -1 :
            print("The requested entity is CommonServices, so something must have gone wrong.")
            print("I'm returning that oject. as-is.  Delegator cannot delegate to CommonServices.")
        return jsonObjectString
    # See if it is possible to load a module for the requested Entity
    theEntity = importEntity(entityType)
    #print(thisTransaction.request_dict['entity']['type'])
    #print("theEntity: " + str(theEntity))

    if theEntity is None:
        if verbosity > -1 :
            print("there was no entity to call.  bailing")
        appendCommonParserNotice(thisTransaction,'NoEntityDefined')
    elif not 'services' in thisTransaction.request_dict['entity'].keys():
        ## If no service is requested in the json object, do the default service.
        if verbosity > 0 :
            print("Calling the default service")
        if verbosity > 1 :
            print("could not find services in thisTransaction.request_dict['entity'].keys()")
            print("keys: " + str(thisTransaction.request_dict['entity'].keys))
        theEntity.receive.doDefaultService(thisTransaction)
    else:
        ## This is where specific requested services are called.
        theEntity.receive.receive(thisTransaction)

    ## Check to see if an outgoing string got built.  If not, try to
    ## build one.  If that still doesn't work, make the string be a
    ## generic error output JSON object.
    if thisTransaction.outgoing_string is None:
        thisTransaction.build_outgoing_string()
    if thisTransaction.outgoing_string is None:
        ## TODO:  write this function....
        thisTransaction.build_general_error_output()

    # Return whatever outgoing string got made
    if verbosity > 0 :
        print("About to return whatever output I have at this point.")
    return thisTransaction.outgoing_string

def doDefaultService(thisTransaction):
    """This might not be necessary... """
    if verbosity > 0 :
        print("Calling the default service for the Delegator itself.")
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='Delegator'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'payload':marco('Delegator')})
    thisTransaction.build_outgoing_string()

## TODO:  this reception code does not conform to the current JSON schema (is close...).
def receive(thisTransaction):
    if verbosity > 0 :
        print("Delegator received a transaction.")
    if verbosity > 1 :
        print("request_dict: " + str(thisTransaction.request_dict))

    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doDefaultService(thisTransaction)
    else:
        requestedServices = thisTransaction.request_dict['entity']['services']
        if verbosity > 0 :
            print("len(requestedServices): " + str(len(requestedServices)))
        for element in requestedServices:
            if verbosity > 1 :
                print("element.keys(): " + str(element.keys()))
            if 'listEntities' in element.keys():
                entities = listEntities("Delegator")
                if verbosity > 1 :
                    print("entities: " + str(entities))
                if thisTransaction.response_dict is None:
                    thisTransaction.response_dict={}
                thisTransaction.response_dict['entity']={}
                thisTransaction.response_dict['entity']['type']='Delegator'
                thisTransaction.response_dict['responses'] = []
                thisTransaction.response_dict['responses'].append({'entities' : entities})
                thisTransaction.build_outgoing_string()
            if 'testSegfault' in element.keys():
#                print("About to segfault, I hope.")
                from . import isegfault
                return

def main():
  import importlib.util, os, sys
  #from importlib import util
  if importlib.util.find_spec("gemsModules") is None:
    this_dir, this_filename = os.path.split(__file__)
    sys.path.append(this_dir + "/../")
    if importlib.util.find_spec("common") is None:
      print("I cannot find the Common Servicer.  No clue what to do. Exiting")
      sys.exit(1)
    else:
      from common import utils
  else:
    from gemsModules.common import utils
  jsonObjectString=utils.JSON_From_Command_Line(sys.argv)
  try:
    responseObjectString=delegate(jsonObjectString)
  except Exception as error:
    print("\nThe delegator module captured an error.")
    print("Error type: " + str(type(error)))
    print(traceback.format_exc())
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


  print("\ndelegator is returning this: \n" +  responseObjectString)


if __name__ == "__main__":
  main()

