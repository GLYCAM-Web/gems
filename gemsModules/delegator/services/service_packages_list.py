#!/usr/bin/env python3

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.error.api import error_Request

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class delegator_Services_Package_List_Manager:

    def get_available_services(self) -> List[str]:
        from gemsModules.delegator.tasks import get_services_list
        self.available_services = get_services_list.execute()
        return self.available_services

