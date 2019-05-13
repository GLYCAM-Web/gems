#!/usr/bin/env python3

def delegate(jsonObject):
    import json
    from io import StringIO
    io=StringIO()
    json.loads(jsonObject)
    theObject = json.loads(jsonObject)
    if theObject['entity'] is None:
        print("This JSON object is not usable by the Delegator.")
        sys.exit(1)
    import gemsModules
    from gemsModules.common import entities
    if not theObject['entity']['type'] in entities.entityFunction:
        print("The entity in this JSON object is not known to the Delegator!")
    if theObject['entity']['type'] == 'Delegator' :
        from gemsModules.common import services
        services.commonServicer(jsonObject)
    else:
        entities.entityFunctions[theObject['entity']['type']](jsonObject)


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
    delegate(jsonObject)


if __name__ == "__main__":
  main()
 
