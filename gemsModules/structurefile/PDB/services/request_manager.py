#!/usr/bin/env python3

from gemsModules.common.services.request_manager import Request_Manager
from gemsModules.common.services.explicit_requests import (
    Explicit_Service_Request_Manager,
)
from gemsModules.common.services.service_packages_list import (
    Services_Package_List_Utilities,
)
from gemsModules.structurefile.PDB.services.implied_requests import (
    AmberMDPrep_Implied_Services_Request_Manager,
)
from gemsModules.structurefile.PDB.services.default_requests import (
    AmberMDPrep_Default_Service_Request_Manager,
)
from gemsModules.structurefile.PDB.services.duplicate_requests import (
    AmberMDPrep_Duplicate_Requests_Manager,
)
from gemsModules.structurefile.PDB.services.request_data_filler import (
    PDB_Request_Data_Filler,
)
from gemsModules.structurefile.PDB.tasks import get_services_list

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Request_Manager(Request_Manager):
    def set_local_modules(self):
        self.explicit_manager_type = Explicit_Service_Request_Manager
        self.unknown_manager_type = Services_Package_List_Utilities
        self.implied_manager_type = AmberMDPrep_Implied_Services_Request_Manager
        self.duplicate_manager_type = AmberMDPrep_Duplicate_Requests_Manager
        self.default_manager_type = AmberMDPrep_Default_Service_Request_Manager
        self.data_filler_type = PDB_Request_Data_Filler
        self.available_services = get_services_list.execute()
