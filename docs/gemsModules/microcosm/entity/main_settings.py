#!/usr/bin/env python3
from typing import List, Dict
from ..common.main_settings import All_Available_Services as Common_Available_Services
from ..common.code_utils import GemsStrEnum

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

