#!/usr/bin/env python3

"""
Use this file to test running the delegator from a python script.
"""

import importlib.util, os, sys
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
utils.investigate_gems_setup(sys.argv)

with open(sys.argv[1], 'r') as file:
  jsonObjectString = file.read().replace('\n', '')

from gemsModules.delegator.entity import delegate
responseObjectString=delegate(jsonObjectString)
print(responseObjectString)



