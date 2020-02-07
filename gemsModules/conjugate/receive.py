#!/usr/bin/env python3
import gemsModules
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from gemsModules.project.projectUtil import *
import gemsModules.conjugate.settings as conjugateSettings

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.DEBUG

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

def doDefaultService(thisTransaction):
    log.info("doDefaultService() was called.\n")
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='Conjugate'
    thisTransaction.response_dict['responses']=[]
    buildGlycoprotein(thisTransaction)

    #thisTransaction.response_dict['responses'].append({'payload':marco('Conjugate')})


def receive(thisTransaction):
    log.info("receive() was called.\n")

    ##Begin building a response dict for holding output
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}
    thisTransaction.response_dict['entity'] = {}
    thisTransaction.response_dict['entity']['type'] = "Conjugate"
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
            if requestedService not in conjugateSettings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                log.error("services: " + str(conjugateSettings.serviceModules.keys()))
                appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity', requestedService)
            elif requestedService == "BuildGlycoprotein":
                buildGlycoprotein(thisTransaction)
            else:
                log.error("Logic should never reach this point. Look at congugate/receive.py.")

    thisTransaction.build_outgoing_string()

def buildGlycoprotein(thisTransaction):
    log.info("buildGlycoprotein() was called.\n")
    request = thisTransaction.request_dict
    log.debug("request: " + str(request))
    pdbFileName = ""
    attachments = []
    if 'inputs' in request['entity'].keys():
        inputs = request['entity']['inputs']
        log.debug("inputs: " + str(inputs))
        for element in inputs:
            log.debug("element: " + str(element))
            log.debug("keys: " + str(element.keys()))
            if "pdb_file_name" in element.keys():
                pdbFileName = element['pdb_file_name']['payload']
                log.debug("pdbFileName: " + pdbFileName)
            elif "attachments" in element.keys():
                attachments = element['attachments']
                log.debug("attachments: " + str(attachments))
            else:
                log.error("Have a look at the inputs. Expected 'pdb_file_name', and 'attachments'.")
                log.error("found: " + str(element.keys()))

        ##Verify that the pdb is in fact of type PDB.
        if pdbFileName != "":
            ##TODO: find a better way to verify that a file is a pdb file, as some may
            ##  legitimately not have the .pdb extension.
            if ".pdb" not in pdbFileName:
                noticeBrief = "For now, pdb files must have the .pdb extension. May change later."
                log.error(noticeBrief)
                ##Transaction, noticeBrief, blockID
                appendCommonParserNotice(thisTransaction, 'InvalidInput' )
            else:
                log.debug("Looks like a pdb file. Moving forward.")
        else:
            log.error("Failed to find a value for pdb_file_name.")
            appendCommonParserNotice(thisTransaction, 'InvalidInput' )


        ##For now, require attachments.
        if len(attachments) == 0:
            log.error("BuildGlycoprotein requests require 'attachments'.")
            appendCommonParserNotice(thisTransaction, 'InvalidInput' )
        else:
            log.debug("Attachments present. Moving forward.")

        log.debug("Still here. Starting a project.")
        startProject(thisTransaction)
        ##TODO: Maybe, If no attachments list is provided, attach Man9 to all likely positions.
        ## Alernatively, require that at least one attachment be present, though it is ok if
        ## it only provides the name of a glycan. If no sites are defined, attach that glycan
        ## to all likely sites.
    else:
        ##TODO: attach an error response.
        log.error("Could not find inputs in the request.")
        log.error(str(request.keys()))



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
  responseObjectString=delegate(jsonObjectString)
  print(responseObjectString)


if __name__ == "__main__":
  main()

