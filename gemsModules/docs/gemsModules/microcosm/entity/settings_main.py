#!/usr/bin/env python3
from typing import List, Dict, Union
from ..common.settings_main import All_Available_Services as Common_Available_Services
from ..common.code_utils    import GemsStrEnum
from  .serviceA_api      import ServiceA_Service, ServiceA_Response
from  .serviceB1_api     import ServiceB1_Service, ServiceB1_Response
from  .serviceB2_api     import ServiceB2_Service, ServiceB2_Response
from  .serviceC_api      import ServiceC_Service, ServiceC_Response

WhoIAm = "Module_Entity"

class Module_Available_Services(GemsStrEnum):
    """
    The services that this module provides.
    These should be listed in the order that they are expected to be used.
    """
    serviceA = "ServiceA"
    serviceB1 = "ServiceB1"
    serviceB2= "ServiceB2"
    serviceC = "ServiceC"

mas = Module_Available_Services # because it's a long name
Module_Service_Dependencies : Dict[str, List[str]] = {
    mas.serviceB2: [mas.serviceB1]
    }

All_Available_Services = GemsStrEnum(
    "All_Available_Services",
    [(avail.name, avail.value) for avail in Common_Available_Services] + 
    [(avail.name, avail.value) for avail in Module_Available_Services] 
)

Module_Available_Service_APIs = Union[
        ServiceA_Service,
        ServiceB1_Service,
        ServiceB2_Service,
        ServiceC_Service
        ]
Module_Available_Response_APIs = Union[
        ServiceA_Response,
        ServiceB1_Response,
        ServiceB2_Response,
        ServiceC_Response
        ]
