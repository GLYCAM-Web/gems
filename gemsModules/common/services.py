#!/usr/bin/env python3
import sys,importlib.util
import gemsModules
from gemsModules.common import entities

commonServicesExitCodes = {
        'NoEntityDefined':'301',
        'EntityNotKnown':'302',
        'NoTypeForEntity':'303',
        'RequestedEntityNotFindable':'310'
        }

## Other entities will need this, too.
def importEntity(requestedEntity):
  import gemsModules
  requestedModule="."+entities.entityFunction[requestedEntity]
  module_spec = importlib.util.find_spec(requestedModule,package="gemsModules")
  if module_spec is None: 
    print("The module spec returned None for rquestedEntity: " + requestedEntity)
    return None
  return importlib.import_module(requestedModule,package="gemsModules")

## Make this create/return the json dict and a response dict.
## Change name to JSON parser or something more appropriate
def parseinput(Transaction thisTransaction):
    import json
    from io import StringIO
    io=StringIO()
    # Load the JSON string into the incoming dictionary
    thisTransaction.request_dict = json.loads(thisTransaction.incoming_string)
    # Set a flag that there are no errors
    isError = False
    # Check to see if there are errors
    if not 'entity' in jsonDict:
        payload= "The JSON object does not contain an Entity."
        exitError = 'NoEntityDefined'
        isError = True
    if not 'type' in jsonDict['entity']:
        payload="The Entity does not contain a type."
        exitError= 'NoTypeForEntity'
        isError = True
    if not jsonDict['entity']['type'] in entities.entityFunction:
        payload="The entity in this JSON Onject is not known to the commonServicer."
        exitError = 'EntityNotKnown'
        isError = True
    if isError :
        responseObject['entity']['type']='commonServicer'
        return exitCode
    return 0


def doServices():
    ## TODO figure out how to impose options on things....
    responseObject['entity']=jsonDict['entity']
    responseObject['responses']=[]
    for i in jsonDict['services']:
        #print("The service is:  " + i['type'])
        ## TODO make the reply object build work better
        if i['type'] in entities.helpDict:
            payload=commonServices[i['type']]((jsonDict['entity']['type']),i['type'])
        else:
            payload=commonServices[i['type']](jsonDict['entity']['type'])
        #print("payload is :  ")
        #print(payload)
        responseObject['responses'].append({
            'type':i['type'],
            'payload':payload
            })
    #print(json.dumps(responseObject))
    return responseObject

def marco(requestedEntity):
  theEntity = importEntity(requestedEntity)
  if hasattr(theEntity, 'entity'):
    return "Polo"
  else:
    return "The entity you seek is not responding properly."

def listEntities(requestedEntity='Delegator'):
  return list(entities.entityFunction.keys())

def returnHelp(requestedEntity,requestedHelp):
  ## have something figure out the help that's wanted...
  ## print("The requestedHelp is >>>" +requestedHelp + "<<< and the entity is >>>" + requestedEntity + "<<<")
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

commonServices = {
        'Marco' : marco,
        'ListEntities' : listEntities,
        'ReturnHelp' : returnHelp,
        'ReturnUsage' : returnHelp,
        'ReturnVerboseHelp' : returnHelp,
        'ReturnSchema' : returnHelp
        }

def main():
  import importlib, os, sys
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
    data = file.read().replace('\n', '')
  commonServicer(data)
 

  print("""
The Entities are:
  """)
  print(listEntities())
  print("")

  if len(sys.argv) == 2:
    print("The available help options for  >>>" + sys.argv[1] + "<<<  are:")
    for i in entities.helpDict.keys():
      print("======================== " + i + " =====================================")
      print(returnHelp(sys.argv[1],i))
      print("=============================================================")
    print("Here is the result of Marco:")
    print(marco(sys.argv[1]))

if __name__ == "__main__":
  main() 
