import sys, os, re, importlib.util
import gemsModules
import gmml
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from . import settings

def receive(thisTransaction : Transaction):
    print("status gemsModule receive.py receive() was called.")

    if not 'services' in thisTransaction.request_dict['entity'].keys():
        print("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        return
    else:
        services = getTypesFromList(thisTransaction.request_dict['entity']['services'])
        for requestedService in services:
            print("requestedService: " + str(requestedService))
            if requestedService not in settings.serviceModules.keys():
                if requestedService not in common.settings.serviceModules.keys():
                    print("The requested service is not recognized.")
                    common.settings.appendCommonParserNotice( thisTransaction, 'ServiceNotKnownToEntity', requestedService)
            elif requestedService == "GenerateReport":
                generateReport(thisTransaction, None)
                thisTransaction.build_outgoing_string()

def generateReport(thisTransaction : Transaction, thisService : Service = None):
    print("generateReport was called.")

    entityKeys = thisTransaction.request_dict['entity'].keys()
    print("entityKeys : " + str(entityKeys))

    if 'options' in entityKeys:
        print("User provided options.")
        optionsKeys = thisTransaction.request_dict['entity']['options'].keys()
        options = thisTransaction.request_dict['entity']['options']
        print("optionsKeys: " + str(optionsKeys))
        if "targets" in optionsKeys:
            for target in options['targets']:
                print("Report requested for target: " + str(target))
                print("target type: " + str(target['type']))

                if target['type'] == 'All':
                    doDefaultService(thisTransaction)
                else:
                    print("Report requested for a specific target.")

        else:
            doDefaultService(thisTransaction)

    else:
        doDefaultService(thisTransaction)


def doDefaultService(thisTransaction : Transaction):
    print("doDefaultService() was called. Generating a status report for all entities and services.")

    for availableEntity in listEntities():
        print("Generating a report for entity: " + availableEntity)
        thisEntity = importEntity(availableEntity)
        print("thisEntity: " + str(thisEntity))

        print("thisEntity.__dict__.keys(): " + str(thisEntity.__dict__.keys()))
        if thisEntity.settings is not None:
            settings = thisEntity.settings
            print("thisEntity's settings: " + str(settings))
            #TODO: Look in settings for a status
            #TODO: Decide what to report if no status is present.
            #TODO: Decide what to show for each entity & each service it offers.
        else:
            print("Could not find settings for this entity.")



def main():
    pass

if __name__ == "__main__":
  main()
