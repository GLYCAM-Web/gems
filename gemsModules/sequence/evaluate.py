#!/usr/bin/env python3
import sys, os

## TODO Write this function
def evaluateSequenceSanity(thisTransaction : Transaction):
    pass
def getSequenceGeometricOptions(thisTransaction : Transaction):
    pass




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
 



if __name__ == "__main__":
  main()
 
