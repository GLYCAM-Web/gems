#!/usr/bin/env python3

from gemsModules.common.services.request_manager import Request_Manager
from gemsModules.common.services.explicit_requests import (
    Explicit_Service_Request_Manager,
)
from gemsModules.common.services.service_packages_list import (
    Services_Package_List_Utilities,
)
from gemsModules.complex.antibody.services.implied_requests import (
    Antibody_Implied_Services_Request_Manager,
)
from gemsModules.complex.antibody.services.default_requests import (
    Antibody_Default_Service_Request_Manager,
)
from gemsModules.complex.antibody.services.duplicate_requests import (
    Antibody_Duplicate_Requests_Manager,
)
from gemsModules.complex.antibody.services.workflow_manager import (
    Antibody_Workflow_Manager,
)
from gemsModules.complex.antibody.services.request_data_filler import (
    Antibody_Request_Data_Filler,
)
from gemsModules.complex.antibody.tasks import get_services_list

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Antibody_Request_Manager(Request_Manager):
    def set_local_modules(self):
        self.explicit_manager_type = Explicit_Service_Request_Manager
        self.unknown_manager_type = Services_Package_List_Utilities
        self.implied_manager_type = Antibody_Implied_Services_Request_Manager
        self.duplicate_manager_type = Antibody_Duplicate_Requests_Manager
        self.default_manager_type = Antibody_Default_Service_Request_Manager
        self.workflow_manager_type = Antibody_Workflow_Manager
        self.data_filler_type = Antibody_Request_Data_Filler
        self.available_services = get_services_list.execute()
