#!/usr/bin/env python3
import uuid
from gemsModules.common.services.request_translator import JSON_to_Service_Request_translator
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.delegator.services.marco.api import marco_Request

## This needs to be split into two classes.  One will be used by the serrvice manager to
## extract the explicit services and to check that the services are available.  It will also
## set the default service.  The other
## will be specific to each service and will be used to extract the implicit services.
class marco_request_translator(JSON_to_Service_Request_translator):
    """ Inspect the incoming JSON object to figure out which services need 
        to be run.  Bundle these into a service request package list.
    """

    def add_default_services(self):
        service_request = marco_Request()
        this_aaop = AAOP(Dictionary_Name='implied_marco', 
                ID_String=uuid.uuid4(),
                The_AAO=service_request,
                AAO_Type='Marco')
        self.aaop_list.append(this_aaop)

    def add_implicit_services(self):
        if self.transaction.inputs.entity.inputs is not None:  
#            print("it is not none")
            this_dict = self.transaction.inputs.entity.inputs
#            print("here is the dict")
#            print(this_dict)
            if 'cake' in this_dict.keys() or 'color' in this_dict.keys() :
#                print("found cake or color")
                service_request = marco_Request()
                service_request.options = {}
                if 'cake' in self.transaction.inputs.entity.inputs.keys() :
                    service_request.options["cake"]=self.transaction.inputs.entity.inputs["cake"]
                if 'color' in self.transaction.inputs.entity.inputs.keys() :
                    service_request.options["color"]=self.transaction.inputs.entity.inputs["color"]
                this_aaop = AAOP(Dictionary_Name='implied_cake_marco', 
                        ID_String=uuid.uuid4(),
                        The_AAO=service_request,
                        AAO_Type='Marco')
#                print(this_aaop)
                self.aaop_list.append(this_aaop)