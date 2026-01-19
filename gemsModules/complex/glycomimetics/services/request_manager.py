#!/usr/bin/env python3

from gemsModules.common.services.request_manager import Request_Manager
from gemsModules.common.services.explicit_requests import (
    Explicit_Service_Request_Manager,
)
from gemsModules.common.services.service_packages_list import (
    Services_Package_List_Utilities,
)
from gemsModules.complex.glycomimetics.services.implied_requests import (
    Glycomimetics_Implied_Services_Request_Manager,
)
from gemsModules.complex.glycomimetics.services.default_requests import (
    Glycomimetics_Default_Service_Request_Manager,
)
from gemsModules.complex.glycomimetics.services.duplicate_requests import (
    Glycomimetics_Duplicate_Requests_Manager,
)
from gemsModules.complex.glycomimetics.services.workflow_manager import (
    Glycomimetics_Workflow_Manager,
)
from gemsModules.complex.glycomimetics.services.request_data_filler import (
    Glycomimetics_Request_Data_Filler,
)
from gemsModules.complex.glycomimetics.tasks import get_services_list

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Glycomimetics_Request_Manager(Request_Manager):
    def set_local_modules(self):
        self.explicit_manager_type = Explicit_Service_Request_Manager
        self.unknown_manager_type = Services_Package_List_Utilities
        self.implied_manager_type = Glycomimetics_Implied_Services_Request_Manager
        self.duplicate_manager_type = Glycomimetics_Duplicate_Requests_Manager
        self.default_manager_type = Glycomimetics_Default_Service_Request_Manager
        self.workflow_manager_type = Glycomimetics_Workflow_Manager
        self.data_filler_type = Glycomimetics_Request_Data_Filler
        self.available_services = get_services_list.execute()
