#!/usr/bin/env python3

from enum import Enum

from gemsModules.docs.microcosm.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

class Service_Modules(Enum):
    from gemsModules.docs.microcosm.common import marco_servicer, status_servicer
    Default = marco_servicer 
    Marco = marco_servicer
    Status = status_servicer

# In this module, this is superfluous, but they ensure that this service uses
# the same names as other modules.  They also provide partial examples of how 
# to generate the lists in the individual service modules.
All_Service_Modules = Enum(
    "All_Service_Modules",
    [(avail.name, avail.value) for avail in Service_Modules] 
)
