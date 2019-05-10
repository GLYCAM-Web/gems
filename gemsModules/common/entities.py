#!/usr/bin/env python3
import sys,importlib

if importlib.util.find_spec("gemsModules") is None:
  sys.exit(1)

from gemsModules import delegator, glycoprotein, sequence

entityFunction = {
  'Delegator'         : delegator ,
  'Sequence'          : sequence ,
  'Glycoprotein'      : glycoprotein
}
helpDict = {
  'Usage'     : 'usageText',
  'Help'      : 'basicHelpText',
  'More Help' : 'moreHelpText',
  'Schema'    : 'schemaLocation'
}

def marco(requestedEntity):
  if hasattr(entityFunction[requestedEntity], 'entity'):
    return "Polo"
  else:
    return "The entity you seek is not responding."

def listEntities():
  return list(entityFunction.keys())

def returnHelp(requestedEntity,requestedHelp):
  if helpDict[requestedHelp] == 'schemaLocation':
    return "Here there should be a location for the schema"  ## TODO:  make this do something real
  if not hasattr(entityFunction[requestedEntity], 'helpme'):
    return "No help available for the requestedEntity"
  helpLocation = getattr(entityFunction[requestedEntity], 'helpme')
  if not hasattr(helpLocation,helpDict[requestedHelp]):
    return "The requestedHelp is not available for the requestedEntity"
  thisHelp =  getattr(helpLocation, helpDict[requestedHelp])
  if thisHelp is None:
    return "Something went wrong getting the requestedHelp from the requestedEntity"
  return thisHelp

def main():
  print("""
The Entities are:
  """)
  print(listEntities())
  print("")

  if len(sys.argv) == 2:
    print("The available help options for  >>>" + sys.argv[1] + "<<<  are:")
    for i in helpDict.keys():
      print("======================== " + i + " =====================================")
      print(returnHelp(sys.argv[1],i))
      print("=============================================================")
    print("Here is the result of Marco:")
    print(marco(sys.argv[1]))
  
if __name__ == "__main__":
  main()

