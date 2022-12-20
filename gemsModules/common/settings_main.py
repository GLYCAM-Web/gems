#!/usr/bin/env python3

# As much as possible, all the specifics, the non-abstractions, should be in a settings file.

from .code_utils import GemsStrEnum

from . import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

WhoIAm = 'CommonServicer'

class Available_Services(GemsStrEnum):
    """
    The services that this module provides.
    These should be listed in the order that they are expected to be used.
    """
    marco = 'Marco'
    status = 'Status'

# In this module, this is superfluous, but they ensure that this service uses
# the same names as other modules.  They also provide partial examples of how 
# to generate the lists in the individual service modules.
All_Available_Services = GemsStrEnum(
    "All_Available_Services",
    [(avail.name, avail.value) for avail in Available_Services] 
)
