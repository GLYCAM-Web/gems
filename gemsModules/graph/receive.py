import sys, os, re, importlib.util
import gemsModules
import gmml

from . import settings
from gemsModules.common.services import *
from gemsModules.common.transaction import *


def receive(thisTransaction : Transaction):
    print("~~~graph module's receive.py has received a transation.")
    import gemsModules.graph

    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doTheDefaultService(thisTransaction)
        return

    input_services = thisTransaction.request_dict['entity']['services']
    requestedServices = getTypesFromList(input_services)

    print("requestedServices: " + str(requestedServices))

    print("graph.settings.serviceModules.keys(): " + str(settings.serviceModules.keys()))

    requestedServices = getTypesFromList(input_services)
    print("requestedServices: " + str(requestedServices))
    for requestedService in requestedServices:
        if requestedService not in common.settings.serviceModules.keys() and requestedService not in settings.serviceModules.keys():
            print("requestedService was not recognized: " + requestedService)
            common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
        else:
            print("requested service was recognized.")

            if thisTransaction.response_dict is None:
                thisTransaction.response_dict={}
            if not 'entity' in thisTransaction.response_dict:
                thisTransaction.response_dict['entity']={}
            if not 'type' in thisTransaction.response_dict['entity']:
                thisTransaction.response_dict['entity']['type']='Graph'
            if not 'responses' in thisTransaction.response_dict:
                thisTransaction.response_dict['responses']=[]

            thisTransaction.response_dict['responses'].append({"Draw" : {'payload': "The Graph module is in development. SVG content will go here." }})


    thisTransaction.build_outgoing_string()
    print("thisTransaction.outgoing_string: " + thisTransaction.outgoing_string)
