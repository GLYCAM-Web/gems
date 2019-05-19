#!/usr/bin/env python3

def evaluate(jsonDict):
    pass

def build3DStructure(jsonDict):
    pass
    

def defaultService(jsonDict):
    evaluate(jsonDict)
    build3DStructure(jsonDict)
    import json
    return json.dumps(responseObject)



def main():
  import importlib.util, os, sys
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
 
