#!/usr/bin/env python3
import gemsModules, traceback
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from gemsModules.query import run_query

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


def doDefaultService(thisTransaction):
    # if thisTransaction.response_dict is None:
    #     thisTransaction.response_dict={}
    # thisTransaction.response_dict['entity']={}
    # thisTransaction.response_dict['entity']['type']='Entity!!!'
    # thisTransaction.response_dict['responses']=[]
    # thisTransaction.response_dict['responses'].append({'payload':marco('Query')})
    # thisTransaction.build_outgoing_string()
    log.debug("About to run query")
    run_query.buildQueryString(thisTransaction)

def receive(thisTransaction):
    log.info("Query received it")
    # doDefaultService(thisTransaction)
    # from . import run_query
    # run_query.buildQueryString(thisTransaction)

def main():
  import importlib.util, os, sys
  #from importlib import util
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
  jsonObjectString=utils.JSON_From_Command_Line(sys.argv)

  # with open(sys.argv[1], 'r') as file:
  #   jsonObjectString = file.read().replace('\n', '')
  # responseObjectString=delegate(jsonObjectString)
  # print(responseObjectString)


if __name__ == "__main__":
  main()
