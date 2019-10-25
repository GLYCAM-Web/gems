import sys, os, re, importlib.util
import gemsModules
import gmml
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from . import settings
from datetime import datetime


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
                print("finished generating the report. Building outgoing string.")
                thisTransaction.build_outgoing_string()
            else:
                print("Perhaps a service was added to settings.py, but not defined in receive.py? Likely this service is still in development.")

##This method needs to check for options. If options are not present, do the default service.
##    If the options are present, and specify a list of entities to report on, only report on those.
def generateReport(thisTransaction : Transaction, thisService : Service = None):
    print("generateReport was called.")

    entityKeys = thisTransaction.request_dict['entity'].keys()
    #print("entityKeys : " + str(entityKeys))

    if 'options' in entityKeys:
        #print("User provided options.")
        optionsKeys = thisTransaction.request_dict['entity']['options'].keys()
        options = thisTransaction.request_dict['entity']['options']
        #print("optionsKeys: " + str(optionsKeys))
        if "targets" in optionsKeys:
            for target in options['targets']:
                #print("Report requested for target: " + str(target))
                print("target type: " + str(target['type']))

                if target['type'] == 'All':
                    doDefaultService(thisTransaction)
                else:
                    print("Report requested for a specific target.")

        else:
            doDefaultService(thisTransaction)

    else:
        doDefaultService(thisTransaction)

## The default here is to just report on every gemsModule and their corresponding services.
def doDefaultService(thisTransaction : Transaction):
    print("doDefaultService() was called. Generating a status report for all entities and services.")
    print("thisTransaction: " + str(thisTransaction))

    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}

    thisTransaction.response_dict['entity'] = {}
    thisTransaction.response_dict['entity']['type']="StatusReport"
    timestamp = str(datetime.now())
    print("timestamp: " + str(timestamp))

    thisTransaction.response_dict['entity']['timestamp'] = timestamp

    if 'responses' not in thisTransaction.response_dict:
        thisTransaction.response_dict['responses'] = []


    for availableEntity in listEntities():
        print("Generating a report for entity: " + availableEntity)
        response = {}
        thisEntity = importEntity(availableEntity)
        response.update({
            'entity' : availableEntity
        })
        #print("thisEntity.__dict__.keys(): " + str(thisEntity.__dict__.keys()))
        if thisEntity.settings is not None:
            settings = thisEntity.settings
            settingsAttributes = settings.__dict__.keys()

            if 'status' in settingsAttributes:
                status = settings.status
                print("     settings.status: " + status)
                response.update({
                    'status' : status
                })

            if 'moduleStatusDetail' in settingsAttributes:
                moduleStatusDetail = settings.moduleStatusDetail
                print("     settings.moduleStatusDetail: " + moduleStatusDetail)
                response.update({
                    'moduleStatusDetail' : moduleStatusDetail
                })


            if 'servicesStatus' in settingsAttributes:
                serviceStatuses= []
                for element in settings.servicesStatus:
                    #print("serviceStatus: " + str(serviceStatus))
                    #print("serviceStatus.keys(): " + str(serviceStatus.keys()))
                    service = element['service']
                    print("service: " + service)
                    serviceStatus = element['status']
                    print("serviceStatus: " + serviceStatus)
                    serviceStatusDetail = element['statusDetail']
                    print("statusDetail: " + serviceStatusDetail)

                    serviceStatuses.append(element)

                response.update({
                    'services' : serviceStatuses
                })

            if 'subEntities' in settingsAttributes:
                subEntities = []
                for element in subEntities:
                    subEntity = element['subEntity']
                    subEntities.append(element)

                response.update({
                    'subEntities' : subEntities
                })

            thisTransaction.response_dict['responses'].append(response)

        else:
            print("Could not find settings for this entity.")
    print("finished updating the transaction.")

    print("timestamp: " + str(timestamp))









def main():
    pass

if __name__ == "__main__":
  main()
