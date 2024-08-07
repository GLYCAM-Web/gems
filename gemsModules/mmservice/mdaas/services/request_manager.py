#!/usr/bin/env python3

from gemsModules.common.services.request_manager import Request_Manager

from gemsModules.common.services.service_packages_list import (
    Services_Package_List_Utilities,
)
from .implied_requests import mdaas_Implied_Services_Request_Manager
from .default_requests import mdaas_Default_Service_Request_Manager
from .duplicate_requests import mdaas_Duplicate_Requests_Manager
from .explicit_requests import mdaas_Explicit_Request_Manager

from gemsModules.mmservice.mdaas.services.workflow_manager import mdaas_Workflow_Manager
from gemsModules.mmservice.mdaas.services.request_data_filler import (
    mdaas_Request_Data_Filler,
)
from gemsModules.mmservice.mdaas.tasks import get_services_list

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class mdaas_Request_Manager(Request_Manager):
    def set_local_modules(self):
        self.explicit_manager_type = mdaas_Explicit_Request_Manager
        self.unknown_manager_type = Services_Package_List_Utilities
        self.implied_manager_type = mdaas_Implied_Services_Request_Manager
        self.duplicate_manager_type = mdaas_Duplicate_Requests_Manager
        self.default_manager_type = mdaas_Default_Service_Request_Manager
        self.workflow_manager_type = mdaas_Workflow_Manager
        self.data_filler_type = mdaas_Request_Data_Filler
        self.available_services = get_services_list.execute()
