#!/usr/bin/env python3

from enum import Enum

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Service_Modules(Enum):
    from gemsModules.common.services import marco
    from gemsModules.common.services import status
    from gemsModules.common.services import aww_snap
    Default = aww_snap
    Marco = marco
    Status = status

# In this module, this is superfluous, but they ensure that this service uses
# the same names as other modules.  They also provide partial examples of how 
# to generate the lists in the individual service modules.
All_Service_Modules = Enum(
    "All_Service_Modules",
    [(avail.name, avail.value) for avail in Service_Modules] 
)
