#!/usr/bin/env python3
from typing import  List, Callable

from gemsModules.common.services.implied_requests import Implied_Services_Request_Manager

from gemsModules.delegator.tasks import get_services_list
from gemsModules.delegator.services.settings.implied_modules import implied_modules 

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class delegator_Implied_Services_Request_Manager(Implied_Services_Request_Manager):
    """ Inspect the incoming JSON object to figure out which services need 
        to be run.  Bundle these into a service request package list.
    """

    def get_available_services(self) -> List[str]:
        return get_services_list.execute()

    def get_implicit_service_manager(self, service : str) -> Callable:
        return implied_modules[service]
        

