#!/usr/bin/env python3
from gemsModules.common import logic
from gemsModules.common import utils
from gemsModules.common.loggingConfig import *
from gemsModules.structureFile.amber.preprocess import preprocessPdbForAmber
import gemsModules.conjugate.glycoprotein
import gemsModules.conjugate.settings as settings
import gemsModules.conjugate.jsoninterface as conjugateio

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

###
### For conjugate, the default is Marco-Polo, maybe with help text.
###
def doDefaultService(jsonObjectString):
    log.info("doDefaultService() was called.\n")
    thisTransaction=conjugateio.Transaction(jsonObjectString)
    thisTransaction.outputs.entity.entityType=settings.WhoIAm
    thisTransaction.outputs.entity.responses=[]
    thisTransaction.outputs.entity.responses.append({'payload': logic.marco(settings.WhoIAm)})
    return thisTransaction


def receive(jsonObjectString, entityType=None):
    log.info("receive() in conjugate was called.\n")
    if entityType is None:
        entityType = logic.getEntityTypeFromJson(jsonObjectString)
        if entityType is None: 
            return logic.buildInvalidInputErrorResponse(
                    thisMessagingEntity=settings.WhoIAm,
                    message="entity type not found in json input string")

    if entityType == 'Glycoprotein':
        returnedTransaction = glycoprotein.receive.receive(
                    jsonObjectString,
                    entityType=entityType)
        return returnedTransaction


    ##Look in transaction for the requested service. If none, do default service.
    if 'services' not in jsonObjectString:
        log.debug("could not find the services in the input - calling default")
        return doDefaultService(jsonObjectString)

    theServices = logic.getServicesFromJson(jsonObjectString)
    if theServices is None:
        return logic.buildInvalidInputErrorResponseJsonString(
                thisMessagingEntity=settings.WhoIAm,
                message="something went wrong trying to get the list of services")
    if theServices == []:
        log.debug("found services, but there are no keys.  Calling default")
        doDefaultService(jsonObjectString)
    log.debug("requestedServices: " + str(services))
    for requestedService in services:
        log.debug("requestedService: " + str(requestedService))
        if requestedService not in settings.serviceModules.keys():
            theMessage="requested service not known to entity"
            log.error(theMessage)
            log.error("requested services: " + str(settings.serviceModules.keys()))
            ## This could be made to be more specific - or not
            return logic.buildInvalidInputErrorResponseJsonString(
                    thisMessagingEntity=settings.WhoIAm,
                    message=theMessage)
        # for now, send everything to glycoprotein builder.  This must change.
        returnedTransaction = glycoprotein.receive.receive(
                    jsonObjectString,
                    entityType=entityType)
        return returnedTransaction


def main():
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

  jsonObjectString=utils.JSON_From_Command_Line(sys.argv)
  returnedTransaction=receive(jsonObjectString)
  returnedTransaction.build_outgoing_string()
  print(returnedTransaction.outgoing_string)


if __name__ == "__main__":
  main()

