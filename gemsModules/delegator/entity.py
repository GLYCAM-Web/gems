#!/usr/bin/env python3

def delegate(jsonObject):
    import gemsModules
    from gemsModules.common import services
    responseObject = services.commonServicer(jsonObject)
    import json
    #print(json.dumps(responseObject))
    return json.dumps(responseObject)


def defaultService(theObject):
    ## TODO give me something to do...
    import json
    responseObject={
            "entity" : "Delegator",
            "responses" : [
                {
                    'payload' : 'there is no default yet'
                    }
                ]
            }
    #print(json.dumps(responseObject))
    return json.dumps(responseObject)

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
  responseObject=delegate(jsonObject)
  print(responseObject)



if __name__ == "__main__":
  main()
 
