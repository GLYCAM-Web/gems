#!/usr/bin/env python3
import sys, os

## TODO Write this function
def evaluateSequenceSanity(thisTransaction : Transaction):
    pass
def getSequenceGeometricOptions(thisTransaction : Transaction):
    pass


## TODO Make this not be a call to a compiled binary
def build3DStructure(thisTransaction : Transaction):
    # Check for environment variables that tell where things go
    # check out the environment
    OutputPath = os.environ.get('GEMS_MODULES_SEQUENCE_STRUCTURE_PATH')
    if OutputPath == None:
        OutputPath = os.environ.get('GEMS_MODULES_SEQUENCE_PATH')
    if OutputPath == None:
        OutputPath = os.environ.get('GEMS_MODULES_PATH')
    if OutputPath == None:
        OutputPath = '.' 
    # Set up the location where output files will be stored
    # This next function should check for directory name prefix or
    # if the complete spec is known or if a UUID should be generated
    OutputDirectorySpecification = getOutputDirectorySpecification(thisTransaction: Transaction)
    # Set up the location of the MD5Sum directory
    # Set up the location of the prep file to be used
    # Generate directories as needed
    # Save output files to the directories as needed
    # Run the program to generate the files
    # Return the name of the directory where the files reside
    pass
    

def defaultService(thisTransaction : Transaction):
    evaluate(thisTransaction : Transaction)
    build3DStructure(thisTransaction : Transaction)
#    import json
#    return json.dumps(responseObject)



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
 
