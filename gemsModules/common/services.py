#!/usr/bin/env python3
#import sys
#import os
#import subprocess
#import json
#from io import StringIO
#from gemsModules.common import data

class commonServices:
  """Services for all of the GEMS Modules"""

  marco = "Polo"


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


  if sys.argv[1] == 'Marco':
    print(commonServices.marco)
  else:
    print("Unrecognized request to commonServices")
 

if __name__ == "__main__":
  main() 
