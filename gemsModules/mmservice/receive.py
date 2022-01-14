import os, sys, importlib.util
import gemsModules
from gemsModules.common.services import *
from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *
from gemsModules.common.loggingConfig import *
import gemsModules.mmservice.settings as mmSettings
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  If this module is receiving a request, then there should be almost no
##  setup required other than whatever is specific to the modeling engine.
##
##  For example, if the modeling engine is amber, then it's ok to have to
##  specify a force field file for building prmtop/inpcrd.  And, it's ok
##  to need to generate an input-control file.  But, there should be no
##  building of coordinates, etc., which aren't really an amber thing.
##  (unless you write modules for using tleap to build, etc.....)
##


##TODO: REFACTOR for better encapsulation
##TODO: REFACTOR to use the new code (common.io rather than common.transaction)
##TODO: Use Doxygen-style comments.
"""
The receive() method receives a transaction, and checks for the requested service.
"""
def receive(thisTransaction):
    log.info("mmservice receive() was called.")
    request = thisTransaction.request_dict

    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}
    thisTransaction.response_dict['entity'] = {}
    thisTransaction.response_dict['entity']['type'] = "MmService"
    thisTransaction.response_dict['responses'] = []

    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doDefaultService(thisTransaction)
    else:
        services = getTypesFromList(thisTransaction.request_dict['entity']['services'])

        for requestedService in services:
            log.debug("requestedService: " + str(requestedService))
            ##Can we detect if this project has already been started?
            ##  If so, check the status of a job that exists, and start jobs that don't.
            if requestedService not in mmSettings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                log.error("services: " + str(mmSettings.serviceModules.keys()))
                thisTransaction.generateCommonParserNotice(noticeBrief='ServiceNotKnownToEntity')
            elif requestedService == "Amber":
                log.debug("Amber service requested.")

                startProject(thisTransaction)
            else:
                log.error("The requested service is still in development.")
                log.error("serviceModules.keys(): " + str(mmSettings.serviceModules.keys()))

    thisTransaction.build_outgoing_string()


def doDefaultService(thisTransaction):
    log.info("doDefaultService() was called.")
    # .setup.check(thisTransaction)
    # .amber.md.generate.plainMD(thisTransaction)
    # batchcompute.check(thisTransaction)
    # batchcompute.generatescript(thisTransaction)
    # batchcompute.submit(thisTransaction)

def main():
    ## TODO:  Make this look more like the main in delegator's receive.py
    ## TODO:  Make this do something successful even with no arguments.
    pass


if __name__ == "__main__":
    main()

