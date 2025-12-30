#!/usr/bin/env python3

from gemsModules.common.services.request_manager import Request_Manager
from gemsModules.common.services.service_packages_list import Services_Package_List_Utilities
from gemsModules.conjugate.glycoprotein.services.implied_requests import GpBuilder_Implied_Services_Request_Manager 
from gemsModules.conjugate.glycoprotein.services.default_requests import Gpbuilder_Default_Service_Request_Manager
from gemsModules.conjugate.glycoprotein.services.explicit_requests import GpBuilder_Explicit_Request_Manager
from gemsModules.conjugate.glycoprotein.services.duplicate_requests import Gpbuilder_Duplicate_Requests_Manager
from gemsModules.conjugate.glycoprotein.services.request_data_filler import Gpbuilder_Request_Data_Filler
from gemsModules.conjugate.glycoprotein.services.workflow_manager import GpBuilder_Workflow_Manager
from gemsModules.conjugate.glycoprotein.tasks import get_services_list

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Gpbuilder_Request_Manager(Request_Manager):
    
    def set_local_modules(self):
        self.explicit_manager_type = GpBuilder_Explicit_Request_Manager
        self.unknown_manager_type = Services_Package_List_Utilities
        self.implied_manager_type = GpBuilder_Implied_Services_Request_Manager
        self.duplicate_manager_type = Gpbuilder_Duplicate_Requests_Manager
        self.default_manager_type = Gpbuilder_Default_Service_Request_Manager
        self.workflow_manager_type = GpBuilder_Workflow_Manager

        self.data_filler_type = Gpbuilder_Request_Data_Filler
        self.available_services = get_services_list.execute()

