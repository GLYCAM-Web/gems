#!/usr/bin/env python3
from typing import List, Dict
from gemsModules.docs.microcosm.common.main_settings import All_Available_Services as Common_Available_Services
from gemsModules.docs.microcosm.common.main_servicer_settings import All_Service_Modules as Common_Service_Modules
from gemsModules.docs.microcosm.common.code_utils import GemsStrEnum
from enum import Enum

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

class Module_Service_Modules(Enum):
    from gemsModules.docs.microcosm.entity import serviceA_servicer, serviceB1_servicer, serviceB2_servicer, serviceC_servicer
    ServiceA = serviceA_servicer
    ServiceB1 = serviceB1_servicer
    ServiceB2= serviceB2_servicer
    ServiceC = serviceC_servicer


All_Available_Services = GemsStrEnum(
    "All_Available_Services",
    [(avail.name, avail.value) for avail in Common_Available_Services] + 
    [(avail.name, avail.value) for avail in Module_Available_Services] 
)

All_Service_Modules = Enum(
    "All_Service_Modules",
    [(avail.name, avail.value) for avail in Common_Service_Modules] +
    [(avail.name, avail.value) for avail in Module_Service_Modules]
)
