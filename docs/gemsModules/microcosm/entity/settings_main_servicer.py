#!/usr/bin/env python3
from enum import Enum
from ..common.settings_main_servicer import All_Service_Modules as Common_Service_Modules


class Module_Service_Modules(Enum):
    from . import serviceA_servicer, serviceB1_servicer, serviceB2_servicer, serviceC_servicer
    ServiceA = serviceA_servicer
    ServiceB1 = serviceB1_servicer
    ServiceB2= serviceB2_servicer
    ServiceC = serviceC_servicer


All_Service_Modules = Enum(
    "All_Service_Modules",
    [(avail.name, avail.value) for avail in Common_Service_Modules] +
    [(avail.name, avail.value) for avail in Module_Service_Modules]
)
