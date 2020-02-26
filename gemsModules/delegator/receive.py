#!/usr/bin/env python3
import gemsModules
from datetime import datetime
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
import traceback

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.ERROR

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

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
    log.info("delegate() was called.\n")
    log.debug("incoming jsonObjectString: " + jsonObjectString)

    # Make a new Transaction object for holding I/O information.
    thisTransaction=Transaction(jsonObjectString)

    # If the incoming string was improperly formed, bail, but give a reason.
    if parseInput(thisTransaction) != 0:
        log.error(" There was an error parsing the input!")
        thisTransaction.build_outgoing_string()
        return thisTransaction.outgoing_string

    # Grab the entity type
    entityType = thisTransaction.request_dict['entity']['type']
    log.debug("Requested entityType: " + entityType)
    # If the entity type is CommonServies, then something was very wrong,
    # and the JSON object is coming from internal errors.  So, just return it.
    if entityType == 'CommonServices':
        log.error("The requested entity is CommonServices, so something must have gone wrong.")
        log.error("I'm returning that oject. as-is.  Delegator cannot delegate to CommonServices.")
        return jsonObjectString
    # See if it is possible to load a module for the requested Entity
    theEntity = importEntity(entityType)
    log.debug("theEntity: " + str(theEntity))

    if theEntity is None:
        log.error("there was no entity to call.  bailing")
        appendCommonParserNotice(thisTransaction,'NoEntityDefined')
    elif not 'services' in thisTransaction.request_dict['entity'].keys():
        ## If no service is requested in the json object, do the default service.
        log.debug("No service defined in the request. Calling the default service")
        theEntity.receive.doDefaultService(thisTransaction)
    else:
        ## This is where specific requested services are called.
        theEntity.receive.receive(thisTransaction)

    ##Set the json_api_version in the response_dict.
    if 'json_api_version' not in thisTransaction.response_dict.keys():
        thisTransaction.response_dict['json_api_version'] = getJsonApiVersion()
    if 'response_timestamp' not in thisTransaction.response_dict.keys():
        thisTransaction.response_dict['response_timestamp'] = str(datetime.now())
    if 'site_host_name' not in thisTransaction.response_dict.keys():
        if 'site_host_name' in thisTransaction.request_dict.keys():
            thisTransaction.response_dict['site_host_name'] = thisTransaction.request_dict['site_host_name']


    ## Check to see if an outgoing string got built.  If not, try to
    ## build one.  If that still doesn't work, make the string be a
    ## generic error output JSON object.
    log.debug("Most of the work is finished now.  About to build the response, if not already built.")
    log.debug("The resquest dict is:  \n" + str(thisTransaction.request_dict) + "\n")
    log.debug("The response dict is:  \n" + str(thisTransaction.response_dict) + "\n")
    if thisTransaction.outgoing_string is None:
        log.debug("An outgoing string does not already exist.  About to build one.")
        thisTransaction.build_outgoing_string()
    if thisTransaction.outgoing_string is None:
        ## TODO:  write this function....
        log.debug("An outgoing string STILL does not exist.  About to build an error response.")
        thisTransaction.build_general_error_output()



    # Return whatever outgoing string got made
    log.debug("About to return whatever output I have at this point.")
    return thisTransaction.outgoing_string

def doDefaultService(thisTransaction):
    """This might not be necessary... """
    log.info("Calling the default service for the Delegator.\n")
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='Delegator'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'payload':marco('Delegator')})
    thisTransaction.build_outgoing_string()

## TODO:  this reception code does not conform to the current JSON schema (is close...).
def receive(thisTransaction):
    log.info("receive() was called.\n")
    log.debug("request_dict: " + str(thisTransaction.request_dict))

    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doDefaultService(thisTransaction)
    else:
        requestedServices = thisTransaction.request_dict['entity']['services']
        log.debug("len(requestedServices): " + str(len(requestedServices)))
        for element in requestedServices:
            log.debug("element.keys(): " + str(element.keys()))
            if 'listEntities' in element.keys():
                entities = listEntities("Delegator")
                log.debug("entities: " + str(entities))
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

