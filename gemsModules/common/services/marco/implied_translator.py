#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.implied_requests import Implied_Services_Inputs
from gemsModules.common.services.each_service.implied_translator import Implied_Translator

from gemsModules.common.services.marco.api import marco_Request

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class marco_Implied_Translator(Implied_Translator):
    """ Inspect the Implied_Services_Inputs to figure out if this service needs to be run, and if so, how many times.
        Bundle resulting services into a service request package list (List[AAOP]).
    """

    def process(self, input_object : Implied_Services_Inputs) -> List[AAOP]:
        if input_object is not None and input_object.options is not None:
            the_options = input_object.options
            if 'cake' in the_options.keys() or 'color' in the_options.keys() :
#                print("found cake or color")
                service_request = marco_Request()
                service_request.options = {}
                if 'cake' in the_options.keys() :
                    service_request.options["cake"]=the_options["cake"]
                if 'color' in the_options.key_object() :
                    service_request.options["color"]=the_options["color"]
                this_aaop = AAOP(Dictionary_Name='implied_cake_marco', 
                        ID_String=uuid.uuid4(),
                        The_AAO=service_request,
                        AAO_Type='Marco')
                self.aaop_list.append(this_aaop)
        return self.get_aaop_list()

