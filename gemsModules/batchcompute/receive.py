#!/usr/bin/env python3
import gemsModules
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
import gemsModules.batchcompute.settings as batchcomputeSettings
from gemsModules.batchcompute.slurm.receive import manageIncomingString
import traceback
import json

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.ERROR

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

## File receive.py in gemsModules batchcompute

##  the receive function
##
##  Sanity checks:
##
##     - Basic json-ness of input should be checked upstream.
##       The input here should be a transaction
##     - Check that the requested service is known.
##
##  Possible actions to take:
##     - Return an error message
##     - Pass the transaction on to the Service


##TODO: Refactor for better encapsulation
##TODO: Use Doxygen-style comments.
def receive(thisTransaction):
    log.info("receive() was called.\n")

    ##Begin building a response dict for holding output
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}
    thisTransaction.response_dict['entity'] = {}
    thisTransaction.response_dict['entity']['type'] = "BatcchCompute"
    thisTransaction.response_dict['responses'] = []

    ##Look in transaction for the requested service. If none, do default service.
    if 'services' not in thisTransaction.request_dict['entity'].keys():
        log.debug("could not find the services key in ['entity']")
        doDefaultService(thisTransaction)
    else:
        services = getTypesFromList(thisTransaction.request_dict['entity']['services'])
        log.debug("requestedServices: " + str(services))
        for requestedService in services:
            log.debug("requestedService: " + str(requestedService))
            if requestedService not in batchcomputeSettings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                log.error("services: " + str(conjugateSettings.serviceModules.keys()))
                appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity', requestedService)
            elif requestedService == "BuildGlycoprotein":
                log.debug("")
            else:
                log.error("Logic should never reach this point. Look at congugate/receive.py.")

    thisTransaction.build_outgoing_string()

def doDefaultService(thisTransaction):
    log.info("doDefaultService() was called.\n")
    log.error("default service needs to be written for batchcompute.")

def submitGpScriptToSlurm(thisTransaction, gemsProject, sbatchArg):
    log.info("submitGpScriptToSlurm() was called.\n")
    log.debug("sbatchArgument: " + sbatchArg)
    if gemsProject is not None:

        outputDir = gemsProject.output_dir
        log.debug("outputDir: " + outputDir)
        #Remove the last /
        outputDir = outputDir[:-1]
        log.debug("outputDir" + outputDir)
    else:
        log.error("Gems project not found.")
        appendCommonParserNotice(thisTransaction, "InvalidInput")

    log.debug("Found the script.")
    jobInfoObject = {}
    jobInfoObject.update({
        "partition" : "amber",
        "user" : "webdev",
        "name" : "gp-test",
        "workingDirectory" : outputDir,
        "sbatchArgument" : sbatchArg
        })

    log.debug("jobInfoObject: " + str(jobInfoObject))
    try:
        response = manageIncomingString(json.dumps(jobInfoObject))
        log.debug("response from manageIncomingString:\n " + str(response).replace("\\", ""))
    except Exception as error:
        log.error("There was a problem calling manageIncomingString()")
        log.error("Error type: "+ str(type(error)))
        log.error(traceback.format_exc())
        response = error

    return response



##
##  Main:
##     - Same thing all the other mains do...
def main():
  import importlib.util, os, sys
  #from importlib import util
  if importlib.util.find_spec("gemsModules") is None:
    this_dir, this_filename = os.path.split(__file__)
    sys.path.append(this_dir + "/../")
    if importlib.util.find_spec("common") is None:
      print("I cannot find the Common Servicer.  No clue what to do. Exiting")
      sys.exit(1)
    else:
      from common import utils
  else:
    from gemsModules.common import utils
  jsonObjectString=utils.JSON_From_Command_Line(sys.argv)
  try:
    responseObjectString=delegate(jsonObjectString)
  except Exception as error:
    print("\nThe delegator module captured an error.")
    print("Error type: " + str(type(error)))
    print(traceback.format_exc())
    ##TODO: see about exploring this error and returning more info. Temp solution for now.
    responseObject = {
        'DelegatorNotice' : {
            'type' : 'UnknownError',
            'notice' : {
                'code' : '500',
                'brief' : 'unknownError',
                'blockID' : 'unknown',
                'message' : 'Not sure what went wrong. Error captured by the Delegator gemsModule.'
            }
        }
    }
    responseObjectString = str(responseObject)


  print("\ndelegator is returning this: \n" +  responseObjectString)

if __name__ == "__main__":
  main()
