#!/usr/bin/env python3
##  Use this file to:
##    * Test running the delegator from a python script.
##    * Run the GEMS Delegator as a standalone script.
import importlib.util, os, sys, faulthandler
faulthandler.enable()

if importlib.util.find_spec("gemsModules") is None:
  this_dir, this_filename = os.path.split(__file__)
  sys.path.append(this_dir + "/../")
  if importlib.util.find_spec("common") is None:
    sys.stderr.write("Unable to locate Common Services.  Exiting.\n")
    sys.exit(129)
  else:
    from common import utils
else:
  from gemsModules.common import utils
jsonObjectString=utils.JSON_From_Command_Line(sys.argv)


from gemsModules.delegator.receive import delegate
responseObjectString=delegate(jsonObjectString)
print(responseObjectString)



