#!/usr/bin/env python3
import os, sys,importlib.util
import gemsModules
from gemsModules import common
from gemsModules.common.settings import *
from gemsModules.common.transaction import *
from gemsModules.common.utils import *
from gemsModules.common.loggingConfig import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema
from pydantic.schema import schema
import traceback

## TODO: Update this method to receive actual module name, not its key.
## Also update methods that call common/services.py importEntity() to reflect this change.

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.ERROR

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

verbosity=common.utils.gems_environment_verbosity()

def importEntity(requestedEntity):
    log.info("importEntity() was called.\n")
    log.debug("requestedEntity: " + requestedEntity)
    log.debug("Entities known to Common Services: " + str(subEntities))

    requestedModule = '.' + subEntities[requestedEntity]
    log.debug("requestedModule: " + requestedModule)

    module_spec = importlib.util.find_spec(requestedModule,package="gemsModules")
    if module_spec is None:
        log.error("The module spec returned None for rquestedEntity: " + requestedEntity)
        return None

    log.debug("module_spec: " + str(module_spec))
    return importlib.import_module(requestedModule,package="gemsModules")

def parseInput(thisTransaction):
    log.info("parseInput() was called.\n")
    import json
    from io import StringIO
    from pydantic import BaseModel, ValidationError
    import jsonpickle
    io=StringIO()

    # Load the JSON string into the incoming dictionary
    thisTransaction.request_dict = json.loads(thisTransaction.incoming_string)
    log.debug("thisTransaction.request_dict: " + str(thisTransaction.request_dict))

    # Check to see if there are errors.  If there are, bail, but give a reason
    #
    ## TODO:  This will break really easily.  The 'response' part needs to refer to the
    ## response from this activity rather than the zeroth response.  That said, at this
    ## point, the response will usually be the zeroth one.
    ## A construction maybe like:  if ('X','Y') in this.big.object.items():
    if thisTransaction.request_dict is None:
        appendCommonParserNotice(thisTransaction,'JsonParseError')
        return thisTransaction.response_dict['entity']['responses'][0]['notices']['code']
    try:
        TransactionSchema(**thisTransaction.request_dict)
    except ValidationError as e:
        # TODO : Add these to the error/verbosity thing
        log.error("Validation Error.")
        log.error(e.json())
        log.error(e.errors())
        log.error(traceback.format_exc())
        if 'entity' in e.errors()[0]['loc']:
            if 'type' in e.errors()[0]['loc']:
                log.error("Type present, but unrecognized.")
                log.error(thisTransaction.request_dict['entity']['type'])
                log.error(str(listEntities()))
                appendCommonParserNotice(thisTransaction,'EntityNotKnown')
            else:
                print("No 'type' present. Appending common parser notice.")
                appendCommonParserNotice(thisTransaction,'NoEntityDefined')

        theResponseTypes = getTypesFromList(thisTransaction.response_dict['entity']['responses'])
        log.debug(theResponseTypes)
        return theResponseTypes.count('error')
    except Exception as error:
        log.error("There was an error parsing transaction.request_dict.")
        log.error("Error type : " + str(type(error)))
        log.error(traceback.format_exc())

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
    return "Here there should be a location for the schema"  ## TODO:  make this do something real
  if not hasattr(theEntity, 'helpme'):
    return "No help available for " + requestedEntity
  helpLocation = getattr(theEntity, 'helpme')
  if not hasattr(helpLocation,theHelp):
    return "The requestedHelp is not available for " + requestedEntity
  thisHelp =  getattr(helpLocation, theHelp)
  if thisHelp is None:
    return "Something went wrong getting the requestedHelp from " + requestedEntity
  return thisHelp

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
    return GEMSHOME


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
