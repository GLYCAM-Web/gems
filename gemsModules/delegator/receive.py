#!/usr/bin/env python3

#import gemsModules
import gemsModules.deprecating_20221212

from datetime import datetime

#from gemsModules import common
from gemsModules.deprecating_20221212 import common

#from gemsModules.common.services import *
from gemsModules.deprecating_20221212.common.services import *

#from gemsModules.common.transaction import * # might need whole file...
from gemsModules.deprecating_20221212.common.transaction import * # might need whole file...

#from gemsModules.common.loggingConfig import *

import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

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

    #from gemsModules.common.io import Transaction as ioTransaction

    from gemsModules.deprecating_20221212.common.io import Transaction as ioTransaction
    thisTransaction=ioTransaction(jsonObjectString)

#    # If the incoming string was improperly formed, bail, but give a reason.
#    ##TODO: Look at this more closely. Predates current error handling approach.
#    from gemsModules.common.logic import parseInput as logic_parseInput
#    if logic_parseInput(thisTransaction) != 0:
#        log.error(" There was an error parsing the input!")
#        thisTransaction.build_outgoing_string()
#        return thisTransaction.outgoing_string

    # Grab the entity type
    entityType = thisTransaction.request_dict['entity']['type']
    log.debug("Requested entityType: " + entityType)
    # If the entity type is CommonServies, then something was very wrong,
    # and the JSON object is coming from internal errors.  So, just return it.
    if entityType == 'CommonServices':
        log.error("The requested entity is CommonServices, so something must have gone wrong.")
        log.error("I'm returning that oject. as-is.  Delegator cannot delegate to CommonServices.")
        return jsonObjectString

    ### See if it is possible to load a module for the requested Entity
    try:
        #from gemsModules.common.logic import importEntity as logic_importEntity
        from gemsModules.deprecating_20221212.common.logic import importEntity as logic_importEntity
        theEntity = logic_importEntity(entityType)
        #log.debug("theEntity: " + str(theEntity))
    except Exception as error:
        error_msg = "There was a problem importing the entity: " + str(error)
        log.error(error_msg)
        log.error(traceback.format_exc())
        thisTransaction.generateCommonParserNotice(messagingEntity='delegator', additionalInfo={"errorMessage":error_msg})
    
    ##Figure out what service to do.
    if theEntity is None:
        log.error("there was no entity to call.  bailing")
        thisTransaction.generateCommonParserNotice(noticeBrief='NoEntityDefined')
    elif not 'services' in thisTransaction.request_dict['entity'].keys():
        ## If no service is requested in the json object, do the default service.
        ## This logic could possibly move down to the Entity level.  Is ok here. (Lachele)
        log.debug("No service defined in the request. Calling the default service")
        returnedTransaction = theEntity.receive.doDefaultService(thisTransaction)
        if returnedTransaction is not None :
            # ## !!!!! This might not work as planned....
            thisTransaction = returnedTransaction
    
    try:
        ## This is where specific requested services are called.
        returnedTransaction = theEntity.receive.receive(thisTransaction)
        if returnedTransaction is not None :
            # ## !!!!! This might not work as planned....
            thisTransaction = returnedTransaction
    except Exception as error:
        error_msg = str(error)
        log.error("There was a problem providing the requested service: " + str(error))
        log.error(traceback.format_exc())
        thisTransaction.generateCommonParserNotice(messagingEntity='delegator', additionalInfo={"errorMessage":error_msg})
    
    ##Set the json_api_version in the response_dict.
    try:
        setResponseApiVersion(thisTransaction)
    except Exception as error:
        error_msg  = "There was a problem setting the response JSON API version: " + str(error)
        log.error(error_msg)
        log.error(traceback.format_exc())
        thisTransaction.generateCommonParserNotice(messagingEntity='delegator', additionalInfo={"errorMessage":error_msg})
    
    ##Set the response timestamp.
    setResponseTimestamp(thisTransaction)
    
    ## Set the response site host.
    setResponseSiteHost(thisTransaction)

    ## Build outgoing string or error.
    log.debug("The resquest dict is:  \n" + str(thisTransaction.request_dict) + "\n")
    log.debug("The response dict is:  \n" + str(thisTransaction.response_dict) + "\n")

    if thisTransaction.outgoing_string is None:
        log.debug("An outgoing string does not already exist.  About to build one.")
        try:
            thisTransaction.build_outgoing_string()
        except Exception as error:
            error_msg = "There was a problem building the outgoing string: " + str(error)
            log.error(error_msg)
            log.error("Error type: " + str(type(error)))
            thisTransaction.generateCommonParserNotice(messagingEntity='delegator', additionalInfo={"errorMessage":error_msg})

    # Return whatever outgoing string was made
    log.debug("About to return whatever output I have at this point:")
    log.debug(prettyPrint(thisTransaction.response_dict))

    log.debug("thisTransaction.outgoing_string obj type: " + str(type(thisTransaction.outgoing_string)))
    log.debug("thisTransaction.outgoing_string: " + thisTransaction.outgoing_string)
    
    return thisTransaction.outgoing_string

def setResponseSiteHost(thisTransaction):
    log.info("setResponseSiteHost() was called.\n")
    if 'site_host_name' not in thisTransaction.response_dict.keys():
        if 'site_host_name' in thisTransaction.request_dict.keys():
            thisTransaction.response_dict['site_host_name'] = thisTransaction.request_dict['site_host_name']

def setResponseTimestamp(thisTransaction):
    log.info("setResponseTimestamp() was called.\n")
    if 'response_timestamp' not in thisTransaction.response_dict.keys():
        thisTransaction.response_dict['response_timestamp'] = str(datetime.now())


def setResponseApiVersion(thisTransaction):
    log.info("setResponseApiVersion() was called.\n")
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}
    if 'json_api_version' not in thisTransaction.response_dict.keys():
        try:
            thisTransaction.response_dict['json_api_version'] = getCurrentStableJsonApiVersion()
        except Exception as error:
            log.error("There was a problem getting the current stable json api version.")
            raise error
    

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
    log.info("delegator.receive() was called.\n")
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
            if 'returnSchema' in element.keys():
                log.debug("returnSchema was requested.")
                schema =  getJsonSchema()
                responseConfig = {
                    "entity" : "Delegator",
                    "respondingService" : "returnSchema",
                    "responses" : [
                        { "payload" : schema}
                    ]
                }

                appendResponse(thisTransaction, responseConfig)

##  Return the content of the current schema, as defined in CurrentStableSchema
def getJsonSchema():
    log.info("getJsonSchema() was called.\n")
    versionFilename = getGemsHome() + "/gemsModules/deprecating_20221212/Schema/currentStableSchema"
    with open(versionFilename, 'r') as versionFile:
        currentStableVersion = versionFile.read().strip()
    schemaFileName = getGemsHome() + "/gemsModules/deprecating_20221212/Schema/" + currentStableVersion + "/schema.json"
    with open(schemaFileName, 'r') as schemaFile:
        content = schemaFile.read()
    #log.debug("schema content: \n" + content )
    return content

def main():
  import importlib.util, os, sys
  #from importlib import util
  if importlib.util.find_spec("gemsModules/deprecating_20221212") is None:
    this_dir, this_filename = os.path.split(__file__)
    sys.path.append(this_dir + "/../")
    if importlib.util.find_spec("common") is None:
      print("I cannot find the Common Servicer.  No clue what to do. Exiting")
      sys.exit(1)
    else:
      #from common import utils
      from deprecating_20221212.common import utils
      
  else:
    #from gemsModules.common import utils
    from gemsModules.deprecating_20221212.common import utils
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

