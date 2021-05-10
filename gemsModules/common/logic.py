#!/usr/bin/env python3
import json, math, os, sys,importlib.util
from datetime import datetime
import gemsModules
from gemsModules.common.settings import *
from gemsModules.common.io import *
from gemsModules.common.loggingConfig import *
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


##  Pass in the name of an entity, receive a module or an error.
def importEntity(requestedEntity):
    log.info("importEntity() was called.\n")
    log.debug("requestedEntity: " + requestedEntity)
    #log.debug("Entities known to Common Services: " + str(subEntities))

    try:
        requestedModule = '.' + subEntities[requestedEntity]
        log.debug("requestedModule: " + requestedModule)
    except Exception as error:
        log.error("There was a problem finding the requested entity. Does it exist? requestedEntity: " + requestedEntity)
        log.error(traceback.format_exc())
        raise error
    else:
        try:
            module_spec = importlib.util.find_spec(requestedModule,package="gemsModules")
        except Exception as error:
            log.error("There was a problem importing the requested module.")
            log.error(traceback.format_exc())
            raise error
        else:

            if module_spec is None:
                log.error("The module spec returned None for rquestedEntity: " + requestedEntity)
                raise FileNotFoundError(requestedEntity)

            #log.debug("module_spec: " + str(module_spec))
            return importlib.import_module(requestedModule,package="gemsModules")

# ###  This now is part of the Transaction Class
# ###  It is deprecated and should go away.   Lachele 2021-04-02
def parseInput(thisTransaction):
    log.info("common.logic.parseInput() was called.\n")
    import json
    from io import StringIO
    from pydantic import BaseModel, ValidationError
    import jsonpickle
    io=StringIO()

    # Load the JSON string into the incoming dictionary
    thisTransaction.request_dict = json.loads(thisTransaction.incoming_string)
    #log.debug("thisTransaction.request_dict: \n\n")
    #prettyPrint(thisTransaction.request_dict)

    # Check to see if there are errors.  If there are, bail, but give a reason
    if thisTransaction.request_dict is None:
        thisTransaction.generateCommonParserNotice(noticeBrief = 'JsonParseError')
        log.error(traceback.format_exc())
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
        #log.debug("thisTransaction.transaction_in: " + str(thisTransaction.transaction_in))
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
        log.error(traceback.format_exc())
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

        Set it using something like:

          BASH:  export GEMSHOME=/path/to/gems
          SH:    setenv GEMSHOME /path/to/gems
        """)

        raise AttributeError("GEMSHOME")
    return GEMSHOME


def make_relative_symbolic_link(
        path_down_to_source : str, 
        path_down_to_dest_dir : str , 
        dest_link_label : str, 
        parent_directory : str
        ):
    #  path_down_to_source      Path, relative to parent_directory, to the source of the link
    #  path_down_to_dest_dir    Path, relative to parent_directory, where the link will be placed
    #                           If None, it will be the current working directory
    #  dest_link_label          The lable to place in path_down_to_dest.
    #                           That is, the sym link will be path_down_to_dest/dest_link_label
    #                           If None - then the last part of the path_down_to_source will be used.
    #                           That is, if path_down_to_source is path/down/to/source, then 
    #                           the sym link will be path_down_to_dest/source
    #  parent_directory         The parent where the two paths down exist.
    #                           If None, it will use the current working directory
    #                           Unless you know you are in a shell, you probably want to set this
    log.info("common.logic.make_relative_symbolic_link() was called")
    log.debug("path_down_to_source: " + path_down_to_source)
    log.debug("path_down_to_dest_dir: " + str(path_down_to_dest_dir))
    log.debug("dest_link_label: " + dest_link_label)
    log.debug("parent_directory: " + parent_directory)

    if parent_directory is not None:
        owd=os.getcwd()
        os.chdir(parent_directory)
        log.debug("The original working directory was : " + owd)
        log.debug("The current working directory is : " + os.getcwd())
    if not os.path.exists(path_down_to_source):
        log.debug("Link source does not exist: " + path_down_to_source)
        log.debug("Allowing anyway.") # Oliver: Seems odd that this would work.
        #raise AttributeError(path_down_to_source)
    if path_down_to_dest_dir is None:
        if dest_link_label is None: 
            path_down_to_dest_label=os.path.basename(path_down_to_source)
        else:
            path_down_to_dest_label=dest_link_label
    else:
        if not os.path.isdir(path_down_to_dest_dir): 
            log.error("The path down to the link to be created is not a directory : " + path_down_to_dest_dir)
            raise AttributeError(path_down_to_dest_dir)
        if dest_link_label is None: 
            path_down_to_dest_label=os.path.join(path_down_to_dest_dir, os.path.basename(path_down_to_source))
        else:
            path_down_to_dest_label=os.path.join(path_down_to_dest_dir, dest_link_label)
    if path_down_to_source == path_down_to_dest_label:
        log.error("Symbolic link source and destination cannot be the same thing : " + path_down_to_dest_label)
        raise AttributeError("Source and destination for symbolic linking are the same: " + path_down_to_dest_label)
    relative_path_to_source =  os.path.relpath(
        path_down_to_source,
        path_down_to_dest_dir
        )
    log.debug("About to link this source : " + relative_path_to_source)
    log.debug(".... to this destination : " + path_down_to_dest_label)
    if os.path.islink(dest_link_label): # Oliver addition to allow overwrites
        os.remove(dest_link_label)
    try:
        os.symlink(relative_path_to_source, path_down_to_dest_label)
    except Exception as error:
        log.debug("Simlink already exists. No need to create a new one. Here is the error, just in case: " + str(error))

    if parent_directory is not None:
        os.chdir(owd)


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
    log.info("common_logic appendResponse() was called.\n")
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
                log.error(traceback.format_exc())
                thisTransaction.generateCommonParserNotice(noticeBrief = 'JsonParseEror')
        else:
            log.Error("Incomplete responseConfig.")
            thisTransaction.generateCommonParserNotice(noticeBrief = 'IncompleteResponseError')
    else:
        log.error("Please add at a list of responses to your responseConfig object.")
        thisTransaction.generateCommonParserNotice(noticeBrief = 'IncompleteResponseError')



##  @brief Handles the construction of the response_dict portion of a transaction. 
##  @details This creates the response bits that are common to all responses.
##           Send one response at a time. Create the response using Pydantic-enabled classes in 
##           your gemsModule's io.py.
def updateResponse(thisTransaction, serviceResponse):
    log.info("common.logic updateResponse() was called.\n")
    log.debug("type of serviceResponse obj: " + str(type(serviceResponse)))
    log.debug("serviceResponse.keys: " + str(serviceResponse.keys()))

    if thisTransaction.response_dict == None:
        log.debug("No response_dict yet. Creating it now.")
        thisTransaction.response_dict = {}
    else:
        log.debug("Response dict already exists")

    ## Remember this could be called several times. Don't overwrite existing responses.
    # Entity contains type, services, inputs, and responses.
    # Type already validated if we reach this point. Copy over from request.
    if 'entity' not in thisTransaction.response_dict.keys():
        log.debug("No entity in the response yet. Creating it now.")
        thisTransaction.response_dict['entity'] = {}
        try:
            requestedEntity = thisTransaction.request_dict['entity']['type']
        except Exception as error:
            log.error("There was no entity type to be found in the transaction's request_dict.")
            log.error(traceback.format_exc())
            thisTransaction.generateCommonParserNotice(noticeBrief = 'InvalidInput') 
        else:
            thisTransaction.response_dict['entity']['type'] = requestedEntity
    else:
        log.debug("Entity already exists.")

    ## services already validated if we reach this point. Copy over from request.
    if 'services' not in thisTransaction.response_dict['entity'].keys():
        thisTransaction.response_dict['entity']['services'] = []
    else:
        log.debug("Services object already exists.")

    log.debug("serviceResponse['type']: " + serviceResponse['type'])

    try:
        serviceType = serviceResponse['type']
        responseServices = thisTransaction.response_dict['entity']['services']
        serviceListed = False
        log.debug("responseServices: " + repr(responseServices))
        #[{'Evaluate': {'type': 'Evaluate'}}, {'Build3DStructure': {'type': 'Build3DStructure'}}]
        for service in responseServices:
            log.debug("service keys: " + str(service.keys()))
            if serviceType in service.keys():
                serviceListed = True
        if serviceListed == False:
            requestedService = { 
                serviceType  :  {
                    "type" : serviceType
                }
            }
            log.debug("Adding service to json response object services list: " + str(requestedService))
            thisTransaction.response_dict['entity']['services'].append(requestedService)
        else:
            log.debug("Service already listed. Skipping.")

    except Exception as error:
        log.error("There was a problem adding the requested service: " + str(error))
        log.error(traceback.format_exc())


    ## inputs already validated if we reach this point. Copy over from request.
    if 'inputs' not in thisTransaction.response_dict['entity'].keys():
        thisTransaction.response_dict['entity']['inputs'] = []
        try:
            requestInputs = thisTransaction.request_dict['entity']['inputs']
            thisTransaction.response_dict['entity']['inputs']  = requestInputs
        except Exception as error:
            log.error("No inputs found in request.")
            log.error(traceback.format_exc())
            thisTransaction.generateCommonParserNotice(noticeBrief = 'InvalidInput')


    log.debug("responding entity: " + thisTransaction.response_dict['entity']['type'])

    ## Timestamp for the creation of this response. Overwrites if multiple responses
    ##  are added. Represents the time of the addition of the final response.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log.debug("response_timestamp: " + timestamp)
    thisTransaction.response_dict['response_timestamp'] = timestamp


    ####################################################################

    if 'responses' not in thisTransaction.response_dict['entity'].keys():
        thisTransaction.response_dict['entity']['responses'] = []

    thisTransaction.response_dict['entity']['responses'].append(serviceResponse)

    try:
        log.debug("response_dict obj type: " + str(type(thisTransaction.response_dict)))
        log.debug("Response_dict before validation: ")

        ##Breaking here. 
        prettyPrint(thisTransaction.response_dict)

        TransactionSchema(**thisTransaction.response_dict)

        log.debug("Passes validation against schema.")
    except ValidationError as e:
        log.error("Validation Error while responding to: " + requestedEntity + e.json())
        log.error(traceback.format_exc())
        thisTransaction.generateCommonParserNotice(noticeBrief = 'JsonParseEror')

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
