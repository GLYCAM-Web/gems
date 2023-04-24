#!/usr/bin/env python3

from gemsModules.common.services.request_manager import Request_Manager
from gemsModules.common.services.explicit_requests import Explicit_Service_Request_Manager
from gemsModules.common.services.service_packages_list import Services_Package_List_Utilities
from gemsModules.delegator.services.implied_requests import delegator_Implied_Services_Request_Manager 
from gemsModules.delegator.services.default_requests import delegator_Default_Service_Request_Manager
from gemsModules.delegator.services.duplicate_requests import delegator_Duplicate_Requests_Manager
from gemsModules.delegator.services.request_data_filler import delegator_Request_Data_Filler
from gemsModules.delegator.tasks import get_services_list

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class delegator_Request_Manager(Request_Manager):
    
    def set_local_modules(self):
        self.explicit_manager = Explicit_Service_Request_Manager(entity=self.entity)
        self.unknown_manager = Services_Package_List_Utilities(aaop_list=self.explicit_aaops)
        self.implied_manager = delegator_Implied_Services_Request_Manager(input_object = self.entity)
        self.duplicate_manager = delegator_Duplicate_Requests_Manager(aaop_list=self.aaop_list)
        self.default_manager = delegator_Default_Service_Request_Manager()
        self.data_filler = delegator_Request_Data_Filler(aaop_list=self.aaop_list, entity=self.entity, project=self.project)
        self.available_services = get_services_list.execute()

