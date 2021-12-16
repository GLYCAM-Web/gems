#!/usr/bin/env python3
import json, math, os, sys,importlib.util, pprint
from datetime import datetime
import gemsModules
from gemsModules import common
from gemsModules.common.settings import *
from gemsModules.common.transaction import *
from gemsModules.common.utils import *
from gemsModules.common.loggingConfig import loggers, createLogger
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, ValidationError
from pydantic.schema import schema
import traceback

## TODO: Update this method to receive actual module name, not its key.
## Also update methods that call common/services.py importEntity() to reflect this change.

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

verbosity=common.utils.gems_environment_verbosity()

def prettyString( incomingDict: Dict ) :
    pp = pprint.PrettyPrinter(indent=2)
    return pp.pprint(incomingDict)

def directoryExists(directory : str) :
    log.info("directoryExists() was called.")
    log.debug("The directory to check : " + directory)
    if os.path.exists(directory):
        log.debug("Found the directory.")
        return True
    else:
        log.debug("Directory not found.")
        return False

##  Pass in the name of an entity, receive a module or an error.
def importEntity(requestedEntity):
    log.info("importEntity() was called.\n")
    log.debug("requestedEntity: " + requestedEntity)
    log.debug("Entities known to Common Services: " + str(subEntities))

    try:
        requestedModule = '.' + subEntities[requestedEntity]
        log.debug("requestedModule: " + requestedModule)
    except Exception as error:
        log.error("There was a problem finding the requested entity. Does it exist? requestedEntity: " + requestedEntity)
        raise error
    else:
        try:
            module_spec = importlib.util.find_spec(requestedModule,package="gemsModules")
        except Exception as error:
            log.error("There was a problem importing the requested module.")
            raise error
        else:

            if module_spec is None:
                log.error("The module spec returned None for rquestedEntity: " + requestedEntity)
                raise FileNotFoundError(requestedEntity)

            log.debug("module_spec: " + str(module_spec))
            return importlib.import_module(requestedModule,package="gemsModules")


def getEntityTypeFromJson(jsonObjectString):
    try:
        temp_dict=json.loads(jsonObjectString)
        thisEntityType = temp_dict['entity']['type']
        return thisEntityType
    except Exception as error:
        error_msg = "There was a problem finding the entity type.  Here is more info: " + str(error)
        log.error(error_msg)
        log.error(traceback.format_exc())
        return None


def getServicesFromJson(jsonObjectString):
    try:
        temp_dict=json.loads(jsonObjectString)
        theServicesObject = temp_dict['entity']['services']
        theServices=list(theServicesObject.keys())
        return theServices
    except Exception as error:
        error_msg = "There was a problem finding the services.  Here is more info: " + str(error)
        log.error(error_msg)
        log.error(traceback.format_exc())
        return None


def buildInvalidInputErrorResponseJsonString(
        thisMessagingEntity : str = 'commonServicer',
        message : str = 'No additional information available',
        prettyPrint : bool = False):
    responseSchema=common.io.TransactionSchema()
    responseSchema.generateCommonParserNotice(
        noticeBrief='InvalidInput',
        messagingEntity=thisMessagingEntity,
        additionalInfo={"errorMessage":message})
    if prettyPrint == True: 
        return responseSchema.json(indent=2)
    else:
        return responseSchema.json()


def parseInput(thisTransaction):
    log.info("parseInput() was called.\n")
    import json
    from io import StringIO
    from pydantic import BaseModel, ValidationError
    import jsonpickle
    io=StringIO()

    # Load the JSON string into the incoming dictionary
    thisTransaction.request_dict = json.loads(thisTransaction.incoming_string)
    log.debug("thisTransaction.request_dict: \n\n")
    prettyString(thisTransaction.request_dict)
    #prettyPrint(thisTransaction.request_dict)

    # Check to see if there are errors.  If there are, bail, but give a reason
    if thisTransaction.request_dict is None:
        thisTransaction.generateCommonParserNotice(noticeBrief = 'JsonParseError')
        raise AttributeError("request_dict")
    try:
        TransactionSchema(**thisTransaction.request_dict)
    except Exception as error:
        log.error("There was an error parsing transaction.request_dict.")
        log.error("Error type : " + str(type(error)))
        log.error(traceback.format_exc())
        raise error
    else:
        # If still here, load the data into a Transaction object and return success
        thisTransaction.transaction_in = jsonpickle.decode(thisTransaction.incoming_string)
        log.debug("thisTransaction.transaction_in: " + str(thisTransaction.transaction_in))
        return 0

def marco(requestedEntity):
    log.info("marco() was called.\n")
    if verbosity > 1 :
        print("The Marco method was called and is being fulfilled by CommonServices.")
    theEntity = importEntity(requestedEntity)
    if hasattr(theEntity, 'receive'):
        return "Polo"
    else:
        return "The entity you seek is not responding properly."

def getTypesFromList(theList):
    log.info("getTypesFromList() was called.\n")
    typesInList=[]
    for i in range(len(theList)):
        thekeys=list(theList[i].keys())
        thevalues=list(theList[i].values())
        for j in range(len(thevalues)):
            #print("Checking if there is a type")
            if not 'type' in thevalues[j].keys():
                #print("there is no type.  If there is a type, it might be")
                #print(thekeys[j])
                typesInList.append(thekeys[j])
            else:
                #print("there is a type and it is:")
                #print(thevalues[j]['type'])
                typesInList.append(thevalues[j]['type'])
    #print("printing the typesInList:")
    #print(typesInList)
    return typesInList


## TODO make this more generic
def listEntities(requestedEntity='Delegator'):
  log.info("listEntities() was called.\n")
  return list(subEntities.keys())

def returnHelp(requestedEntity,requestedHelp):
  log.info("returnHelp() was called.\n")
  theEntity = importEntity(requestedEntity)
  theHelp = entities.helpDict[requestedHelp]
  if theHelp == 'schemaLocation':
    schema_location = settings.getSchemaLocation()
    return schema_location  ## TODO:  make this do something real
  if not hasattr(theEntity, 'helpme'):
    return "No help available for " + requestedEntity
  helpLocation = getattr(theEntity, 'helpme')
  if not hasattr(helpLocation,theHelp):
    return "The requestedHelp is not available for " + requestedEntity
  thisHelp =  getattr(helpLocation, theHelp)
  if thisHelp is None:
    return "Something went wrong getting the requestedHelp from " + requestedEntity
  return thisHelp

##  Looks at currentStableSchema file and returns the version it finds there.
def getCurrentStableJsonApiVersion():
    log.info("getCurrentStableJsonApiVersion() was called.\n")
    currentStableSchema = getGemsHome() + "/gemsModules/Schema/currentStableSchema"
    try:
        with open(currentStableSchema) as schemaFile:
            version = schemaFile.read().strip()
        log.debug("json_api_version: " + version)
    except Exception as error:
        log.error("Failed to read the currentStableSchema file.")
        raise error
    else:
        return version

##  Looks for an environment var with GEMSHOME and returns it.
def getGemsHome():
    log.info("getGemsHome() was called.\n")
    GEMSHOME = os.environ.get('GEMSHOME')
    if GEMSHOME == None:
        log.error("""

        GEMSHOME environment variable is not set.

        Set it using somthing like:

          BASH:  export GEMSHOME=/path/to/gems
          SH:    setenv GEMSHOME /path/to/gems
        """)
        raise AttributeError("GEMSHOME")
    return GEMSHOME

##  Give a transaction, return its requested entity type
#   @param  transaction
def getEntityType(thisTransaction):
    log.info("getEntityType() was called.\n")
    entity = thisTransaction.request_dict['entity']['type']
    log.debug("entity: " + entity)
    return entity

##  Send a transaction and a response. This method checks the response validity and
#   updates the transaction with a response for you, though they may be errors.
#   @param transaction
#   @param responseConfig
def appendResponse(thisTransaction, responseConfig):
    log.info("appendResponse() was called.\n")
    ## Check the responseConfig:
    if 'entity' in responseConfig.keys():
        entity = responseConfig['entity']
        log.debug("entity: " + entity)
    else:
        log.error("Please add the entity type to your responseConfig object.")
        thisTransaction.generateCommonParserNotice(noticeBrief =  'IncompleteResponseError')

    if 'respondingService' in responseConfig.keys():
        respondingService = responseConfig['respondingService']
        log.debug("respondingService: " + respondingService)
    else:
        log.error("Please add a respondingService field to your responseConfig object.")
        thisTransaction.generateCommonParserNotice(noticeBrief = 'IncompleteResponseError')

    if 'responses' in responseConfig.keys():
        responsesToWrite = responseConfig['responses']
        if entity is not None and respondingService is not None and responsesToWrite is not None:
            if thisTransaction.response_dict == None:
                thisTransaction.response_dict = {}

            if 'entity' not in thisTransaction.response_dict.keys():
                thisTransaction.response_dict['entity'] = {}
                thisTransaction.response_dict['entity']['type'] = entity

            if 'timestamp' not in thisTransaction.response_dict.keys():
                timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                log.debug("timestamp: " + timestamp)
                thisTransaction.response_dict['timestamp'] = timestamp

            if 'responses' not in thisTransaction.response_dict['entity'].keys():
                thisTransaction.response_dict['entity']['responses'] = []

            for response in responsesToWrite:
                resource = {respondingService : response }
                log.debug("Adding a resource to the response: " + str(resource))
                thisTransaction.response_dict['entity']['responses'].append(resource)
            # if 'echoed_response' not in thisTransaction.response_dict.keys():
            #     thisTransaction.response_dict['echoed_response'] = {}

            # if 'payload' not in thisTransaction.response_dict['echoed_response']:
            #     thisTransaction.response_dict['echoed_response']['payload'] = {}

            # thisTransaction.response_dict['echoed_response']['payload'] = "echoed payload goes here"

            try:
                TransactionSchema(**thisTransaction.response_dict)
                log.debug("Passes validation against schema.")
            except ValidationError as e:
                log.error("Validation Error: " + str(e))
                thisTransaction.generateCommonParserNotice(noticeBrief = 'JsonParseEror')
        else:
            log.Error("Incomplete responseConfig.")
            thisTransaction.generateCommonParserNotice(noticeBrief = 'IncompleteResponseError')
    else:
        log.error("Please add at a list of responses to your responseConfig object.")
        thisTransaction.generateCommonParserNotice(noticeBrief = 'IncompleteResponseError')


##  @brief Convenience method for cleaning and speeding up log reading of dict objects.
#   @detail Useful for assessing json objects.
def prettyPrint(myObj):

    preparedObj = {}
    for field in myObj.keys():
        if type(field != str):
            ## recursively convert object and all children to strings.
            preparedObj[field] = processFieldForPrettyPrinting(myObj[field])
        else:
            preparedObj[field] = myObj[field]

    log.debug("\n" + json.dumps(preparedObj, indent=4, sort_keys=False))


##  @brief Recursively convert object and all children to strings. 
#   @detail Only intended for use with the prettyPrint method.
#   @param field of unknown type
#   @param field of type string
def processFieldForPrettyPrinting(field):
    #log.info("processFieldForPrettyPrinting() was called.")
 
    #log.debug("fieldType: " + str(type(field)))
    #log.debug(repr(field))
    if type(field) != str:
        if type(field) == list:
            #log.debug("processing a list.")
            newList = []
            for subField in field:
                newList.append(processFieldForPrettyPrinting(subField))
            return newList
        elif type(field) == dict:
            #log.debug("processing a dict.\n" + repr(field))
            newDict = {}
            try:
                #log.debug("keys: " + str(field.keys()))
                for key in field.keys():
                    #log.debug("key: " + key)
                    newDict.update({
                        key : processFieldForPrettyPrinting(field[key])
                    }) 
                return newDict
            except Exception as error:
                log.error("There was an error processing this dict: " + str(error))
                log.error(repr(field))
        else:
            ## Convert non-strings to string.
            #log.debug("converting field to string then returning it.")
            return str(field)
    else:
        #log.debug("This field is already a string. Returning it.")
        return field



##  Logic borrowed from https://realpython.com/python-rounding/
#   @param number
#   @param decimals
def roundHalfUp(number, decimals=0):
    log.info("roundHalfUp() was called.\n ")
    log.debug("number before rounding: " + str(number))
    multiplier = 10 ** decimals
    roundedNumber = math.floor(number * multiplier + 0.5) / multiplier
    log.debug("roundedNumber: " + str(roundedNumber))
    return roundedNumber

def main():
    import importlib, os, sys
    from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
    from pydantic import BaseModel, Schema
    from pydantic.schema import schema
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
#  utils.investigate_gems_setup(sys.argv)
#
#  with open(sys.argv[1], 'r') as file:
#    data = file.read().replace('\n', '')
    # Make a new Transaction object for holding I/O information.
    data=utils.JSON_From_Command_Line(sys.argv)
    print("The object is:")
    print(data)
    thisTransaction=Transaction(data)
    parseInput(thisTransaction)
    print("finished parsing")



if __name__ == "__main__":
  main()
