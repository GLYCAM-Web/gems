#!/usr/bin/env python3
from typing import List, Callable

from gemsModules.common.services.implied_requests import (
    Implied_Services_Request_Manager,
)


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Implied_Services_Request_Manager(Implied_Services_Request_Manager):
    """Inspect the incoming JSON object to figure out which services need
    to be run.  Bundle these into a service request package list.
    """

    def get_available_services(self) -> List[str]:
        log.info("In AmberMDPrep_Implied_Services_Request_Manager, get_available_services")
        from gemsModules.structurefile.PDBFile.tasks import get_services_list
        return get_services_list.execute()

    def get_implicit_service_manager(self, service: str) -> Callable:
        log.info("In AmberMDPrep_Implied_Services_Request_Manager, get_implicit_service_manager")
        log.debug("service: " + str(service))
        from gemsModules.structurefile.PDBFile.services.settings.implied_modules import module_loader
        return module_loader.get_module_attr(service)

