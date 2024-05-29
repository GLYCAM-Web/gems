#!/usr/bin/env python3

# As much as possible, all the specifics, the non-abstractions, should be in a settings file.

from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Module_Available_Services(GemsStrEnum):
    """
    The services that this module provides.
    These should be listed in the order that they are expected to be used.
    """

    error = "Error"
    marco = "Marco"
    status = "Status"
    list_services = "ListServices"


Multiples_Action = {
    ##  What to do if there are multiple requests for the same service.
    ##
    ##  Merge = Attempt to merge them into a single request (only one request is allowed)
    ##  Fail = Do not attempt to process any of the service requests.
    ##  All = Process each request (multiples are allowed).
    ##
    ##  In all cases, an informative Notice should be returned.
    "Error": "All",
    "Marco": "Merge",
    "Status": "Merge",
    "ListServices": "Merge",
}

Request_Conflict_Action = {
    ##  What to do if a service request has an internal conflict.
    ##
    ##  Fail = stop processing the service
    ##  LastIn = Overwrite the conflicted setting and act on whichever comes last
    ##  FirstIn = Act on the first conflicted setting
    ##
    ##  In all cases, an informative Notice should be returned.
    "Error": "FirstIn",
    "Marco": "Fail",
    "Status": "LastIn",
    "ListServices": "LastIn",
}


# In this module, this is superfluous, but it ensures that this service uses
# the same names as other modules.  They also provide partial examples of how
# to generate the lists in the individual service modules.
# Available_Services = GemsStrEnum(
#     "Available_Services",
#     [(avail.name, avail.value) for avail in Module_Available_Services]
# )


# above, but as a class
class Available_Services(GemsStrEnum):
    """
    The services that this module provides.
    These should be listed in the order that they are expected to be used.
    """

    def __init__(self):
        super().__init__(
            [(avail.name, avail.value) for avail in Module_Available_Services]
        )
